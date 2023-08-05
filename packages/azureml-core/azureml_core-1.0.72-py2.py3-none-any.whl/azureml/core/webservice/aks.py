# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for managing the Azure Kubernetes Service Webservices in Azure Machine Learning service."""

import copy
import json
import logging
import re
import requests
from dateutil.parser import parse
from azureml._base_sdk_common.tracking import global_tracking_info_registry
from azureml._model_management._constants import AKS_ENDPOINT_TYPE
from azureml._model_management._constants import AKS_WEBSERVICE_TYPE
from azureml._model_management._constants import MMS_WORKSPACE_API_VERSION
from azureml._model_management._constants import NAMESPACE_REGEX
from azureml._model_management._constants import WEBSERVICE_SWAGGER_PATH
from azureml._model_management._util import _get_mms_url
from azureml._model_management._util import build_and_validate_no_code_environment_image_request
from azureml._model_management._util import convert_parts_to_environment
from azureml._model_management._util import get_requests_session
from azureml._model_management._util import webservice_name_validation
from azureml._restclient.clientbase import ClientBase
from azureml.core.compute import ComputeTarget
from azureml.core.environment import Environment
from azureml.core.model import Model
from azureml.core.image import Image
from azureml.core.webservice import Webservice
from azureml.core.webservice.webservice import WebserviceDeploymentConfiguration
from azureml.exceptions import WebserviceException
from datetime import datetime
from enum import Enum

module_logger = logging.getLogger(__name__)


