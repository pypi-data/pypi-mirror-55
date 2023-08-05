# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator 2.3.33.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class CreateRunDto(Model):
    """CreateRunDto.

    :param run_id:
    :type run_id: str
    :param parent_run_id:
    :type parent_run_id: str
    :param status:
    :type status: str
    :param start_time_utc:
    :type start_time_utc: datetime
    :param end_time_utc:
    :type end_time_utc: datetime
    :param heartbeat_enabled:
    :type heartbeat_enabled: bool
    :param options:
    :type options: ~_restclient.models.RunOptions
    :param name:
    :type name: str
    :param data_container_id:
    :type data_container_id: str
    :param description:
    :type description: str
    :param hidden:
    :type hidden: bool
    :param run_type:
    :type run_type: str
    :param properties:
    :type properties: dict[str, str]
    :param script_name:
    :type script_name: str
    :param target:
    :type target: str
    :param tags:
    :type tags: dict[str, str]
    :param input_datasets:
    :type input_datasets: list[~_restclient.models.Dataset]
    :param run_definition:
    :type run_definition: object
    :param created_from:
    :type created_from: ~_restclient.models.CreatedFromDto
    :param cancel_uri:
    :type cancel_uri: str
    :param diagnostics_uri:
    :type diagnostics_uri: str
    """

    _attribute_map = {
        'run_id': {'key': 'runId', 'type': 'str'},
        'parent_run_id': {'key': 'parentRunId', 'type': 'str'},
        'status': {'key': 'status', 'type': 'str'},
        'start_time_utc': {'key': 'startTimeUtc', 'type': 'iso-8601'},
        'end_time_utc': {'key': 'endTimeUtc', 'type': 'iso-8601'},
        'heartbeat_enabled': {'key': 'heartbeatEnabled', 'type': 'bool'},
        'options': {'key': 'options', 'type': 'RunOptions'},
        'name': {'key': 'name', 'type': 'str'},
        'data_container_id': {'key': 'dataContainerId', 'type': 'str'},
        'description': {'key': 'description', 'type': 'str'},
        'hidden': {'key': 'hidden', 'type': 'bool'},
        'run_type': {'key': 'runType', 'type': 'str'},
        'properties': {'key': 'properties', 'type': '{str}'},
        'script_name': {'key': 'scriptName', 'type': 'str'},
        'target': {'key': 'target', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '{str}'},
        'input_datasets': {'key': 'inputDatasets', 'type': '[Dataset]'},
        'run_definition': {'key': 'runDefinition', 'type': 'object'},
        'created_from': {'key': 'createdFrom', 'type': 'CreatedFromDto'},
        'cancel_uri': {'key': 'cancelUri', 'type': 'str'},
        'diagnostics_uri': {'key': 'diagnosticsUri', 'type': 'str'},
    }

    def __init__(self, run_id=None, parent_run_id=None, status=None, start_time_utc=None, end_time_utc=None, heartbeat_enabled=None, options=None, name=None, data_container_id=None, description=None, hidden=None, run_type=None, properties=None, script_name=None, target=None, tags=None, input_datasets=None, run_definition=None, created_from=None, cancel_uri=None, diagnostics_uri=None):
        super(CreateRunDto, self).__init__()
        self.run_id = run_id
        self.parent_run_id = parent_run_id
        self.status = status
        self.start_time_utc = start_time_utc
        self.end_time_utc = end_time_utc
        self.heartbeat_enabled = heartbeat_enabled
        self.options = options
        self.name = name
        self.data_container_id = data_container_id
        self.description = description
        self.hidden = hidden
        self.run_type = run_type
        self.properties = properties
        self.script_name = script_name
        self.target = target
        self.tags = tags
        self.input_datasets = input_datasets
        self.run_definition = run_definition
        self.created_from = created_from
        self.cancel_uri = cancel_uri
        self.diagnostics_uri = diagnostics_uri