class AksWebservice(Webservice):
    """Class for Azure Kubernetes Service Webservices."""

    _expected_payload_keys = Webservice._expected_payload_keys + ['appInsightsEnabled', 'authEnabled',
                                                                  'autoScaler', 'computeName',
                                                                  'containerResourceRequirements', 'dataCollection',
                                                                  'maxConcurrentRequestsPerContainer',
                                                                  'maxQueueWaitMs', 'numReplicas', 'scoringTimeoutMs',
                                                                  'scoringUri', 'livenessProbeRequirements',
                                                                  'aadAuthEnabled']
    _webservice_type = AKS_WEBSERVICE_TYPE

    def _initialize(self, workspace, obj_dict):
        """Initialize the Webservice instance.

        This is used because the constructor is used as a getter.

        :param workspace:
        :type workspace: azureml.core.Workspace
        :param obj_dict:
        :type obj_dict: dict
        :return:
        :rtype: None
        """
        # Validate obj_dict with _expected_payload_keys
        AksWebservice._validate_get_payload(obj_dict)

        # Initialize common Webservice attributes
        super(AksWebservice, self)._initialize(workspace, obj_dict)

        # Initialize expected AksWebservice specific attributes
        self.enable_app_insights = obj_dict.get('appInsightsEnabled')
        self.autoscaler = AutoScaler.deserialize(obj_dict.get('autoScaler'))
        self.compute_name = obj_dict.get('computeName')
        self.container_resource_requirements = \
            ContainerResourceRequirements.deserialize(obj_dict.get('containerResourceRequirements'))
        self.liveness_probe_requirements = \
            LivenessProbeRequirements.deserialize(obj_dict.get('livenessProbeRequirements'))
        self.data_collection = DataCollection.deserialize(obj_dict.get('dataCollection'))
        self.max_concurrent_requests_per_container = obj_dict.get('maxConcurrentRequestsPerContainer')
        self.max_request_wait_time = obj_dict.get('maxQueueWaitMs')
        self.num_replicas = obj_dict.get('numReplicas')
        self.scoring_timeout_ms = obj_dict.get('scoringTimeoutMs')
        self.scoring_uri = obj_dict.get('scoringUri')
        self.is_default = obj_dict.get('isDefault')
        self.traffic_percentile = obj_dict.get('trafficPercentile')
        self.version_type = obj_dict.get('type')

        self.token_auth_enabled = obj_dict.get('aadAuthEnabled')
        env_dict = obj_dict.get('environment')
        self.environment = Environment._deserialize_and_add_to_object(env_dict) if env_dict else None
        models = obj_dict.get('models')
        self.models = [Model.deserialize(workspace, model_payload) for model_payload in models] if models else []

        # Initialize other AKS utility attributes
        self.deployment_status = obj_dict.get('deploymentStatus')
        self.namespace = obj_dict.get('namespace')
        self.swagger_uri = '/'.join(self.scoring_uri.split('/')[:-1]) + WEBSERVICE_SWAGGER_PATH \
            if self.scoring_uri else None
        self._model_config_map = obj_dict.get('modelConfigMap')
        self._refresh_token_time = None

    def __repr__(self):
        """Return the string representation of the AksWebservice object.

        :return: String representation of the AksWebservice object
        :rtype: str
        """
        return super().__repr__()

    @staticmethod
    def deploy_configuration(autoscale_enabled=None, autoscale_min_replicas=None, autoscale_max_replicas=None,
                             autoscale_refresh_seconds=None, autoscale_target_utilization=None,
                             collect_model_data=None, auth_enabled=None, cpu_cores=None, memory_gb=None,
                             enable_app_insights=None, scoring_timeout_ms=None, replica_max_concurrent_requests=None,
                             max_request_wait_time=None, num_replicas=None, primary_key=None, secondary_key=None,
                             tags=None, properties=None, description=None, gpu_cores=None, period_seconds=None,
                             initial_delay_seconds=None, timeout_seconds=None, success_threshold=None,
                             failure_threshold=None, namespace=None, token_auth_enabled=None):
        """Create a configuration object for deploying to an AKS compute target.

        :param autoscale_enabled: Whether or not to enable autoscaling for this Webservice.
            Defaults to True if num_replicas is None
        :type autoscale_enabled: bool
        :param autoscale_min_replicas: The minimum number of containers to use when autoscaling this Webservice.
            Defaults to 1
        :type autoscale_min_replicas: int
        :param autoscale_max_replicas: The maximum number of containers to use when autoscaling this Webservice.
            Defaults to 10
        :type autoscale_max_replicas: int
        :param autoscale_refresh_seconds: How often the autoscaler should attempt to scale this Webservice.
            Defaults to 1
        :type autoscale_refresh_seconds: int
        :param autoscale_target_utilization: The target utilization (in percent out of 100) the autoscaler should
            attempt to maintain for this Webservice. Defaults to 70
        :type autoscale_target_utilization: int
        :param collect_model_data: Whether or not to enable model data collection for this Webservice.
            Defaults to False
        :type collect_model_data: bool
        :param auth_enabled: Whether or not to enable key auth for this Webservice. Defaults to True
        :type auth_enabled: bool
        :param cpu_cores: The number of cpu cores to allocate for this Webservice. Can be a decimal. Defaults to 0.1
        :type cpu_cores: float
        :param memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal.
            Defaults to 0.5
        :type memory_gb: float
        :param enable_app_insights: Whether or not to enable Application Insights logging for this Webservice.
            Defaults to False
        :type enable_app_insights: bool
        :param scoring_timeout_ms: A timeout to enforce for scoring calls to this Webservice. Defaults to 60000
        :type scoring_timeout_ms: int
        :param replica_max_concurrent_requests: The number of maximum concurrent requests per node to allow for this
            Webservice. Defaults to 1
        :type replica_max_concurrent_requests: int
        :param max_request_wait_time: The maximum amount of time a request will stay in the queue (in milliseconds)
            before returning a 503 error. Defaults to 500
        :type max_request_wait_time: int
        :param num_replicas: The number of containers to allocate for this Webservice. No default, if this parameter
            is not set then the autoscaler is enabled by default.
        :type num_replicas: int
        :param primary_key: A primary auth key to use for this Webservice
        :type primary_key: str
        :param secondary_key: A secondary auth key to use for this Webservice
        :type secondary_key: str
        :param tags: Dictionary of key value tags to give this Webservice
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to give this Webservice. These properties cannot
            be changed after deployment, however new key value pairs can be added
        :type properties: dict[str, str]
        :param description: A description to give this Webservice
        :type description: str
        :param gpu_cores: The number of gpu cores to allocate for this Webservice. Default is 1
        :type gpu_cores: int
        :param period_seconds: How often (in seconds) to perform the liveness probe. Default to 10 seconds.
            Minimum value is 1.
        :type period_seconds: int
        :param initial_delay_seconds: Number of seconds after the container has started before liveness probes are
            initiated. Defaults to 310
        :type initial_delay_seconds: int
        :param timeout_seconds: Number of seconds after which the liveness probe times out. Defaults to 2 second.
            Minimum value is 1
        :type timeout_seconds: int
        :param success_threshold: Minimum consecutive successes for the liveness probe to be considered successful
            after having failed. Defaults to 1. Minimum value is 1.
        :type success_threshold: int
        :return: A configuration object to use when
        :param failure_threshold: When a Pod starts and the liveness probe fails, Kubernetes will try failureThreshold
            times before giving up. Defaults to 3. Minimum value is 1.
        :type failure_threshold: int deploying a Webservice object
        :param namespace: The Kubernetes namespace in which to deploy this Webservice: up to 63 lowercase alphanumeric
            ('a'-'z', '0'-'9') and hyphen ('-') characters. The first and last characters cannot be hyphens.
        :type namespace: str
        :param token_auth_enabled: Whether or not to enable Token auth for this Webservice. If this is
            enabled, users can access this Webservice by fetching access token using their Azure Active Directory
            credentials. Defaults to False
        :type token_auth_enabled: bool
        :rtype: AksServiceDeploymentConfiguration
        :raises: azureml.exceptions.WebserviceException
        """
        config = AksServiceDeploymentConfiguration(autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                                                   autoscale_refresh_seconds, autoscale_target_utilization,
                                                   collect_model_data, auth_enabled, cpu_cores, memory_gb,
                                                   enable_app_insights, scoring_timeout_ms,
                                                   replica_max_concurrent_requests, max_request_wait_time,
                                                   num_replicas, primary_key, secondary_key, tags, properties,
                                                   description, gpu_cores, period_seconds, initial_delay_seconds,
                                                   timeout_seconds, success_threshold, failure_threshold, namespace,
                                                   token_auth_enabled)
        return config

    @staticmethod
    def _deploy(workspace, name, image, deployment_config, deployment_target, overwrite=False):
        """Deploy the Webservice.

        :param workspace:
        :type workspace: azureml.core.Workspace
        :param name:
        :type name: str
        :param image:
        :type image: azureml.core.Image
        :param deployment_config:
        :type deployment_config: AksServiceDeploymentConfiguration | None
        :param deployment_target:
        :type deployment_target: azureml.core.compute.AksCompute
        :param overwrite:
        :type overwrite: bool
        :return:
        :rtype: AksWebservice
        """
        if not deployment_target:
            raise WebserviceException("Must have a deployment target for an AKS web service.", logger=module_logger)
        if not deployment_config:
            deployment_config = AksWebservice.deploy_configuration()
        elif not isinstance(deployment_config, AksServiceDeploymentConfiguration):
            raise WebserviceException('Error, provided deployment configuration must be of type '
                                      'AksServiceDeploymentConfiguration in order to deploy an AKS service.',
                                      logger=module_logger)
        deployment_config.validate_image(image)
        create_payload = AksWebservice._build_create_payload(name, image, deployment_target, deployment_config,
                                                             overwrite)
        return Webservice._deploy_webservice(workspace, name, create_payload, AksWebservice)

    @staticmethod
    def _build_create_payload(name, image, target, config, overwrite):
        """Construct the payload used to create this Webservice.

        :param name:
        :type name: str
        :param image:
        :type image: azureml.core.Image
        :param target:
        :type target: azureml.core.compute.AksCompute
        :param config:
        :type config: azureml.core.compute.AksServiceDeploymentConfiguration
        :return:
        :rtype: dict
        """
        from azureml._model_management._util import aks_service_payload_template
        json_payload = copy.deepcopy(aks_service_payload_template)
        json_payload['name'] = name
        json_payload['computeType'] = 'AKS'
        json_payload['computeName'] = target.name
        json_payload['imageId'] = image.id

        properties = config.properties or {}
        properties.update(global_tracking_info_registry.gather_all())
        json_payload['properties'] = properties

        if config.description:
            json_payload['description'] = config.description
        else:
            del (json_payload['description'])
        if config.tags:
            json_payload['kvTags'] = config.tags
        if config.num_replicas:
            json_payload['numReplicas'] = config.num_replicas
        else:
            del (json_payload['numReplicas'])
        if config.collect_model_data is None:
            del (json_payload['dataCollection'])
        else:
            json_payload['dataCollection']['storageEnabled'] = config.collect_model_data
        if config.enable_app_insights is None:
            del (json_payload['appInsightsEnabled'])
        else:
            json_payload['appInsightsEnabled'] = config.enable_app_insights
        if not config.autoscale_enabled:
            del (json_payload['autoScaler'])
        else:
            json_payload['autoScaler']['autoscaleEnabled'] = config.autoscale_enabled
            json_payload['autoScaler']['minReplicas'] = config.autoscale_min_replicas
            json_payload['autoScaler']['maxReplicas'] = config.autoscale_max_replicas
            json_payload['autoScaler']['targetUtilization'] = config.autoscale_target_utilization
            json_payload['autoScaler']['refreshPeriodInSeconds'] = config.autoscale_refresh_seconds
            if 'numReplicas' in json_payload:
                del (json_payload['numReplicas'])
        if config.auth_enabled is None:
            del (json_payload['authEnabled'])
        else:
            json_payload['authEnabled'] = config.auth_enabled
        if config.token_auth_enabled is None:
            del json_payload['aadAuthEnabled']
        else:
            json_payload['aadAuthEnabled'] = config.token_auth_enabled
        if config.cpu_cores or config.memory_gb or config.gpu_cores:
            if config.cpu_cores:
                json_payload['containerResourceRequirements']['cpu'] = config.cpu_cores
            else:
                del (json_payload['containerResourceRequirements']['cpu'])
            if config.memory_gb:
                json_payload['containerResourceRequirements']['memoryInGB'] = config.memory_gb
            else:
                del (json_payload['containerResourceRequirements']['memoryInGB'])
            if config.gpu_cores:
                json_payload['containerResourceRequirements']['gpu'] = config.gpu_cores
            else:
                del (json_payload['containerResourceRequirements']['gpu'])
        else:
            del (json_payload['containerResourceRequirements'])

        if config.period_seconds or config.initial_delay_seconds or config.timeout_seconds \
                or config.failure_threshold or config.success_threshold:
            if config.period_seconds:
                json_payload['livenessProbeRequirements']['periodSeconds'] = config.period_seconds
            else:
                del (json_payload['livenessProbeRequirements']['periodSeconds'])
            if config.initial_delay_seconds:
                json_payload['livenessProbeRequirements']['initialDelaySeconds'] = config.initial_delay_seconds
            else:
                del (json_payload['livenessProbeRequirements']['initialDelaySeconds'])
            if config.timeout_seconds:
                json_payload['livenessProbeRequirements']['timeoutSeconds'] = config.timeout_seconds
            else:
                del (json_payload['livenessProbeRequirements']['timeoutSeconds'])
            if config.failure_threshold:
                json_payload['livenessProbeRequirements']['failureThreshold'] = config.failure_threshold
            else:
                del (json_payload['livenessProbeRequirements']['failureThreshold'])
            if config.success_threshold:
                json_payload['livenessProbeRequirements']['successThreshold'] = config.success_threshold
            else:
                del (json_payload['livenessProbeRequirements']['successThreshold'])
        else:
            del (json_payload['livenessProbeRequirements'])

        json_payload['maxConcurrentRequestsPerContainer'] = config.replica_max_concurrent_requests
        if config.max_request_wait_time:
            json_payload['maxQueueWaitMs'] = config.max_request_wait_time
        else:
            del (json_payload['maxQueueWaitMs'])
        if config.namespace:
            json_payload['namespace'] = config.namespace
        else:
            del (json_payload['namespace'])
        if config.primary_key:
            json_payload['keys']['primaryKey'] = config.primary_key
            json_payload['keys']['secondaryKey'] = config.secondary_key
        else:
            del (json_payload['keys'])
        if config.scoring_timeout_ms:
            json_payload['scoringTimeoutMs'] = config.scoring_timeout_ms
        else:
            del (json_payload['scoringTimeoutMs'])

        if overwrite:
            json_payload['overwrite'] = overwrite
        else:
            del (json_payload['overwrite'])
        return json_payload

    def run(self, input_data):
        """Call this Webservice with the provided input.

        :param input_data: The input to call the Webservice with
        :type input_data: varies
        :return: The result of calling the Webservice
        :rtype: dict
        :raises: azureml.exceptions.WebserviceException
        """
        if not self.scoring_uri:
            raise WebserviceException('Error attempting to call webservice, scoring_uri unavailable. '
                                      'This could be due to a failed deployment, or the service is not ready yet.\n'
                                      'Current State: {}\n'
                                      'Errors: {}'.format(self.state, self.error), logger=module_logger)

        resp = ClientBase._execute_func(self._webservice_session.post, self.scoring_uri, data=input_data)

        if resp.status_code == 401:
            if self.auth_enabled:
                service_keys = self.get_keys()
                self._session.headers.update({'Authorization': 'Bearer ' + service_keys[0]})
            elif self.token_auth_enabled:
                service_token, refresh_token_time = self.get_token()
                self._refresh_token_time = refresh_token_time
                self._session.headers.update({'Authorization': 'Bearer ' + service_token})
            resp = ClientBase._execute_func(self._webservice_session.post, self.scoring_uri, data=input_data)

        if resp.status_code == 200:
            return resp.json()
        else:
            raise WebserviceException('Received bad response from service. More information can be found by calling '
                                      '`.get_logs()` on the webservice object.\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content),
                                      logger=module_logger)

    def update(self, image=None, autoscale_enabled=None, autoscale_min_replicas=None, autoscale_max_replicas=None,
               autoscale_refresh_seconds=None, autoscale_target_utilization=None, collect_model_data=None,
               auth_enabled=None, cpu_cores=None, memory_gb=None, enable_app_insights=None, scoring_timeout_ms=None,
               replica_max_concurrent_requests=None, max_request_wait_time=None, num_replicas=None, tags=None,
               properties=None, description=None, models=None, inference_config=None, gpu_cores=None,
               period_seconds=None, initial_delay_seconds=None, timeout_seconds=None, success_threshold=None,
               failure_threshold=None, namespace=None, token_auth_enabled=None):
        """Update the Webservice with provided properties.

        Values left as None will remain unchanged in this Webservice.

        :param image: A new Image to deploy to the Webservice
        :type image: azureml.core.Image
        :param autoscale_enabled: Enable or disable autoscaling of this Webservice
        :type autoscale_enabled: bool
        :param autoscale_min_replicas: The minimum number of containers to use when autoscaling this Webservice
        :type autoscale_min_replicas: int
        :param autoscale_max_replicas: The maximum number of containers to use when autoscaling this Webservice
        :type autoscale_max_replicas: int
        :param autoscale_refresh_seconds: How often the autoscaler should attempt to scale this Webservice
        :type autoscale_refresh_seconds: int
        :param autoscale_target_utilization: The target utilization (in percent out of 100) the autoscaler should
            attempt to maintain for this Webservice
        :type autoscale_target_utilization: int
        :param collect_model_data: Enable or disable model data collection for this Webservice
        :type collect_model_data: bool
        :param auth_enabled: Whether or not to enable auth for this Webservice
        :type auth_enabled: bool
        :param cpu_cores: The number of cpu cores to allocate for this Webservice. Can be a decimal
        :type cpu_cores: float
        :param memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal
        :type memory_gb: float
        :param enable_app_insights: Whether or not to enable Application Insights logging for this Webservice
        :type enable_app_insights: bool
        :param scoring_timeout_ms: A timeout to enforce for scoring calls to this Webservice
        :type scoring_timeout_ms: int
        :param replica_max_concurrent_requests: The number of maximum concurrent requests per node to allow for this
            Webservice
        :type replica_max_concurrent_requests: int
        :param max_request_wait_time: The maximum amount of time a request will stay in the queue (in milliseconds)
            before returning a 503 error
        :type max_request_wait_time: int
        :param num_replicas: The number of containers to allocate for this Webservice
        :type num_replicas: int
        :param tags: Dictionary of key value tags to give this Webservice. Will replace existing tags.
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to add to existing properties dictionary
        :type properties: dict[str, str]
        :param description: A description to give this Webservice
        :type description: str
        :param models: A list of Model objects to package with the updated service
        :type models: :class:`list[azureml.core.Model]`
        :param inference_config: An InferenceConfig object used to provide the required model deployment properties.
        :type inference_config: azureml.core.model.InferenceConfig
        :param gpu_cores: The number of gpu cores to allocate for this Webservice
        :type gpu_cores: int
        :param period_seconds: How often (in seconds) to perform the liveness probe. Default to 10 seconds.
            Minimum value is 1.
        :type period_seconds: int
        :param initial_delay_seconds: Number of seconds after the container has started before liveness probes are
            initiated.
        :type initial_delay_seconds: int
        :param timeout_seconds: Number of seconds after which the liveness probe times out. Defaults to 1 second.
            Minimum value is 1.
        :type timeout_seconds: int
        :param success_threshold: Minimum consecutive successes for the liveness probe to be considered successful
            after having failed. Defaults to 1. Minimum value is 1.
        :type success_threshold: int
        :param failure_threshold: When a Pod starts and the liveness probe fails, Kubernetes will try failureThreshold
            times before giving up. Defaults to 3. Minimum value is 1.
        :type failure_threshold: int
        :param namespace: The Kubernetes namespace in which to deploy this Webservice: up to 63 lowercase alphanumeric
            ('a'-'z', '0'-'9') and hyphen ('-') characters. The first and last characters cannot be hyphens.
        :type namespace: str
        :param token_auth_enabled: Whether or not to enable Token auth for this Webservice. If this is
            enabled, users can access this Webservice by fetching access token using their Azure Active Directory
            credentials. Defaults to False
        :type token_auth_enabled: bool
        :raises: azureml.exceptions.WebserviceException
        """
        if not image and autoscale_enabled is None and not autoscale_min_replicas and not autoscale_max_replicas \
                and not autoscale_refresh_seconds and not autoscale_target_utilization and collect_model_data is None \
                and auth_enabled is None and not cpu_cores and not memory_gb and not gpu_cores \
                and enable_app_insights is None and not scoring_timeout_ms and not replica_max_concurrent_requests \
                and not max_request_wait_time and not num_replicas and tags is None and properties is None \
                and not description and not period_seconds and not initial_delay_seconds and not timeout_seconds \
                and models is None and inference_config is None and not failure_threshold and not success_threshold \
                and not namespace and token_auth_enabled is None:
            raise WebserviceException('No parameters provided to update.', logger=module_logger)

        headers = {'Content-Type': 'application/json-patch+json'}
        headers.update(self._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        self._validate_update(image, autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                              autoscale_refresh_seconds, autoscale_target_utilization, collect_model_data, cpu_cores,
                              memory_gb, enable_app_insights, scoring_timeout_ms, replica_max_concurrent_requests,
                              max_request_wait_time, num_replicas, tags, properties, description, models,
                              inference_config, gpu_cores, period_seconds, initial_delay_seconds, timeout_seconds,
                              success_threshold, failure_threshold, namespace, auth_enabled, token_auth_enabled)

        patch_list = []

        if inference_config:
            if not models:
                models = self.image.models if self.image else self.models

            if self.environment:  # Use the new environment handling
                inference_config, _ = convert_parts_to_environment(self.name, inference_config)

                environment_image_request = \
                    inference_config._build_environment_image_request(self.workspace, [model.id for model in models])
                patch_list.append({'op': 'replace', 'path': '/environmentImageRequest',
                                   'value': environment_image_request})
            else:  # Use the old image handling
                image = Image.create(self.workspace, self.name, models, inference_config)
                image.wait_for_creation(True)
                if image.creation_state != 'Succeeded':
                    raise WebserviceException('Error occurred creating model package {} for service update. More '
                                              'information can be found here: {}, generated DockerFile can be '
                                              'found here: {}'.format(image.id,
                                                                      image.image_build_log_uri,
                                                                      image.generated_dockerfile_uri),
                                              logger=module_logger)
        elif models is not None:
            # No-code deploy.
            environment_image_request = build_and_validate_no_code_environment_image_request(models)
            patch_list.append({'op': 'replace', 'path': '/environmentImageRequest',
                               'value': environment_image_request})

        properties = properties or {}
        properties.update(global_tracking_info_registry.gather_all())

        if image:
            patch_list.append({'op': 'replace', 'path': '/imageId', 'value': image.id})
        if autoscale_enabled is not None:
            patch_list.append({'op': 'replace', 'path': '/autoScaler/autoscaleEnabled', 'value': autoscale_enabled})
        if autoscale_min_replicas:
            patch_list.append({'op': 'replace', 'path': '/autoScaler/minReplicas', 'value': autoscale_min_replicas})
        if autoscale_max_replicas:
            patch_list.append({'op': 'replace', 'path': '/autoScaler/maxReplicas', 'value': autoscale_max_replicas})
        if autoscale_refresh_seconds:
            patch_list.append({'op': 'replace', 'path': '/autoScaler/refreshPeriodInSeconds',
                               'value': autoscale_refresh_seconds})
        if autoscale_target_utilization:
            patch_list.append({'op': 'replace', 'path': '/autoScaler/targetUtilization',
                               'value': autoscale_target_utilization})
        if collect_model_data is not None:
            patch_list.append({'op': 'replace', 'path': '/dataCollection/storageEnabled', 'value': collect_model_data})

        if auth_enabled is not None:
            patch_list.append({'op': 'replace', 'path': '/authEnabled', 'value': auth_enabled})
        if token_auth_enabled is not None:
            patch_list.append({'op': 'replace', 'path': '/aadAuthEnabled', 'value': token_auth_enabled})

        if cpu_cores:
            patch_list.append({'op': 'replace', 'path': '/containerResourceRequirements/cpu', 'value': cpu_cores})
        if memory_gb:
            patch_list.append({'op': 'replace', 'path': '/containerResourceRequirements/memoryInGB',
                               'value': memory_gb})
        if gpu_cores:
            patch_list.append({'op': 'replace', 'path': '/containerResourceRequirements/gpu', 'value': gpu_cores})
        if enable_app_insights is not None:
            patch_list.append({'op': 'replace', 'path': '/appInsightsEnabled', 'value': enable_app_insights})
        if scoring_timeout_ms:
            patch_list.append({'op': 'replace', 'path': '/scoringTimeoutMs', 'value': scoring_timeout_ms})
        if replica_max_concurrent_requests:
            patch_list.append({'op': 'replace', 'path': '/maxConcurrentRequestsPerContainer',
                               'value': replica_max_concurrent_requests})
        if max_request_wait_time:
            patch_list.append({'op': 'replace', 'path': '/maxQueueWaitMs',
                               'value': max_request_wait_time})
        if num_replicas:
            patch_list.append({'op': 'replace', 'path': '/numReplicas', 'value': num_replicas})
        if period_seconds:
            patch_list.append({'op': 'replace', 'path': '/livenessProbeRequirements/periodSeconds',
                               'value': period_seconds})
        if initial_delay_seconds:
            patch_list.append({'op': 'replace', 'path': '/livenessProbeRequirements/initialDelaySeconds',
                               'value': initial_delay_seconds})
        if timeout_seconds:
            patch_list.append({'op': 'replace', 'path': '/livenessProbeRequirements/timeoutSeconds',
                               'value': timeout_seconds})
        if success_threshold:
            patch_list.append({'op': 'replace', 'path': '/livenessProbeRequirements/successThreshold',
                               'value': success_threshold})
        if failure_threshold:
            patch_list.append({'op': 'replace', 'path': '/livenessProbeRequirements/failureThreshold',
                               'value': failure_threshold})
        if namespace:
            patch_list.append({'op': 'replace', 'path': '/namespace', 'value': namespace})
        if tags is not None:
            patch_list.append({'op': 'replace', 'path': '/kvTags', 'value': tags})
        if properties is not None:
            for key in properties:
                patch_list.append({'op': 'add', 'path': '/properties/{}'.format(key), 'value': properties[key]})
        if description:
            patch_list.append({'op': 'replace', 'path': '/description', 'value': description})

        resp = ClientBase._execute_func(get_requests_session().patch, self._mms_endpoint, headers=headers,
                                        params=params, json=patch_list)

        if resp.status_code == 200:
            self.update_deployment_state()
        elif resp.status_code == 202:
            if 'Operation-Location' in resp.headers:
                operation_location = resp.headers['Operation-Location']
            else:
                raise WebserviceException('Missing response header key: Operation-Location', logger=module_logger)
            create_operation_status_id = operation_location.split('/')[-1]
            base_url = '/'.join(self._mms_endpoint.split('/')[:-2])
            operation_url = base_url + '/operations/{}'.format(create_operation_status_id)
            self._operation_endpoint = operation_url
            self.update_deployment_state()
        else:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content),
                                      logger=module_logger)

    def _validate_update(self, image, autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                         autoscale_refresh_seconds, autoscale_target_utilization, collect_model_data, cpu_cores,
                         memory_gb, enable_app_insights, scoring_timeout_ms, replica_max_concurrent_requests,
                         max_request_wait_time, num_replicas, tags, properties, description, models,
                         inference_config, gpu_cores, period_seconds, initial_delay_seconds, timeout_seconds,
                         success_threshold, failure_threshold, namespace, auth_enabled, token_auth_enabled):
        """Validate the values provided to update the webservice.

        :param image:
        :type image: azureml.core.Image
        :param autoscale_enabled:
        :type autoscale_enabled: bool
        :param autoscale_min_replicas:
        :type autoscale_min_replicas: int
        :param autoscale_max_replicas:
        :type autoscale_max_replicas: int
        :param autoscale_refresh_seconds:
        :type autoscale_refresh_seconds: int
        :param autoscale_target_utilization:
        :type autoscale_target_utilization: int
        :param collect_model_data:
        :type collect_model_data: bool
        :param cpu_cores:
        :type cpu_cores: float
        :param memory_gb:
        :type memory_gb: float
        :param enable_app_insights:
        :type enable_app_insights: bool
        :param scoring_timeout_ms:
        :type scoring_timeout_ms: int
        :param replica_max_concurrent_requests:
        :type replica_max_concurrent_requests: int
        :param max_request_wait_time: The maximum amount of time a request will stay in the queue (in milliseconds)
            before returning a 503 error
        :type max_request_wait_time: int
        :param num_replicas:
        :type num_replicas: int
        :param tags:
        :type tags: dict[str, str]
        :param properties:
        :type properties: dict[str, str]
        :param description:
        :type description: str
        :param models: A list of Model objects to package with this image. Can be an empty list
        :type models: :class:`list[azureml.core.Model]`
        :param inference_config: An InferenceConfig object used to determine required model properties.
        :type inference_config: azureml.core.model.InferenceConfig
        :param: gpu_cores
        :type: int
        :param period_seconds:
        :type period_seconds: int
        :param initial_delay_seconds:
        :type initial_delay_seconds: int
        :param timeout_seconds:
        :type timeout_seconds: int
        :param success_threshold:
        :type success_threshold: int
        :param failure_threshold:
        :type failure_threshold: int
        :param namespace:
        :type namespace: str
        :param auth_enabled: If Key auth is enabled.
        :type auth_enabled: bool
        :param token_auth_enabled: Whether or not to enable Token auth for this Webservice. If this is
            enabled, users can access this Webservice by fetching access token using their Azure Active Directory
            credentials. Defaults to False
        :type token_auth_enabled: bool
        """
        error = ""
        if image and self.environment:
            error += 'Error, unable to use Image object to update Webservice created with Environment object.\n'
        if inference_config and inference_config.environment and self.image:
            error += 'Error, unable to use Environment object to update Webservice created with Image object.\n'
        if image and inference_config:
            error += 'Error, unable to pass both an Image object and an InferenceConfig object to update.\n'
        if cpu_cores and cpu_cores <= 0:
            error += 'Error, cpu_cores must be greater than zero.\n'
        if memory_gb and memory_gb <= 0:
            error += 'Error, memory_gb must be greater than zero.\n'
        if gpu_cores and gpu_cores <= 0:
            error += 'Error, gpu_cores must be greater than zero.\n'
        if scoring_timeout_ms and scoring_timeout_ms <= 0:
            error += 'Error, scoring_timeout_ms must be greater than zero.\n'
        if replica_max_concurrent_requests and replica_max_concurrent_requests <= 0:
            error += 'Error, replica_max_concurrent_requests must be greater than zero.\n'
        if max_request_wait_time and max_request_wait_time <= 0:
            error += 'Error, max_request_wait_time must be greater than zero.\n'
        if num_replicas and num_replicas <= 0:
            error += 'Error, num_replicas must be greater than zero.\n'
        if period_seconds and period_seconds <= 0:
            error += 'Error, period_seconds must be greater than zero.\n'
        if timeout_seconds and timeout_seconds <= 0:
            error += 'Error, timeout_seconds must be greater than zero.\n'
        if initial_delay_seconds and initial_delay_seconds <= 0:
            error += 'Error, initial_delay_seconds must be greater than zero.\n'
        if success_threshold and success_threshold <= 0:
            error += 'Error, success_threshold must be greater than zero.\n'
        if failure_threshold and failure_threshold <= 0:
            error += 'Error, failure_threshold must be greater than zero.\n'
        if namespace and not re.match(NAMESPACE_REGEX, namespace):
            error += 'Error, namespace must be a valid Kubernetes namespace. ' \
                     'Regex for validation is ' + NAMESPACE_REGEX + '\n'
        if autoscale_enabled:
            if num_replicas:
                error += 'Error, autoscale enabled and num_replicas provided.\n'
            if autoscale_min_replicas and autoscale_min_replicas <= 0:
                error += 'Error, autoscale_min_replicas must be greater than zero.\n'
            if autoscale_max_replicas and autoscale_max_replicas <= 0:
                error += 'Error, autoscale_max_replicas must be greater than zero.\n'
            if autoscale_min_replicas and autoscale_max_replicas and \
                    autoscale_min_replicas > autoscale_max_replicas:
                error += 'Error, autoscale_min_replicas cannot be greater than autoscale_max_replicas.\n'
            if autoscale_refresh_seconds and autoscale_refresh_seconds <= 0:
                error += 'Error, autoscale_refresh_seconds must be greater than zero.\n'
            if autoscale_target_utilization and autoscale_target_utilization <= 0:
                error += 'Error, autoscale_target_utilization must be greater than zero.\n'
        else:
            if autoscale_enabled is False and not num_replicas:
                error += 'Error, autoscale disabled but num_replicas not provided.\n'
            if autoscale_min_replicas:
                error += 'Error, autoscale_min_replicas provided without enabling autoscaling.\n'
            if autoscale_max_replicas:
                error += 'Error, autoscale_max_replicas provided without enabling autoscaling.\n'
            if autoscale_refresh_seconds:
                error += 'Error, autoscale_refresh_seconds provided without enabling autoscaling.\n'
            if autoscale_target_utilization:
                error += 'Error, autoscale_target_utilization provided without enabling autoscaling.\n'
        if inference_config is None and models and \
                (len(models) != 1 or models[0].model_framework not in Model._SUPPORTED_FRAMEWORKS_FOR_NO_CODE_DEPLOY):
            error += 'Error, both "models" and "inference_config" inputs must be provided in order ' \
                     'to update the models.\n'
        if token_auth_enabled and auth_enabled:
            error += 'Error, cannot set both token_auth_enabled and auth_enabled.\n'
        elif token_auth_enabled and (self.auth_enabled and auth_enabled is not False):
            error += 'Error, cannot set token_auth_enabled without disabling key auth (set auth_enabled to False).\n'
        elif auth_enabled and (self.token_auth_enabled and token_auth_enabled is not False):
            error += 'Error, cannot set token_auth_enabled without disabling key auth (set auth_enabled to False).\n'

        if error:
            raise WebserviceException(error, logger=module_logger)

    def add_tags(self, tags):
        """Add key value pairs to this Webservice's tags dictionary.

        :param tags: The dictionary of tags to add
        :type tags: dict[str, str]
        :raises: azureml.exceptions.WebserviceException
        """
        updated_tags = self._add_tags(tags)
        self.tags = updated_tags
        self.update(tags=updated_tags)

        print('Image tag add operation complete.')

    def remove_tags(self, tags):
        """Remove the specified keys from this Webservice's dictionary of tags.

        :param tags: The list of keys to remove
        :type tags: :class:`list[str]`
        """
        updated_tags = self._remove_tags(tags)
        self.tags = updated_tags
        self.update(tags=updated_tags)

        print('Image tag remove operation complete.')

    def add_properties(self, properties):
        """Add key value pairs to this Webservice's properties dictionary.

        :param properties: The dictionary of properties to add
        :type properties: dict[str, str]
        """
        updated_properties = self._add_properties(properties)
        self.properties = updated_properties
        self.update(tags=updated_properties)

        print('Image tag add operation complete.')

    def serialize(self):
        """Convert this Webservice into a json serialized dictionary.

        :return: The json representation of this Webservice
        :rtype: dict
        """
        properties = super(AksWebservice, self).serialize()
        autoscaler = self.autoscaler.serialize() if self.autoscaler else None
        container_resource_requirements = self.container_resource_requirements.serialize() \
            if self.container_resource_requirements else None
        liveness_probe_requirements = self.liveness_probe_requirements.serialize() \
            if self.liveness_probe_requirements else None
        data_collection = self.data_collection.serialize() if self.data_collection else None
        env_details = Environment._serialize_to_dict(self.environment) if self.environment else None
        model_details = [model.serialize() for model in self.models] if self.models else None
        aks_properties = {'appInsightsEnabled': self.enable_app_insights, 'authEnabled': self.auth_enabled,
                          'autoScaler': autoscaler, 'computeName': self.compute_name,
                          'containerResourceRequirements': container_resource_requirements,
                          'dataCollection': data_collection, 'imageId': self.image_id,
                          'maxConcurrentRequestsPerContainer': self.max_concurrent_requests_per_container,
                          'maxQueueWaitMs': self.max_request_wait_time,
                          'livenessProbeRequirements': liveness_probe_requirements,
                          'numReplicas': self.num_replicas, 'deploymentStatus': self.deployment_status,
                          'scoringTimeoutMs': self.scoring_timeout_ms, 'scoringUri': self.scoring_uri,
                          'aadAuthEnabled': self.token_auth_enabled, 'environmentDetails': env_details,
                          'modelDetails': model_details, 'isDefault': self.is_default,
                          'trafficPercentile': self.traffic_percentile, 'versionType': self.version_type}
        properties.update(aks_properties)
        return properties

    def get_token(self):
        """Retrieve auth token for this Webservice.

        :return: The auth token for this Webservice and when to refresh it.
        :rtype: str, datetime
        :raises: azureml.exceptions.WebserviceException
        """
        headers = self._auth.get_authentication_header()
        params = {'api-version': MMS_WORKSPACE_API_VERSION}
        token_url = self._mms_endpoint + '/token'

        try:
            resp = ClientBase._execute_func(get_requests_session().post, token_url,
                                            params=params, headers=headers)

            content = resp.content
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            auth_token_result = json.loads(content)
            if 'accessToken' not in auth_token_result:
                raise WebserviceException('Missing response key: accessToken', logger=module_logger)
            if 'refreshAfter' not in auth_token_result:
                raise WebserviceException('Missing response key: refreshAfter', logger=module_logger)
            return auth_token_result['accessToken'], datetime.fromtimestamp(auth_token_result['refreshAfter'])
        except requests.exceptions.HTTPError:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content),
                                      logger=module_logger)


class AksEndpoint(AksWebservice):
    """Class for Azure Kubernetes Service Endpoints."""

    class VersionType(Enum):
        """Class for to represent the version type in an Endpoints."""

        control = "Control"
        treatment = "Treatment"

    _expected_payload_keys = Webservice._expected_payload_keys + ['appInsightsEnabled', 'authEnabled', 'computeName',
                                                                  'scoringUri', 'aadAuthEnabled']
    _webservice_type = AKS_ENDPOINT_TYPE

    def _initialize(self, workspace, obj_dict):
        """Initialize the Endpoint instance.

        This is used because the constructor is used as a getter.

        :param workspace:
        :type workspace: azureml.core.Workspace
        :param obj_dict:
        :type obj_dict: dict
        :return:
        :rtype: None
        """
        # Validate obj_dict with _expected_payload_keys
        AksEndpoint._validate_get_payload(obj_dict)

        # Initialize common Webservice attributes
        self.auth_enabled = obj_dict.get('authEnabled')
        self.compute_type = obj_dict.get('computeType')
        self.created_time = parse(obj_dict.get('createdTime'))
        self.description = obj_dict.get('description')
        self.tags = obj_dict.get('kvTags')
        self.name = obj_dict.get('name')
        self.properties = obj_dict.get('properties')

        # Common amongst Webservice classes but optional payload keys
        self.error = obj_dict.get('error')
        self.state = obj_dict.get('state')
        self.updated_time = parse(obj_dict['updatedTime']) if 'updatedTime' in obj_dict else None

        # Utility payload keys
        self._auth = workspace._auth
        self._mms_endpoint = _get_mms_url(workspace) + '/services/{}'.format(self.name)
        self._operation_endpoint = None
        self.workspace = workspace
        self._session = None
        self.image = None

        # Initialize expected AksEndpoint specific attributes
        self.enable_app_insights = obj_dict.get('appInsightsEnabled')
        self.compute_name = obj_dict.get('computeName')
        self.scoring_uri = obj_dict.get('scoringUri')
        self.token_auth_enabled = obj_dict.get('aadAuthEnabled')
        version_payloads = obj_dict.get('versions', {})
        self.versions = {}

        if version_payloads is not None:
            for version_name in version_payloads:
                version = super(Webservice, self).__new__(AksWebservice)
                version._initialize(workspace, version_payloads[version_name])
                self.versions[version_name] = version

        # Initialize other AKS utility attributes
        self.deployment_status = obj_dict.get('deploymentStatus')
        self.namespace = obj_dict.get('namespace')
        self.swagger_uri = '/'.join(self.scoring_uri.split('/')[:-1]) + WEBSERVICE_SWAGGER_PATH \
            if self.scoring_uri else None
        self._refresh_token_time = None

    @staticmethod
    def deploy_configuration(autoscale_enabled=None, autoscale_min_replicas=None, autoscale_max_replicas=None,
                             autoscale_refresh_seconds=None, autoscale_target_utilization=None,
                             collect_model_data=None, auth_enabled=None, cpu_cores=None, memory_gb=None,
                             enable_app_insights=None, scoring_timeout_ms=None, replica_max_concurrent_requests=None,
                             max_request_wait_time=None, num_replicas=None, primary_key=None, secondary_key=None,
                             tags=None, properties=None, description=None, gpu_cores=None, period_seconds=None,
                             initial_delay_seconds=None, timeout_seconds=None, success_threshold=None,
                             failure_threshold=None, namespace=None, token_auth_enabled=None, version_name=None,
                             traffic_percentile=None):
        """Create a configuration object for deploying to an AKS compute target.

        :param autoscale_enabled: Whether or not to enable autoscaling for this version in an Endpoint.
            Defaults to True if num_replicas is None
        :type autoscale_enabled: bool
        :param autoscale_min_replicas: The minimum number of containers to use when autoscaling this version in an
            Endpoint. Defaults to 1
        :type autoscale_min_replicas: int
        :param autoscale_max_replicas: The maximum number of containers to use when autoscaling this version in an
            Endpoint. Defaults to 10
        :type autoscale_max_replicas: int
        :param autoscale_refresh_seconds: How often the autoscaler should attempt to scale this version in an Endpoint.
            Defaults to 1
        :type autoscale_refresh_seconds: int
        :param autoscale_target_utilization: The target utilization (in percent out of 100) the autoscaler should
            attempt to maintain for this version in an Endpoint. Defaults to 70
        :type autoscale_target_utilization: int
        :param collect_model_data: Whether or not to enable model data collection for this version in an Endpoint.
            Defaults to False
        :type collect_model_data: bool
        :param auth_enabled: Whether or not to enable key auth for this version in an Endpoint. Defaults to True
        :type auth_enabled: bool
        :param cpu_cores: The number of cpu cores to allocate for this version in an Endpoint. Can be a decimal.
            Defaults to 0.1
        :type cpu_cores: float
        :param memory_gb: The amount of memory (in GB) to allocate for this version in an Endpoint. Can be a decimal.
            Defaults to 0.5
        :type memory_gb: float
        :param enable_app_insights: Whether or not to enable ApplicationInsights logging for this version in an
            Endpoint. Defaults to False
        :type enable_app_insights: bool
        :param scoring_timeout_ms: A timeout to enforce scoring calls to this version in an Endpoint. Defaults to 60000
        :type scoring_timeout_ms: int
        :param replica_max_concurrent_requests: The number of maximum concurrent requests per node to allow for this
            version in an Endpoint. Defaults to 1
        :type replica_max_concurrent_requests: int
        :param max_request_wait_time: The maximum amount of time a request will stay in the queue (in milliseconds)
            before returning a 503 error. Defaults to 500
        :type max_request_wait_time: int
        :param num_replicas: The number of containers to allocate for this version in an Endpoint. No default, if this
            parameter is not set then the autoscaler is enabled by default.
        :type num_replicas: int
        :param primary_key: A primary auth key to use for this Endpoint
        :type primary_key: str
        :param secondary_key: A secondary auth key to use for this Endpoint
        :type secondary_key: str
        :param tags: Dictionary of key value tags to give this Endpoint
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to give this Endpoint. These properties cannot
            be changed after deployment, however new key value pairs can be added
        :type properties: dict[str, str]
        :param description: A description to give this Endpoint
        :type description: str
        :param gpu_cores: The number of gpu cores to allocate for this version in an Endpoint. Default is 1
        :type gpu_cores: int
        :param period_seconds: How often (in seconds) to perform the liveness probe. Default to 10 seconds.
            Minimum value is 1.
        :type period_seconds: int
        :param initial_delay_seconds: Number of seconds after the container has started before liveness probes are
            initiated. Defaults to 310
        :type initial_delay_seconds: int
        :param timeout_seconds: Number of seconds after which the liveness probe times out. Defaults to 2 second.
            Minimum value is 1
        :type timeout_seconds: int
        :param success_threshold: Minimum consecutive successes for the liveness probe to be considered successful
            after having failed. Defaults to 1. Minimum value is 1.
        :type success_threshold: int
        :param failure_threshold: When a Pod starts and the liveness probe fails, Kubernetes will try failureThreshold
            times before giving up. Defaults to 3. Minimum value is 1.
        :type failure_threshold: int deploying a version in an Endpoint object
        :param namespace: The Kubernetes namespace in which to deploy this Endpoint: up to 63 lowercase alphanumeric
            ('a'-'z', '0'-'9') and hyphen ('-') characters. The first and last characters cannot be hyphens.
        :type namespace: str
        :param token_auth_enabled: Whether or not to enable Token auth for this Endpoint. If this is
            enabled, users can access this Endpoint by fetching access token using their Azure Active Directory
            credentials. Defaults to False
        :type token_auth_enabled: bool
        :param version_name: The name of the version in an endpoint.
        :type version_name: str
        :param traffic_percentile: the amount of traffic the version takes in an endpoint.
        :type traffic_percentile: float
        :rtype: AksEndpointDeploymentConfiguration
        :raises: azureml.exceptions.WebserviceException
        """
        config = AksEndpointDeploymentConfiguration(autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                                                    autoscale_refresh_seconds, autoscale_target_utilization,
                                                    collect_model_data, auth_enabled, cpu_cores, memory_gb,
                                                    enable_app_insights, scoring_timeout_ms,
                                                    replica_max_concurrent_requests, max_request_wait_time,
                                                    num_replicas, primary_key, secondary_key, tags, properties,
                                                    description, gpu_cores, period_seconds, initial_delay_seconds,
                                                    timeout_seconds, success_threshold, failure_threshold, namespace,
                                                    token_auth_enabled, version_name, traffic_percentile)
        return config

    def update(self, auth_enabled=None, token_auth_enabled=None, enable_app_insights=None, description=None, tags=None,
               properties=None):
        """Update the Endpoint with provided properties.

        Values left as None will remain unchanged in this Endpoint

        :param auth_enabled: Whether or not to enable key auth for this version in an Endpoint. Defaults to True
        :type auth_enabled: bool
        :param token_auth_enabled: Whether or not to enable Token auth for this Endpoint. If this is
            enabled, users can access this Endpoint by fetching access token using their Azure Active Directory
            credentials. Defaults to False
        :type token_auth_enabled: bool
        :param enable_app_insights: Whether or not to enable Application Insights logging for this version in an
            Endpoint. Defaults to False
        :type enable_app_insights: bool
        :param description: A description to give this Endpoint
        :type description: str
        :param tags: Dictionary of key value tags to give this Endpoint
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to give this Endpoint. These properties cannot
            be changed after deployment, however new key value pairs can be added
        :type properties: dict[str, str]
        :raises: azureml.exceptions.WebserviceException
        """
        if auth_enabled is None and enable_app_insights is None and tags is None and properties is None \
                and not description and token_auth_enabled is None:
            raise WebserviceException('No parameters provided to update.', logger=module_logger)

        self._validate_update(None, None, None, None, None, None, None, None, enable_app_insights, None, None,
                              None, None, tags, properties, description, None, None, None, None, None, None,
                              None, None, None, auth_enabled, token_auth_enabled, None, None)

        patch_list = []
        properties = properties or {}
        properties.update(global_tracking_info_registry.gather_all())
        headers = {'Content-Type': 'application/json-patch+json'}
        headers.update(self._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        if auth_enabled is not None:
            patch_list.append({'op': 'replace', 'path': '/authEnabled', 'value': auth_enabled})
        if token_auth_enabled is not None:
            patch_list.append({'op': 'replace', 'path': '/aadAuthEnabled', 'value': token_auth_enabled})
        if enable_app_insights is not None:
            patch_list.append({'op': 'replace', 'path': '/appInsightsEnabled', 'value': enable_app_insights})
        if tags is not None:
            patch_list.append({'op': 'replace', 'path': '/kvTags', 'value': tags})
        if properties is not None:
            for key in properties:
                patch_list.append({'op': 'add', 'path': '/properties/{}'.format(key), 'value': properties[key]})
        if description:
            patch_list.append({'op': 'replace', 'path': '/description', 'value': description})

        self._patch_endpoint_call(headers, params, patch_list)

    def delete_version(self, version_name):
        """Delete a version in an Endpoint.

        :param version_name: The name of the version in an endpoint to delete.
        :type version_name: str
        :raises: azureml.exceptions.WebserviceException
        """
        if version_name is None:
            raise WebserviceException('No name is provided to delete a version in an Endpoint {}'.format(self.name),
                                      logger=module_logger)

        patch_list = []
        headers = {'Content-Type': 'application/json-patch+json'}
        headers.update(self._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}
        patch_list.append({'op': 'remove', 'path': '/versions/{}'.format(version_name)})
        self._patch_endpoint_call(headers, params, patch_list)

    def create_version(self, version_name, autoscale_enabled=None, autoscale_min_replicas=None,
                       autoscale_max_replicas=None, autoscale_refresh_seconds=None, autoscale_target_utilization=None,
                       collect_model_data=None, cpu_cores=None, memory_gb=None, scoring_timeout_ms=None,
                       replica_max_concurrent_requests=None, max_request_wait_time=None, num_replicas=None, tags=None,
                       properties=None, description=None, models=None, inference_config=None, gpu_cores=None,
                       period_seconds=None, initial_delay_seconds=None, timeout_seconds=None, success_threshold=None,
                       failure_threshold=None, traffic_percentile=None, is_default=None, is_control_version_type=None):
        """Add a new version in an Endpoint with provided properties.

        :param version_name: The name of the version in an endpoint.
        :type version_name: str
        :param autoscale_enabled: Whether or not to enable autoscaling for this version in an Endpoint.
            Defaults to True if num_replicas is None
        :type autoscale_enabled: bool
        :param autoscale_min_replicas: The minimum number of containers to use when autoscaling this version in an
            Endpoint. Defaults to 1
        :type autoscale_min_replicas: int
        :param autoscale_max_replicas: The maximum number of containers to use when autoscaling this version in an
            Endpoint. Defaults to 10
        :type autoscale_max_replicas: int
        :param autoscale_refresh_seconds: How often the autoscaler should attempt to scale this version in an Endpoint.
            Defaults to 1
        :type autoscale_refresh_seconds: int
        :param autoscale_target_utilization: The target utilization (in percent out of 100) the autoscaler should
            attempt to maintain for this version in an Endpoint. Defaults to 70
        :type autoscale_target_utilization: int
        :param collect_model_data: Whether or not to enable model data collection for this version in an Endpoint.
            Defaults to False
        :type collect_model_data: bool
        :param cpu_cores: The number of cpu cores to allocate for this version in an Endpoint. Can be a decimal.
            Defaults to 0.1
        :type cpu_cores: float
        :param memory_gb: The amount of memory (in GB) to allocate for this version in an Endpoint. Can be a decimal.
            Defaults to 0.5
        :type memory_gb: float
        :param scoring_timeout_ms: A timeout to enforce for scoring calls to this version in an Endpoint.
            Defaults to 60000
        :type scoring_timeout_ms: int
        :param replica_max_concurrent_requests: The number of maximum concurrent requests per node to allow for this
            version in an Endpoint. Defaults to 1
        :type replica_max_concurrent_requests: int
        :param max_request_wait_time: The maximum amount of time a request will stay in the queue (in milliseconds)
            before returning a 503 error. Defaults to 500
        :type max_request_wait_time: int
        :param num_replicas: The number of containers to allocate for this version in an Endpoint. No default, if this
            parameter is not set then the autoscaler is enabled by default.
        :type num_replicas: int
        :param tags: Dictionary of key value tags to give this Endpoint
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to give this Endpoint. These properties cannot
            be changed after deployment, however new key value pairs can be added
        :type properties: dict[str, str]
        :param description: A description to give this Endpoint
        :type description: str
        :param models: A list of Model objects to package with the updated service
        :type models: :class:`list[azureml.core.Model]`
        :param inference_config: An InferenceConfig object used to provide the required model deployment properties.
        :type inference_config: azureml.core.model.InferenceConfig
        :param gpu_cores: The number of gpu cores to allocate for this version in an Endpoint. Default is 1
        :type gpu_cores: int
        :param period_seconds: How often (in seconds) to perform the liveness probe. Default to 10 seconds.
            Minimum value is 1.
        :type period_seconds: int
        :param initial_delay_seconds: Number of seconds after the container has started before liveness probes are
            initiated. Defaults to 310
        :type initial_delay_seconds: int
        :param timeout_seconds: Number of seconds after which the liveness probe times out. Defaults to 2 second.
            Minimum value is 1
        :type timeout_seconds: int
        :param success_threshold: Minimum consecutive successes for the liveness probe to be considered successful
            after having failed. Defaults to 1. Minimum value is 1.
        :type success_threshold: int
        :param failure_threshold: When a Pod starts and the liveness probe fails, Kubernetes will try failureThreshold
            times before giving up. Defaults to 3. Minimum value is 1.
        :type failure_threshold: int deploying a version in an Endpoint object
        :param traffic_percentile: the amount of traffic the version takes in an endpoint.
        :type traffic_percentile: float
        :param is_default: Whether or not to make this version as default version in an Endpoint.
            Defaults to False
        :type is_default: bool
        :param is_control_version_type: Whether or not to make this version as control version in an Endpoint.
            Defaults to False
        :type is_control_version_type: bool
        :raises: azureml.exceptions.WebserviceException
        """
        if version_name is None:
            raise WebserviceException('No name is provided to create a version in an Endpoint {}'.format(self.name),
                                      logger=module_logger)

        self._validate_update(autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                              autoscale_refresh_seconds, autoscale_target_utilization, collect_model_data, cpu_cores,
                              memory_gb, None, scoring_timeout_ms, replica_max_concurrent_requests,
                              max_request_wait_time, num_replicas, tags, properties, description, models,
                              inference_config, gpu_cores, period_seconds, initial_delay_seconds, timeout_seconds,
                              success_threshold, failure_threshold, None, None, None,
                              version_name, traffic_percentile)

        if models is None:
            models = []

        if inference_config is None:  # No-code deploy.
            environment_image_request = build_and_validate_no_code_environment_image_request(models)
        else:  # Normal inference config route.
            inference_config, has_env = convert_parts_to_environment(version_name, inference_config)

            if not has_env:
                raise WebserviceException('No Environment information is provided.', logger=module_logger)

            environment_image_request = \
                inference_config._build_environment_image_request(self.workspace, [model.id for model in models])

        patch_list = []
        properties = properties or {}
        properties.update(global_tracking_info_registry.gather_all())
        headers = {'Content-Type': 'application/json-patch+json'}
        headers.update(self._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        for existing_version_name in self.versions:
            if is_default:
                if existing_version_name != version_name:
                    patch_list.append(
                        {'op': 'replace', 'path': '/versions/{}/isDefault'.format(existing_version_name),
                         'value': False})

            if is_control_version_type:
                if existing_version_name != version_name:
                    patch_list.append(
                        {'op': 'replace', 'path': '/versions/{}/type'.format(existing_version_name),
                         'value': AksEndpoint.VersionType.treatment.value})

        version_deployment_config = AksServiceDeploymentConfiguration(autoscale_enabled, autoscale_min_replicas,
                                                                      autoscale_max_replicas,
                                                                      autoscale_refresh_seconds,
                                                                      autoscale_target_utilization,
                                                                      collect_model_data, None, cpu_cores,
                                                                      memory_gb,
                                                                      None, scoring_timeout_ms,
                                                                      replica_max_concurrent_requests,
                                                                      max_request_wait_time,
                                                                      num_replicas, None, None, tags,
                                                                      properties,
                                                                      description, gpu_cores, period_seconds,
                                                                      initial_delay_seconds,
                                                                      timeout_seconds, success_threshold,
                                                                      failure_threshold, None,
                                                                      None)
        deployment_target = ComputeTarget(self.workspace, self.compute_name)
        version_create_payload = version_deployment_config._build_create_payload(version_name,
                                                                                 environment_image_request,
                                                                                 deployment_target)
        if traffic_percentile is not None:
            version_create_payload['trafficPercentile'] = traffic_percentile
        if is_default:
            version_create_payload['isDefault'] = True
        if is_control_version_type:
            version_create_payload['type'] = AksEndpoint.VersionType.control.value
        patch_list.append({'op': 'add', 'path': '/versions/{}'.format(version_name), 'value': version_create_payload})
        self._patch_endpoint_call(headers, params, patch_list)

    def update_version(self, version_name, autoscale_enabled=None, autoscale_min_replicas=None,
                       autoscale_max_replicas=None, autoscale_refresh_seconds=None, autoscale_target_utilization=None,
                       collect_model_data=None, cpu_cores=None, memory_gb=None, scoring_timeout_ms=None,
                       replica_max_concurrent_requests=None, max_request_wait_time=None, num_replicas=None, tags=None,
                       properties=None, description=None, models=None, inference_config=None, gpu_cores=None,
                       period_seconds=None, initial_delay_seconds=None, timeout_seconds=None, success_threshold=None,
                       failure_threshold=None, traffic_percentile=None, is_default=None, is_control_version_type=None):
        """Update an existing version in an Endpoint with provided properties.

        Values left as None will remain unchanged in this version.

        :param version_name: The name of the version in an endpoint.
        :type version_name: str
        :param autoscale_enabled: Whether or not to enable autoscaling for this version in an Endpoint.
            Defaults to True if num_replicas is None
        :type autoscale_enabled: bool
        :param autoscale_min_replicas: The minimum number of containers to use when autoscaling this version in an
            Endpoint. Defaults to 1
        :type autoscale_min_replicas: int
        :param autoscale_max_replicas: The maximum number of containers to use when autoscaling this version in an
            Endpoint. Defaults to 10
        :type autoscale_max_replicas: int
        :param autoscale_refresh_seconds: How often the autoscaler should attempt to scale this version in an Endpoint.
            Defaults to 1
        :type autoscale_refresh_seconds: int
        :param autoscale_target_utilization: The target utilization (in percent out of 100) the autoscaler should
            attempt to maintain for this version in an Endpoint. Defaults to 70
        :type autoscale_target_utilization: int
        :param collect_model_data: Whether or not to enable model data collection for this version in an Endpoint.
            Defaults to False
        :type collect_model_data: bool
        :param cpu_cores: The number of cpu cores to allocate for this version in an Endpoint. Can be a decimal.
            Defaults to 0.1
        :type cpu_cores: float
        :param memory_gb: The amount of memory (in GB) to allocate for this version in an Endpoint. Can be a decimal.
            Defaults to 0.5
        :type memory_gb: float
        :param scoring_timeout_ms: A timeout to enforce for scoring calls to this version in an Endpoint.
            Defaults to 60000
        :type scoring_timeout_ms: int
        :param replica_max_concurrent_requests: The number of maximum concurrent requests per node to allow for this
            version in an Endpoint. Defaults to 1
        :type replica_max_concurrent_requests: int
        :param max_request_wait_time: The maximum amount of time a request will stay in the queue (in milliseconds)
            before returning a 503 error. Defaults to 500
        :type max_request_wait_time: int
        :param num_replicas: The number of containers to allocate for this version in an Endpoint. No default,
            if this parameter is not set then the autoscaler is enabled by default.
        :type num_replicas: int
        :param tags: Dictionary of key value tags to give this Endpoint
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to give this Endpoint. These properties cannot
            be changed after deployment, however new key value pairs can be added
        :type properties: dict[str, str]
        :param description: A description to give this Endpoint
        :type description: str
        :param models: A list of Model objects to package with the updated service
        :type models: :class:`list[azureml.core.Model]`
        :param inference_config: An InferenceConfig object used to provide the required model deployment properties.
        :type inference_config: azureml.core.model.InferenceConfig
        :param gpu_cores: The number of gpu cores to allocate for this version in an Endpoint. Default is 1
        :type gpu_cores: int
        :param period_seconds: How often (in seconds) to perform the liveness probe. Default to 10 seconds.
            Minimum value is 1.
        :type period_seconds: int
        :param initial_delay_seconds: Number of seconds after the container has started before liveness probes are
            initiated. Defaults to 310
        :type initial_delay_seconds: int
        :param timeout_seconds: Number of seconds after which the liveness probe times out. Defaults to 2 second.
            Minimum value is 1
        :type timeout_seconds: int
        :param success_threshold: Minimum consecutive successes for the liveness probe to be considered successful
            after having failed. Defaults to 1. Minimum value is 1.
        :type success_threshold: int
        :param failure_threshold: When a Pod starts and the liveness probe fails, Kubernetes will try failureThreshold
            times before giving up. Defaults to 3. Minimum value is 1.
        :type failure_threshold: int deploying a version in an Endpoint object
        :param traffic_percentile: the amount of traffic the version takes in an endpoint.
        :type traffic_percentile: float
        :param is_default: Whether or not to make this version as default version in an Endpoint.
            Defaults to False
        :type is_default: bool
        :param is_control_version_type: Whether or not to make this version as control version in an Endpoint.
            Defaults to False
        :type is_control_version_type: bool
        :raises: azureml.exceptions.WebserviceException
        """
        if version_name is None:
            raise WebserviceException('No name is provided to update a version.', logger=module_logger)

        if autoscale_enabled is None and not autoscale_min_replicas and not autoscale_max_replicas \
                and not autoscale_refresh_seconds and not autoscale_target_utilization and collect_model_data is None \
                and not cpu_cores and not memory_gb and not gpu_cores \
                and not scoring_timeout_ms and not replica_max_concurrent_requests \
                and not max_request_wait_time and not num_replicas and tags is None and properties is None \
                and not description and not period_seconds and not initial_delay_seconds and not timeout_seconds \
                and models is None and inference_config is None and not failure_threshold and not success_threshold \
                and traffic_percentile is None and is_default is None and is_control_version_type is None:
            raise WebserviceException('No parameters provided to update a version.', logger=module_logger)

        patch_list = []
        properties = properties or {}
        properties.update(global_tracking_info_registry.gather_all())
        headers = {'Content-Type': 'application/json-patch+json'}
        headers.update(self._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}
        for existing_version_name in self.versions:
            if is_default:
                if existing_version_name == version_name:
                    patch_list.append(
                        {'op': 'replace', 'path': '/versions/{}/isDefault'.format(existing_version_name),
                         'value': True})
                else:
                    patch_list.append(
                        {'op': 'replace', 'path': '/versions/{}/isDefault'.format(existing_version_name),
                         'value': False})
            if is_control_version_type:
                if existing_version_name == version_name:
                    patch_list.append(
                        {'op': 'replace', 'path': '/versions/{}/type'.format(existing_version_name),
                         'value': AksEndpoint.VersionType.control.value})
                else:
                    patch_list.append(
                        {'op': 'replace', 'path': '/versions/{}/type'.format(existing_version_name),
                         'value': AksEndpoint.VersionType.treatment.value})

        if inference_config:
            if models is None:
                models = self.versions[version_name].models

            inference_config, has_env = convert_parts_to_environment(version_name, inference_config)

            if not has_env:
                raise WebserviceException('No Environment information is provided.', logger=module_logger)

            environment_image_request = \
                inference_config._build_environment_image_request(self.workspace,
                                                                  [model.id for model in models])
            patch_list.append({'op': 'replace', 'path': '/versions/{}/environmentImageRequest'.format(version_name),
                               'value': environment_image_request})
        elif models is not None:
            # No-code deploy.
            environment_image_request = build_and_validate_no_code_environment_image_request(models)
            patch_list.append({'op': 'replace', 'path': '/versions/{}/environmentImageRequest'.format(version_name),
                               'value': environment_image_request})

        if autoscale_enabled is not None:
            patch_list.append(
                {'op': 'replace', 'path': '/versions/{}/autoScaler/autoscaleEnabled'.format(version_name),
                 'value': autoscale_enabled})
        if autoscale_min_replicas:
            patch_list.append(
                {'op': 'replace', 'path': '/versions/{}/autoScaler/minReplicas'.format(version_name),
                 'value': autoscale_min_replicas})
        if autoscale_max_replicas:
            patch_list.append(
                {'op': 'replace', 'path': '/versions/{}/autoScaler/maxReplicas'.format(version_name),
                 'value': autoscale_max_replicas})
        if autoscale_refresh_seconds:
            patch_list.append({'op': 'replace',
                               'path': '/versions/{}/autoScaler/refreshPeriodInSeconds'.format(version_name),
                               'value': autoscale_refresh_seconds})
        if autoscale_target_utilization:
            patch_list.append(
                {'op': 'replace', 'path': '/versions/{}/autoScaler/targetUtilization'.format(version_name),
                 'value': autoscale_target_utilization})
        if collect_model_data is not None:
            patch_list.append(
                {'op': 'replace', 'path': '/versions/{}/dataCollection/storageEnabled'.format(version_name),
                 'value': collect_model_data})

        if cpu_cores:
            patch_list.append({'op': 'replace',
                               'path': '/versions/{}/containerResourceRequirements/cpu'.format(version_name),
                               'value': cpu_cores})
        if memory_gb:
            patch_list.append({'op': 'replace',
                               'path': '/versions/{}/containerResourceRequirements/memoryInGB'.format(
                                   version_name),
                               'value': memory_gb})
        if gpu_cores:
            patch_list.append({'op': 'replace',
                               'path': '/versions/{}/containerResourceRequirements/gpu'.format(version_name),
                               'value': gpu_cores})
        if scoring_timeout_ms:
            patch_list.append({'op': 'replace', 'path': '/versions/{}/scoringTimeoutMs'.format(version_name),
                               'value': scoring_timeout_ms})
        if replica_max_concurrent_requests:
            patch_list.append({'op': 'replace',
                               'path': '/versions/{}/maxConcurrentRequestsPerContainer'.format(version_name),
                               'value': replica_max_concurrent_requests})
        if max_request_wait_time:
            patch_list.append({'op': 'replace', 'path': '/versions/{}/maxQueueWaitMs'.format(version_name),
                               'value': max_request_wait_time})
        if num_replicas:
            patch_list.append({'op': 'replace', 'path': '/versions/{}/numReplicas'.format(version_name),
                               'value': num_replicas})
        if period_seconds:
            patch_list.append({'op': 'replace',
                               'path': '/versions/{}/livenessProbeRequirements/periodSeconds'.format(
                                   version_name),
                               'value': period_seconds})
        if initial_delay_seconds:
            patch_list.append({'op': 'replace',
                               'path': '/versions/{}/livenessProbeRequirements/initialDelaySeconds'.format(
                                   version_name),
                               'value': initial_delay_seconds})
        if timeout_seconds:
            patch_list.append({'op': 'replace',
                               'path': '/versions/{}/livenessProbeRequirements/timeoutSeconds'.format(
                                   version_name),
                               'value': timeout_seconds})
        if success_threshold:
            patch_list.append({'op': 'replace',
                               'path': '/versions/{}/livenessProbeRequirements/successThreshold'.format(
                                   version_name),
                               'value': success_threshold})
        if failure_threshold:
            patch_list.append({'op': 'replace',
                               'path': '/versions/{}/livenessProbeRequirements/failureThreshold'.format(
                                   version_name),
                               'value': failure_threshold})
        if traffic_percentile is not None:
            patch_list.append({'op': 'replace',
                               'path': '/versions/{}/trafficPercentile'.format(
                                   version_name),
                               'value': traffic_percentile})
        if description:
            patch_list.append({'op': 'replace',
                               'path': '/versions/{}/description'.format(
                                   version_name),
                               'value': description})
        if tags:
            patch_list.append({'op': 'replace',
                               'path': '/versions/{}/tags'.format(
                                   version_name),
                               'value': tags})

        self._patch_endpoint_call(headers, params, patch_list)

    def _patch_endpoint_call(self, headers, params, patch_list):
        resp = ClientBase._execute_func(get_requests_session().patch, self._mms_endpoint, headers=headers,
                                        params=params, json=patch_list)

        if resp.status_code == 200:
            self.update_deployment_state()
        elif resp.status_code == 202:
            if 'Operation-Location' in resp.headers:
                operation_location = resp.headers['Operation-Location']
            else:
                raise WebserviceException('Missing response header key: Operation-Location', logger=module_logger)
            create_operation_status_id = operation_location.split('/')[-1]
            base_url = '/'.join(self._mms_endpoint.split('/')[:-2])
            operation_url = base_url + '/operations/{}'.format(create_operation_status_id)
            self._operation_endpoint = operation_url
            self.update_deployment_state()
        else:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content),
                                      logger=module_logger)

    def _validate_update(self, autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                         autoscale_refresh_seconds, autoscale_target_utilization, collect_model_data, cpu_cores,
                         memory_gb, enable_app_insights, scoring_timeout_ms, replica_max_concurrent_requests,
                         max_request_wait_time, num_replicas, tags, properties, description, models,
                         inference_config, gpu_cores, period_seconds, initial_delay_seconds, timeout_seconds,
                         success_threshold, failure_threshold, namespace, auth_enabled, token_auth_enabled,
                         version_name, traffic_percentile):

        super(AksEndpoint,
              self)._validate_update(None, autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                                     autoscale_refresh_seconds, autoscale_target_utilization, collect_model_data,
                                     cpu_cores, memory_gb, enable_app_insights, scoring_timeout_ms,
                                     replica_max_concurrent_requests, max_request_wait_time, num_replicas, tags,
                                     properties, description, models, inference_config, gpu_cores, period_seconds,
                                     initial_delay_seconds, timeout_seconds, success_threshold, failure_threshold,
                                     namespace, auth_enabled, token_auth_enabled)

        if version_name is not None:
            webservice_name_validation(version_name)
        error = ""
        if traffic_percentile and (traffic_percentile < 0 or traffic_percentile > 100):
            error += 'Invalid configuration, traffic_percentile cannot be negative or greater than 100.\n'

        if error:
            raise WebserviceException(error, logger=module_logger)

    def serialize(self):
        """Convert this Webservice into a json serialized dictionary.

        :return: The json representation of this Webservice
        :rtype: dict
        """
        created_time = self.created_time.isoformat() if self.created_time else None
        updated_time = self.updated_time.isoformat() if self.updated_time else None

        serialized_versions = {}
        for version in self.versions:
            serialized_versions.update({version: self.versions[version].serialize()})
        aks_endpoint_properties = {'name': self.name, 'description': self.description, 'tags': self.tags,
                                   'properties': self.properties, 'state': self.state, 'createdTime': created_time,
                                   'updatedTime': updated_time, 'error': self.error, 'computeName': self.compute_name,
                                   'computeType': self.compute_type, 'workspaceName': self.workspace.name,
                                   'deploymentStatus': self.deployment_status, 'scoringUri': self.scoring_uri,
                                   'authEnabled': self.auth_enabled, 'aadAuthEnabled': self.token_auth_enabled,
                                   'appInsightsEnabled': self.enable_app_insights, 'versions': serialized_versions}
        return aks_endpoint_properties


class AutoScaler(object):
    """Class containing details for the autoscaler for AKS Webservices."""

    _expected_payload_keys = ['autoscaleEnabled', 'maxReplicas', 'minReplicas', 'refreshPeriodInSeconds',
                              'targetUtilization']

    def __init__(self, autoscale_enabled, max_replicas, min_replicas, refresh_period_seconds, target_utilization):
        """Initialize the AKS AutoScaler.

        :param autoscale_enabled: Whether the autoscaler is enabled or disabled
        :type autoscale_enabled: bool
        :param max_replicas: The maximum number of containers for the Autoscaler to use
        :type max_replicas: int
        :param min_replicas: The minimum number of containers for the Autoscaler to use
        :type min_replicas: int
        :param refresh_period_seconds: How often the autoscaler should attempt to scale the Webservice
        :type refresh_period_seconds: int
        :param target_utilization: The target utilization (in percent out of 100) the autoscaler should
            attempt to maintain for the Webservice
        :type target_utilization: int
        """
        self.autoscale_enabled = autoscale_enabled
        self.max_replicas = max_replicas
        self.min_replicas = min_replicas
        self.refresh_period_seconds = refresh_period_seconds
        self.target_utilization = target_utilization

    def serialize(self):
        """Convert this AutoScaler into a json serialized dictionary.

        :return: The json representation of this AutoScaler
        :rtype: dict
        """
        return {'autoscaleEnabled': self.autoscale_enabled, 'minReplicas': self.min_replicas,
                'maxReplicas': self.max_replicas, 'refreshPeriodInSeconds': self.refresh_period_seconds,
                'targetUtilization': self.target_utilization}

    @staticmethod
    def deserialize(payload_obj):
        """Convert a json object into a AutoScaler object.

        :param payload_obj: A json object to convert to a AutoScaler object
        :type payload_obj: dict
        :return: The AutoScaler representation of the provided json object
        :rtype: azureml.core.webservice.aks.AutoScaler
        """
        for payload_key in AutoScaler._expected_payload_keys:
            if payload_key not in payload_obj:
                raise WebserviceException('Invalid webservice payload, missing {} for autoScaler:\n'
                                          '{}'.format(payload_key, payload_obj), logger=module_logger)

        return AutoScaler(payload_obj['autoscaleEnabled'], payload_obj['maxReplicas'], payload_obj['minReplicas'],
                          payload_obj['refreshPeriodInSeconds'], payload_obj['targetUtilization'])


class ContainerResourceRequirements(object):
    """Class containing details for the resource requirements for each container used by the Webservice."""

    _expected_payload_keys = ['cpu', 'memoryInGB', 'gpu']

    def __init__(self, cpu, memory_in_gb, gpu=None):
        """Initialize the container resource requirements.

        :param cpu: The number of cpu cores to allocate for this Webservice. Can be a decimal
        :type cpu: float
        :param memory_in_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal
        :type memory_in_gb: float
        """
        self.cpu = cpu
        self.memory_in_gb = memory_in_gb
        self.gpu = gpu

    def serialize(self):
        """Convert this ContainerResourceRequirements into a json serialized dictionary.

        :return: The json representation of this ContainerResourceRequirements
        :rtype: dict
        """
        return {'cpu': self.cpu, 'memoryInGB': self.memory_in_gb, 'gpu': self.gpu}

    @staticmethod
    def deserialize(payload_obj):
        """Convert a json object into a ContainerResourceRequirements object.

        :param payload_obj: A json object to convert to a ContainerResourceRequirements object
        :type payload_obj: dict
        :return: The ContainerResourceRequirements representation of the provided json object
        :rtype: azureml.core.webservice.aks.ContainerResourceRequirements
        """
        for payload_key in ContainerResourceRequirements._expected_payload_keys:
            if payload_key not in payload_obj:
                raise WebserviceException('Invalid webservice payload, missing {} for ContainerResourceRequirements:\n'
                                          '{}'.format(payload_key, payload_obj), logger=module_logger)

        return ContainerResourceRequirements(payload_obj['cpu'], payload_obj['memoryInGB'], payload_obj['gpu'])


class LivenessProbeRequirements(object):
    """Class containing details for the liveness probe time requirements for deployments of the webservice."""

    _expected_payload_keys = ['periodSeconds', 'initialDelaySeconds', 'timeoutSeconds',
                              'failureThreshold', 'successThreshold']

    def __init__(self, period_seconds, initial_delay_seconds, timeout_seconds, success_threshold, failure_threshold):
        """Initialize the container resource requirements.

        :param period_seconds: How often (in seconds) to perform the liveness probe. Default to 10 seconds.
            Minimum value is 1.
        :type period_seconds: int
        :param initial_delay_seconds: Number of seconds after the container has started before liveness probes are
            initiated.
        :type initial_delay_seconds: int
        :param timeout_seconds: Number of seconds after which the liveness probe times out. Defaults to 1 second.
            Minimum value is 1.
        :type timeout_seconds: int
        :param failure_threshold: When a Pod starts and the liveness probe fails, Kubernetes will try failureThreshold
            times before giving up. Defaults to 3. Minimum value is 1.
        :type failure_threshold: int
        :param success_threshold: Minimum consecutive successes for the liveness probe to be considered successful
            after having failed. Defaults to 1. Minimum value is 1.
        :type success_threshold: int
        """
        self.period_seconds = period_seconds
        self.timeout_seconds = timeout_seconds
        self.initial_delay_seconds = initial_delay_seconds
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold

    def serialize(self):
        """Convert this LivenessProbeRequirements into a json serialized dictionary.

        :return: The json representation of this LivenessProbeRequirements
        :rtype: dict
        """
        return {'periodSeconds': self.period_seconds, 'initialDelaySeconds': self.initial_delay_seconds,
                'timeoutSeconds': self.timeout_seconds, 'successThreshold': self.success_threshold,
                'failureThreshold': self.failure_threshold}

    @staticmethod
    def deserialize(payload_obj):
        """Convert a json object into a LivenessProbeRequirements object.

        :param payload_obj: A json object to convert to a LivenessProbeRequirements object
        :type payload_obj: dict
        :return: The LivenessProbeRequirements representation of the provided json object
        :rtype: azureml.core.webservice.aks.LivenessProbeRequirements
        """
        if payload_obj is None:
            return LivenessProbeRequirements(period_seconds=10, initial_delay_seconds=310, timeout_seconds=1,
                                             success_threshold=1, failure_threshold=3)
        for payload_key in LivenessProbeRequirements._expected_payload_keys:
            if payload_key not in payload_obj:
                raise WebserviceException('Invalid webservice payload, missing {} for LivenessProbeRequirements:\n'
                                          '{}'.format(payload_key, payload_obj), logger=module_logger)

        return LivenessProbeRequirements(payload_obj['periodSeconds'], payload_obj['initialDelaySeconds'],
                                         payload_obj['timeoutSeconds'], payload_obj['successThreshold'],
                                         payload_obj['failureThreshold'])


class DataCollection(object):
    """Class for managing data collection for an AKS Webservice."""

    _expected_payload_keys = ['eventHubEnabled', 'storageEnabled']

    def __init__(self, event_hub_enabled, storage_enabled):
        """Intialize the DataCollection object.

        :param event_hub_enabled: Whether or not event hub is enabled for the Webservice
        :type event_hub_enabled: bool
        :param storage_enabled: Whether or not data collection storage is enabled for the Webservice
        :type storage_enabled: bool
        """
        self.event_hub_enabled = event_hub_enabled
        self.storage_enabled = storage_enabled

    def serialize(self):
        """Convert this DataCollection into a json serialized dictionary.

        :return: The json representation of this DataCollection
        :rtype: dict
        """
        return {'eventHubEnabled': self.event_hub_enabled, 'storageEnabled': self.storage_enabled}

    @staticmethod
    def deserialize(payload_obj):
        """Convert a json object into a DataCollection object.

        :param payload_obj: A json object to convert to a DataCollection object
        :type payload_obj: dict
        :return: The DataCollection representation of the provided json object
        :rtype: azureml.core.webservice.aks.DataCollection
        """
        for payload_key in DataCollection._expected_payload_keys:
            if payload_key not in payload_obj:
                raise WebserviceException('Invalid webservice payload, missing {} for DataCollection:\n'
                                          '{}'.format(payload_key, payload_obj), logger=module_logger)

        return DataCollection(payload_obj['eventHubEnabled'], payload_obj['storageEnabled'])


class AksServiceDeploymentConfiguration(WebserviceDeploymentConfiguration):
    """Service deployment configuration object for services deployed on AKS compute.

    :param autoscale_enabled: Whether or not to enable autoscaling for this Webservice.
        Defaults to True if num_replicas is None
    :type autoscale_enabled: bool
    :param autoscale_min_replicas: The minimum number of containers to use when autoscaling this Webservice.
        Defaults to 1
    :type autoscale_min_replicas: int
    :param autoscale_max_replicas: The maximum number of containers to use when autoscaling this Webservice.
        Defaults to 10
    :type autoscale_max_replicas: int
    :param autoscale_refresh_seconds: How often the autoscaler should attempt to scale this Webservice.
        Defaults to 1
    :type autoscale_refresh_seconds: int
    :param autoscale_target_utilization: The target utilization (in percent out of 100) the autoscaler should
        attempt to maintain for this Webservice. Defaults to 70
    :type autoscale_target_utilization: int
    :param collect_model_data: Whether or not to enable model data collection for this Webservice.
        Defaults to False
    :type collect_model_data: bool
    :param auth_enabled: Whether or not to enable auth for this Webservice. Defaults to True
    :type auth_enabled: bool
    :param cpu_cores: The number of cpu cores to allocate for this Webservice. Can be a decimal. Defaults to 0.1
    :type cpu_cores: float
    :param memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal.
        Defaults to 0.5
    :type memory_gb: float
    :param enable_app_insights: Whether or not to enable Application Insights logging for this Webservice.
        Defaults to False
    :type enable_app_insights: bool
    :param scoring_timeout_ms: A timeout to enforce for scoring calls to this Webservice. Defaults to 60000
    :type scoring_timeout_ms: int
    :param replica_max_concurrent_requests: The number of maximum concurrent requests per node to allow for this
        Webservice. Defaults to 1
    :type replica_max_concurrent_requests: int
    :param max_request_wait_time: The maximum amount of time a request will stay in the queue (in milliseconds)
        before returning a 503 error. Defaults to 500
    :type max_request_wait_time: int
    :param num_replicas: The number of containers to allocate for this Webservice. No default, if this parameter
        is not set then the autoscaler is enabled by default.
    :type num_replicas: int
    :param primary_key: A primary auth key to use for this Webservice
    :type primary_key: str
    :param secondary_key: A secondary auth key to use for this Webservice
    :type secondary_key: str
    :param tags: Dictionary of key value tags to give this Webservice
    :type tags: dict[str, str]
    :param properties: Dictionary of key value properties to give this Webservice. These properties cannot
        be changed after deployment, however new key value pairs can be added
    :type properties: dict[str, str]
    :param description: A description to give this Webservice
    :type description: str
    :param gpu_cores: The number of gpu cores to allocate for this Webservice. Default is 1
    :type gpu_cores: int
    :param period_seconds: How often (in seconds) to perform the liveness probe. Default to 10 seconds.
        Minimum value is 1.
    :type period_seconds: int
    :param initial_delay_seconds: Number of seconds after the container has started before liveness probes are
        initiated. Defaults to 310
    :type initial_delay_seconds: int
    :param timeout_seconds: Number of seconds after which the liveness probe times out. Defaults to 2 second.
        Minimum value is 1
    :type timeout_seconds: int
    :param success_threshold: Minimum consecutive successes for the liveness probe to be considered successful
        after having failed. Defaults to 1. Minimum value is 1.
    :type success_threshold: int
    :param failure_threshold: When a Pod starts and the liveness probe fails, Kubernetes will try failureThreshold
        times before giving up. Defaults to 3. Minimum value is 1.
    :type failure_threshold: int
    :param namespace: The Kubernetes namespace in which to deploy this Webservice: up to 63 lowercase alphanumeric
        ('a'-'z', '0'-'9') and hyphen ('-') characters. The first and last characters cannot be hyphens.
    :type namespace: str
    :param token_auth_enabled: Whether or not to enable Azure Active Directory auth for this Webservice. If this is
            enabled, users can access this Webservice by fetching access token using their Azure Active Directory
            credentials. Defaults to False
    :type token_auth_enabled: bool
    :return: A configuration object to use when deploying a Webservice object.
    """

    def __init__(self, autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas, autoscale_refresh_seconds,
                 autoscale_target_utilization, collect_model_data, auth_enabled, cpu_cores, memory_gb,
                 enable_app_insights, scoring_timeout_ms, replica_max_concurrent_requests, max_request_wait_time,
                 num_replicas, primary_key, secondary_key, tags, properties, description, gpu_cores, period_seconds,
                 initial_delay_seconds, timeout_seconds, success_threshold, failure_threshold, namespace,
                 token_auth_enabled):
        """Initialize a configuration object for deploying to an AKS compute target.

        :param autoscale_enabled: Whether or not to enable autoscaling for this Webservice.
            Defaults to True if num_replicas is None
        :type autoscale_enabled: bool
        :param autoscale_min_replicas: The minimum number of containers to use when autoscaling this Webservice.
            Defaults to 1
        :type autoscale_min_replicas: int
        :param autoscale_max_replicas: The maximum number of containers to use when autoscaling this Webservice.
            Defaults to 10
        :type autoscale_max_replicas: int
        :param autoscale_refresh_seconds: How often the autoscaler should attempt to scale this Webservice.
            Defaults to 1
        :type autoscale_refresh_seconds: int
        :param autoscale_target_utilization: The target utilization (in percent out of 100) the autoscaler should
            attempt to maintain for this Webservice. Defaults to 70
        :type autoscale_target_utilization: int
        :param collect_model_data: Whether or not to enable model data collection for this Webservice.
            Defaults to False
        :type collect_model_data: bool
        :param auth_enabled: Whether or not to enable auth for this Webservice. Defaults to True
        :type auth_enabled: bool
        :param cpu_cores: The number of cpu cores to allocate for this Webservice. Can be a decimal. Defaults to 0.1
        :type cpu_cores: float
        :param memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal.
            Defaults to 0.5
        :type memory_gb: float
        :param enable_app_insights: Whether or not to enable Application Insights logging for this Webservice.
            Defaults to False
        :type enable_app_insights: bool
        :param scoring_timeout_ms: A timeout to enforce for scoring calls to this Webservice. Defaults to 60000
        :type scoring_timeout_ms: int
        :param replica_max_concurrent_requests: The number of maximum concurrent requests per node to allow for this
            Webservice. Defaults to 1
        :type replica_max_concurrent_requests: int
        :param max_request_wait_time: The maximum amount of time a request will stay in the queue (in milliseconds)
            before returning a 503 error. Defaults to 500
        :type max_request_wait_time: int
        :param num_replicas: The number of containers to allocate for this Webservice. No default, if this parameter
            is not set then the autoscaler is enabled by default.
        :type num_replicas: int
        :param primary_key: A primary auth key to use for this Webservice
        :type primary_key: str
        :param secondary_key: A secondary auth key to use for this Webservice
        :type secondary_key: str
        :param tags: Dictionary of key value tags to give this Webservice
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to give this Webservice. These properties cannot
            be changed after deployment, however new key value pairs can be added
        :type properties: dict[str, str]
        :param description: A description to give this Webservice
        :type description: str
        :param gpu_cores: The number of gpu cores to allocate for this Webservice. Default is 1
        :type gpu_cores: int
        :param period_seconds: How often (in seconds) to perform the liveness probe. Default to 10 seconds.
            Minimum value is 1.
        :type period_seconds: int
        :param initial_delay_seconds: Number of seconds after the container has started before liveness probes are
            initiated. Defaults to 310
        :type initial_delay_seconds: int
        :param timeout_seconds: Number of seconds after which the liveness probe times out. Defaults to 2 second.
            Minimum value is 1
        :type timeout_seconds: int
        :param success_threshold: Minimum consecutive successes for the liveness probe to be considered successful
            after having failed. Defaults to 1. Minimum value is 1.
        :type success_threshold: int
        :param failure_threshold: When a Pod starts and the liveness probe fails, Kubernetes will try failureThreshold
            times before giving up. Defaults to 3. Minimum value is 1.
        :type failure_threshold: int
        :param namespace: The Kubernetes namespace in which to deploy this Webservice: up to 63 lowercase alphanumeric
            ('a'-'z', '0'-'9') and hyphen ('-') characters. The first and last characters cannot be hyphens.
        :type namespace: str
        :param token_auth_enabled: Whether or not to enable Azure Active Directory auth for this Webservice. If this is
            enabled, users can access this Webservice by fetching access token using their Azure Active Directory
            credentials. Defaults to False
        :type token_auth_enabled: bool
        :return: A configuration object to use when deploying a Webservice object.
        :raises: azureml.exceptions.WebserviceException
        """
        super(AksServiceDeploymentConfiguration, self).__init__(AksWebservice, description, tags, properties,
                                                                primary_key, secondary_key)
        self.autoscale_enabled = autoscale_enabled
        self.autoscale_min_replicas = autoscale_min_replicas
        self.autoscale_max_replicas = autoscale_max_replicas
        self.autoscale_refresh_seconds = autoscale_refresh_seconds
        self.autoscale_target_utilization = autoscale_target_utilization
        self.collect_model_data = collect_model_data
        self.auth_enabled = auth_enabled
        self.cpu_cores = cpu_cores
        self.memory_gb = memory_gb
        self.gpu_cores = gpu_cores
        self.enable_app_insights = enable_app_insights
        self.scoring_timeout_ms = scoring_timeout_ms
        self.replica_max_concurrent_requests = replica_max_concurrent_requests
        self.max_request_wait_time = max_request_wait_time
        self.num_replicas = num_replicas
        self.period_seconds = period_seconds
        self.initial_delay_seconds = initial_delay_seconds
        self.timeout_seconds = timeout_seconds
        self.success_threshold = success_threshold
        self.failure_threshold = failure_threshold
        self.namespace = namespace
        self.token_auth_enabled = token_auth_enabled
        self.validate_configuration()

    def validate_configuration(self):
        """Check that the specified configuration values are valid.

        Will raise a WebserviceException if validation fails.

        :raises: azureml.exceptions.WebserviceException
        """
        error = ""
        if self.cpu_cores and self.cpu_cores <= 0:
            error += 'Invalid configuration, cpu_cores must be greater than zero.\n'
        if self.memory_gb and self.memory_gb <= 0:
            error += 'Invalid configuration, memory_gb must be greater than zero.\n'
        if self.gpu_cores and self.gpu_cores <= 0:
            error += 'Invalid configuration, gpu_cores must be greater than zero.\n'
        if self.period_seconds and self.period_seconds <= 0:
            error += 'Invalid configuration, period_seconds must be greater than zero.\n'
        if self.initial_delay_seconds and self.initial_delay_seconds <= 0:
            error += 'Invalid configuration, initial_delay_seconds must be greater than zero.\n'
        if self.timeout_seconds and self.timeout_seconds <= 0:
            error += 'Invalid configuration, timeout_seconds must be greater than zero.\n'
        if self.success_threshold and self.success_threshold <= 0:
            error += 'Invalid configuration, success_threshold must be greater than zero.\n'
        if self.failure_threshold and self.failure_threshold <= 0:
            error += 'Invalid configuration, failure_threshold must be greater than zero.\n'
        if self.namespace and not re.match(NAMESPACE_REGEX, self.namespace):
            error += 'Invalid configuration, namespace must be a valid Kubernetes namespace. ' \
                     'Regex for validation is ' + NAMESPACE_REGEX + '\n'
        if self.scoring_timeout_ms and self.scoring_timeout_ms <= 0:
            error += 'Invalid configuration, scoring_timeout_ms must be greater than zero.\n'
        if self.replica_max_concurrent_requests and self.replica_max_concurrent_requests <= 0:
            error += 'Invalid configuration, replica_max_concurrent_requests must be greater than zero.\n'
        if self.max_request_wait_time and self.max_request_wait_time <= 0:
            error += 'Invalid configuration, max_request_wait_time must be greater than zero.\n'
        if self.num_replicas and self.num_replicas <= 0:
            error += 'Invalid configuration, num_replicas must be greater than zero.\n'
        if self.autoscale_enabled:
            if self.num_replicas:
                error += 'Invalid configuration, autoscale enabled and num_replicas provided.\n'
            if self.autoscale_min_replicas and self.autoscale_min_replicas <= 0:
                error += 'Invalid configuration, autoscale_min_replicas must be greater than zero.\n'
            if self.autoscale_max_replicas and self.autoscale_max_replicas <= 0:
                error += 'Invalid configuration, autoscale_max_replicas must be greater than zero.\n'
            if self.autoscale_min_replicas and self.autoscale_max_replicas and \
                    self.autoscale_min_replicas > self.autoscale_max_replicas:
                error += 'Invalid configuration, autoscale_min_replicas cannot be greater than ' \
                         'autoscale_max_replicas.\n'
            if self.autoscale_refresh_seconds and self.autoscale_refresh_seconds <= 0:
                error += 'Invalid configuration, autoscale_refresh_seconds must be greater than zero.\n'
            if self.autoscale_target_utilization and self.autoscale_target_utilization <= 0:
                error += 'Invalid configuration, autoscale_target_utilization must be greater than zero.\n'
        else:
            if self.autoscale_enabled is False and not self.num_replicas:
                error += 'Invalid configuration, autoscale disabled but num_replicas not provided.\n'
            if self.autoscale_min_replicas:
                error += 'Invalid configuration, autoscale_min_replicas provided without enabling autoscaling.\n'
            if self.autoscale_max_replicas:
                error += 'Invalid configuration, autoscale_max_replicas provided without enabling autoscaling.\n'
            if self.autoscale_refresh_seconds:
                error += 'Invalid configuration, autoscale_refresh_seconds provided without enabling autoscaling.\n'
            if self.autoscale_target_utilization:
                error += 'Invalid configuration, autoscale_target_utilization provided without enabling autoscaling.\n'
        if self.token_auth_enabled and self.auth_enabled:
            error += "Invalid configuration, auth_enabled and token_auth_enabled cannot both be true.\n"

        if error:
            raise WebserviceException(error, logger=module_logger)

    def _build_create_payload(self, name, environment_image_request, deployment_target=None, overwrite=False):
        import copy
        from azureml._model_management._util import aks_specific_service_create_payload_template
        json_payload = copy.deepcopy(aks_specific_service_create_payload_template)
        base_payload = super(AksServiceDeploymentConfiguration,
                             self)._build_base_create_payload(name, environment_image_request)

        json_payload['numReplicas'] = self.num_replicas
        if self.collect_model_data:
            json_payload['dataCollection']['storageEnabled'] = self.collect_model_data
        else:
            del(json_payload['dataCollection'])
        if self.enable_app_insights is not None:
            json_payload['appInsightsEnabled'] = self.enable_app_insights
        else:
            del(json_payload['appInsightsEnabled'])
        if self.autoscale_enabled is not None:
            json_payload['autoScaler']['autoscaleEnabled'] = self.autoscale_enabled
            json_payload['autoScaler']['minReplicas'] = self.autoscale_min_replicas
            json_payload['autoScaler']['maxReplicas'] = self.autoscale_max_replicas
            json_payload['autoScaler']['targetUtilization'] = self.autoscale_target_utilization
            json_payload['autoScaler']['refreshPeriodInSeconds'] = self.autoscale_refresh_seconds
        else:
            del(json_payload['autoScaler'])
        json_payload['containerResourceRequirements']['cpu'] = self.cpu_cores
        json_payload['containerResourceRequirements']['memoryInGB'] = self.memory_gb
        json_payload['containerResourceRequirements']['gpu'] = self.gpu_cores
        json_payload['maxConcurrentRequestsPerContainer'] = self.replica_max_concurrent_requests
        json_payload['maxQueueWaitMs'] = self.max_request_wait_time
        json_payload['namespace'] = self.namespace
        json_payload['scoringTimeoutMs'] = self.scoring_timeout_ms
        if self.auth_enabled is not None:
            json_payload['authEnabled'] = self.auth_enabled
        else:
            del(json_payload['authEnabled'])
        if self.token_auth_enabled is not None:
            json_payload['aadAuthEnabled'] = self.token_auth_enabled
        else:
            del(json_payload['aadAuthEnabled'])
        json_payload['livenessProbeRequirements']['periodSeconds'] = self.period_seconds
        json_payload['livenessProbeRequirements']['initialDelaySeconds'] = self.initial_delay_seconds
        json_payload['livenessProbeRequirements']['timeoutSeconds'] = self.timeout_seconds
        json_payload['livenessProbeRequirements']['failureThreshold'] = self.failure_threshold
        json_payload['livenessProbeRequirements']['successThreshold'] = self.success_threshold

        if overwrite:
            json_payload['overwrite'] = overwrite
        else:
            del (json_payload['overwrite'])

        if deployment_target is not None:
            json_payload['computeName'] = deployment_target.name

        json_payload.update(base_payload)

        return json_payload


class AksEndpointDeploymentConfiguration(AksServiceDeploymentConfiguration):
    """Service deployment configuration object for services deployed on AKS compute.

    :param autoscale_enabled: Whether or not to enable autoscaling for this Webservice.
        Defaults to True if num_replicas is None
    :type autoscale_enabled: bool
    :param autoscale_min_replicas: The minimum number of containers to use when autoscaling this Webservice.
        Defaults to 1
    :type autoscale_min_replicas: int
    :param autoscale_max_replicas: The maximum number of containers to use when autoscaling this Webservice.
        Defaults to 10
    :type autoscale_max_replicas: int
    :param autoscale_refresh_seconds: How often the autoscaler should attempt to scale this Webservice.
        Defaults to 1
    :type autoscale_refresh_seconds: int
    :param autoscale_target_utilization: The target utilization (in percent out of 100) the autoscaler should
        attempt to maintain for this Webservice. Defaults to 70
    :type autoscale_target_utilization: int
    :param collect_model_data: Whether or not to enable model data collection for this Webservice.
        Defaults to False
    :type collect_model_data: bool
    :param auth_enabled: Whether or not to enable auth for this Webservice. Defaults to True
    :type auth_enabled: bool
    :param cpu_cores: The number of cpu cores to allocate for this Webservice. Can be a decimal. Defaults to 0.1
    :type cpu_cores: float
    :param memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal.
        Defaults to 0.5
    :type memory_gb: float
    :param enable_app_insights: Whether or not to enable Application Insights logging for this Webservice.
        Defaults to False
    :type enable_app_insights: bool
    :param scoring_timeout_ms: A timeout to enforce for scoring calls to this Webservice. Defaults to 60000
    :type scoring_timeout_ms: int
    :param replica_max_concurrent_requests: The number of maximum concurrent requests per node to allow for this
        Webservice. Defaults to 1
    :type replica_max_concurrent_requests: int
    :param max_request_wait_time: The maximum amount of time a request will stay in the queue (in milliseconds)
        before returning a 503 error. Defaults to 500
    :type max_request_wait_time: int
    :param num_replicas: The number of containers to allocate for this Webservice. No default, if this parameter
        is not set then the autoscaler is enabled by default.
    :type num_replicas: int
    :param primary_key: A primary auth key to use for this Webservice
    :type primary_key: str
    :param secondary_key: A secondary auth key to use for this Webservice
    :type secondary_key: str
    :param tags: Dictionary of key value tags to give this Webservice
    :type tags: dict[str, str]
    :param properties: Dictionary of key value properties to give this Webservice. These properties cannot
        be changed after deployment, however new key value pairs can be added
    :type properties: dict[str, str]
    :param description: A description to give this Webservice
    :type description: str
    :param gpu_cores: The number of gpu cores to allocate for this Webservice. Default is 1
    :type gpu_cores: int
    :param period_seconds: How often (in seconds) to perform the liveness probe. Default to 10 seconds.
        Minimum value is 1.
    :type period_seconds: int
    :param initial_delay_seconds: Number of seconds after the container has started before liveness probes are
        initiated. Defaults to 310
    :type initial_delay_seconds: int
    :param timeout_seconds: Number of seconds after which the liveness probe times out. Defaults to 2 second.
        Minimum value is 1
    :type timeout_seconds: int
    :param success_threshold: Minimum consecutive successes for the liveness probe to be considered successful
        after having failed. Defaults to 1. Minimum value is 1.
    :type success_threshold: int
    :param failure_threshold: When a Pod starts and the liveness probe fails, Kubernetes will try failureThreshold
        times before giving up. Defaults to 3. Minimum value is 1.
    :type failure_threshold: int
    :param namespace: The Kubernetes namespace in which to deploy this Webservice: up to 63 lowercase alphanumeric
        ('a'-'z', '0'-'9') and hyphen ('-') characters. The first and last characters cannot be hyphens.
    :type namespace: str
    :param token_auth_enabled: Whether or not to enable Azure Active Directory auth for this Webservice. If this is
            enabled, users can access this Webservice by fetching access token using their Azure Active Directory
            credentials. Defaults to False
    :type token_auth_enabled: bool
    :param version_name: The name of the version in an endpoint.
    :type version_name: str
    :param traffic_percentile: the amount of traffic the version takes in an endpoint.
    :type traffic_percentile: float
    :return: A configuration object to use when deploying a Endpoint object.
    """

    def __init__(self, autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas, autoscale_refresh_seconds,
                 autoscale_target_utilization, collect_model_data, auth_enabled, cpu_cores, memory_gb,
                 enable_app_insights, scoring_timeout_ms, replica_max_concurrent_requests, max_request_wait_time,
                 num_replicas, primary_key, secondary_key, tags, properties, description, gpu_cores, period_seconds,
                 initial_delay_seconds, timeout_seconds, success_threshold, failure_threshold, namespace,
                 token_auth_enabled, version_name, traffic_percentile):
        """Initialize a configuration object for deploying an Endpoint to an AKS compute target.

        :param autoscale_enabled: Whether or not to enable autoscaling for this Webservice.
            Defaults to True if num_replicas is None
        :type autoscale_enabled: bool
        :param autoscale_min_replicas: The minimum number of containers to use when autoscaling this Webservice.
            Defaults to 1
        :type autoscale_min_replicas: int
        :param autoscale_max_replicas: The maximum number of containers to use when autoscaling this Webservice.
            Defaults to 10
        :type autoscale_max_replicas: int
        :param autoscale_refresh_seconds: How often the autoscaler should attempt to scale this Webservice.
            Defaults to 1
        :type autoscale_refresh_seconds: int
        :param autoscale_target_utilization: The target utilization (in percent out of 100) the autoscaler should
            attempt to maintain for this Webservice. Defaults to 70
        :type autoscale_target_utilization: int
        :param collect_model_data: Whether or not to enable model data collection for this Webservice.
            Defaults to False
        :type collect_model_data: bool
        :param auth_enabled: Whether or not to enable auth for this Webservice. Defaults to True
        :type auth_enabled: bool
        :param cpu_cores: The number of cpu cores to allocate for this Webservice. Can be a decimal. Defaults to 0.1
        :type cpu_cores: float
        :param memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal.
            Defaults to 0.5
        :type memory_gb: float
        :param enable_app_insights: Whether or not to enable Application Insights logging for this Webservice.
            Defaults to False
        :type enable_app_insights: bool
        :param scoring_timeout_ms: A timeout to enforce for scoring calls to this Webservice. Defaults to 60000
        :type scoring_timeout_ms: int
        :param replica_max_concurrent_requests: The number of maximum concurrent requests per node to allow for this
            Webservice. Defaults to 1
        :type replica_max_concurrent_requests: int
        :param max_request_wait_time: The maximum amount of time a request will stay in the queue (in milliseconds)
            before returning a 503 error. Defaults to 500
        :type max_request_wait_time: int
        :param num_replicas: The number of containers to allocate for this Webservice. No default, if this parameter
            is not set then the autoscaler is enabled by default.
        :type num_replicas: int
        :param primary_key: A primary auth key to use for this Webservice
        :type primary_key: str
        :param secondary_key: A secondary auth key to use for this Webservice
        :type secondary_key: str
        :param tags: Dictionary of key value tags to give this Webservice
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to give this Webservice. These properties cannot
            be changed after deployment, however new key value pairs can be added
        :type properties: dict[str, str]
        :param description: A description to give this Webservice
        :type description: str
        :param gpu_cores: The number of gpu cores to allocate for this Webservice. Default is 1
        :type gpu_cores: int
        :param period_seconds: How often (in seconds) to perform the liveness probe. Default to 10 seconds.
            Minimum value is 1.
        :type period_seconds: int
        :param initial_delay_seconds: Number of seconds after the container has started before liveness probes are
            initiated. Defaults to 310
        :type initial_delay_seconds: int
        :param timeout_seconds: Number of seconds after which the liveness probe times out. Defaults to 2 second.
            Minimum value is 1
        :type timeout_seconds: int
        :param success_threshold: Minimum consecutive successes for the liveness probe to be considered successful
            after having failed. Defaults to 1. Minimum value is 1.
        :type success_threshold: int
        :param failure_threshold: When a Pod starts and the liveness probe fails, Kubernetes will try failureThreshold
            times before giving up. Defaults to 3. Minimum value is 1.
        :type failure_threshold: int
        :param namespace: The Kubernetes namespace in which to deploy this Webservice: up to 63 lowercase alphanumeric
            ('a'-'z', '0'-'9') and hyphen ('-') characters. The first and last characters cannot be hyphens.
        :type namespace: str
        :param token_auth_enabled: Whether or not to enable Azure Active Directory auth for this Webservice. If this is
            enabled, users can access this Webservice by fetching access token using their Azure Active Directory
            credentials. Defaults to False
        :type token_auth_enabled: bool
        :param version_name: The name of the version in an endpoint.
        :type version_name: str
        :param traffic_percentile: the amount of traffic the version takes in an endpoint.
        :type traffic_percentile: float
        :return: A configuration object to use when deploying a Endpoint object.
        :raises: azureml.exceptions.WebserviceException
        """
        super(AksEndpointDeploymentConfiguration, self).__init__(autoscale_enabled, autoscale_min_replicas,
                                                                 autoscale_max_replicas, autoscale_refresh_seconds,
                                                                 autoscale_target_utilization, collect_model_data,
                                                                 auth_enabled, cpu_cores, memory_gb,
                                                                 enable_app_insights, scoring_timeout_ms,
                                                                 replica_max_concurrent_requests,
                                                                 max_request_wait_time, num_replicas, primary_key,
                                                                 secondary_key, tags, properties, description,
                                                                 gpu_cores, period_seconds, initial_delay_seconds,
                                                                 timeout_seconds, success_threshold, failure_threshold,
                                                                 namespace, token_auth_enabled)
        self._webservice_type = AksEndpoint
        self.version_name = version_name
        self.traffic_percentile = traffic_percentile
        self.validate_endpoint_configuration()

    def validate_endpoint_configuration(self):
        """Check that the specified configuration values are valid.

        Will raise a WebserviceException if validation fails.

        :raises: azureml.exceptions.WebserviceException
        """
        error = ""
        if self.version_name:
            webservice_name_validation(self.version_name)
        if self.traffic_percentile and (self.traffic_percentile < 0 or self.traffic_percentile > 100):
            error += 'Invalid configuration, traffic_percentile cannot be negative or greater than 100.\n'

        if error:
            raise WebserviceException(error, logger=module_logger)

    def _build_create_payload(self, name, environment_image_request, overwrite=False):
        from azureml._model_management._util import aks_specific_endpoint_create_payload_template
        json_payload = copy.deepcopy(aks_specific_endpoint_create_payload_template)
        if self.version_name is None:
            self.version_name = name

        version_payload = super(AksEndpointDeploymentConfiguration,
                                self)._build_create_payload(self.version_name, environment_image_request)

        # update the version payload
        version_payload['trafficPercentile'] = self.traffic_percentile

        json_payload['name'] = name
        json_payload['description'] = self.description
        json_payload['kvTags'] = self.tags

        properties = self.properties or {}
        properties.update(global_tracking_info_registry.gather_all())
        json_payload['properties'] = properties

        if self.primary_key:
            json_payload['keys']['primaryKey'] = self.primary_key
            json_payload['keys']['secondaryKey'] = self.secondary_key

        json_payload['computeType'] = AksEndpoint._webservice_type
        if self.enable_app_insights is not None:
            json_payload['appInsightsEnabled'] = self.enable_app_insights
        else:
            del(json_payload['appInsightsEnabled'])
        if self.namespace is not None:
            json_payload['namespace'] = self.namespace
        else:
            del(json_payload['namespace'])
        if self.auth_enabled is not None:
            json_payload['authEnabled'] = self.auth_enabled
        else:
            del(json_payload['authEnabled'])
        if self.token_auth_enabled is not None:
            json_payload['aadAuthEnabled'] = self.token_auth_enabled
        else:
            del(json_payload['aadAuthEnabled'])

        if overwrite:
            json_payload['overwrite'] = overwrite
        else:
            del (json_payload['overwrite'])

        json_payload['versions'] = {self.version_name: version_payload}
        return json_payload
