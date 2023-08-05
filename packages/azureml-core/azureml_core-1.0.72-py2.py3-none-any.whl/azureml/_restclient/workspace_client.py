# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# ---------------------------------------------------------
"""Access workspace client"""
import copy

from azureml._restclient.models import ModifyExperimentDto, DeleteTagsCommandDto

from .clientbase import ClientBase, PAGINATED_KEY

from msrest.exceptions import HttpOperationError
from ._odata.constants import ORDER_BY_CREATEDTIME_EXPRESSION
from ._odata.experiments import get_filter_expression

from .utils import _generate_client_kwargs, _validate_order_by
from .exceptions import ServiceException
from .models.error_response import ErrorResponseException


class WorkspaceClient(ClientBase):
    """
    Run History APIs

    :param host: The base path for the server to call.
    :type host: str
    :param auth: Client authentication
    :type auth: azureml.core.authentication.AbstractAuthentication
    :param subscription_id:
    :type subscription_id: str
    :param resource_group_name:
    :type resource_group_name: str
    :param workspace_name:
    :type workspace_name: str
    """

    def __init__(self, service_context, host=None, **kwargs):
        """
        Constructor of the class.
        """
        self._service_context = service_context
        self._override_host = host
        self._workspace_arguments = [self._service_context.subscription_id,
                                     self._service_context.resource_group_name,
                                     self._service_context.workspace_name]
        super(WorkspaceClient, self).__init__(**kwargs)

        self._custom_headers = {}

    @property
    def auth(self):
        return self._service_context.get_auth()

    def get_rest_client(self, user_agent=None):
        """get service rest client"""
        return self._service_context._get_run_history_restclient(
            host=self._override_host, user_agent=user_agent)

    def get_cluster_url(self):
        """get service url"""
        return self._host

    def get_workspace_uri_path(self):
        return self._service_context._get_workspace_scope()

    def _execute_with_workspace_arguments(self, func, *args, **kwargs):
        return self._execute_with_arguments(func, copy.deepcopy(self._workspace_arguments), *args, **kwargs)

    def _execute_with_arguments(self, func, args_list, *args, **kwargs):
        if not callable(func):
            raise TypeError('Argument is not callable')

        if self._custom_headers:
            kwargs["custom_headers"] = self._custom_headers

        if args:
            args_list.extend(args)
        is_paginated = kwargs.pop(PAGINATED_KEY, False)
        try:
            if is_paginated:
                return self._call_paginated_api(func, *args_list, **kwargs)
            else:
                return self._call_api(func, *args_list, **kwargs)
        except ErrorResponseException as e:
            raise ServiceException(e)

    def get_or_create_experiment(self, experiment_name, is_async=False):
        """
        get or create an experiment by name
        :param experiment_name: experiment name (required)
        :type experiment_name: str
        :param is_async: execute request asynchronously
        :type is_async: bool
        :return:
            If is_async parameter is True,
            the request is called asynchronously.
            The method returns azureml._async_task.AsyncTask object
            If parameter is_async is False or missing,
            return: ~_restclient.models.ExperimentDto
        """

        # Client Create, Get on Conflict
        try:
            return self._execute_with_workspace_arguments(self._client.experiment.create,
                                                          experiment_name=experiment_name,
                                                          is_async=is_async)
        except HttpOperationError as e:
            if e.response.status_code == 409:
                experiment = self._execute_with_workspace_arguments(self._client.experiment.get,
                                                                    experiment_name=experiment_name,
                                                                    is_async=is_async)
                if experiment is None:  # This should never happen
                    raise ServiceException("Failed to get an existing experiment with name " + experiment_name)
            else:
                raise ServiceException(e)

    def list_experiments(self, last=None, order_by=None, experiment_name=None, view_type=None, tags=None):
        """
        list all experiments
        :return: a generator of ~_restclient.models.ExperimentDto
        """

        kwargs = {}
        if last is not None:
            order_by_expression = _validate_order_by(order_by) if order_by else [ORDER_BY_CREATEDTIME_EXPRESSION]
            kwargs = _generate_client_kwargs(top=last, orderby=order_by_expression)
            # TODO: Doesn't work
            raise NotImplementedError("Cannot limit experiment list")

        filter_expression = get_filter_expression(experiment_name=experiment_name, tags=tags)
        filter_expression = None if filter_expression == "" else filter_expression

        kwargs = _generate_client_kwargs(filter=filter_expression, view_type=view_type)

        return self._execute_with_workspace_arguments(self._client.experiment.list,
                                                      is_paginated=True,
                                                      **kwargs)

    def get_experiment(self, experiment_name, is_async=False):
        """
        get experiment by name
        :param experiment_name: experiment name (required)
        :type experiment_name: str
        :param is_async: execute request asynchronously
        :type is_async: bool
        :return:
            If is_async parameter is True,
            the request is called asynchronously.
            The method returns azureml._async_task.AsyncTask object
            If parameter is_async is False or missing,
            return: ~_restclient.models.ExperimentDto
        """

        return self._execute_with_workspace_arguments(self._client.experiment.get,
                                                      experiment_name=experiment_name,
                                                      is_async=is_async)

    def get_experiment_by_id(self, experiment_id, is_async=False):
        """
        get experiment by id
        :param experiment_id: experiment id (required)
        :type experiment_id: str
        :param is_async: execute request asynchronously
        :type is_async: bool
        :return:
            If is_async parameter is True,
            the request is called asynchronously.
            The method returns azureml._async_task.AsyncTask object
            If parameter is_async is False or missing,
            return: ~_restclient.models.ExperimentDto
        """

        return self._execute_with_workspace_arguments(self._client.experiment.get_by_id,
                                                      experiment_id=experiment_id,
                                                      is_async=is_async)

    def archive_experiment(self, experiment_id, caller=None, custom_headers=None, is_async=False):
        """
        Archive the experiment
        :param experiment_id: experiment id (required)
        :type experiment_id: str
        :param is_async: execute request asynchronously
        :type is_async: bool
        :param caller: caller function name (optional)
        :type caller: optional[string]
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_headers: optional[dict]
        :return:
            the return type is based on is_async parameter.
            If is_async parameter is True,
            the request is called asynchronously.
        rtype: ~_restclient.models.ExperimentDto (is_async is False) or
            azureml._async.AsyncTask (is_async is True)
        """
        modify_experiment_dto = ModifyExperimentDto(archive=True)
        return self.update_experiment(experiment_id, modify_experiment_dto, caller, custom_headers, is_async)

    def reactivate_experiment(self, experiment_id, new_name=None, caller=None, custom_headers=None, is_async=False):
        """
        Reactivate an archived experiment
        :param experiment_id: experiment id (required)
        :type experiment_id: str
        :param new_name: new experiment name (optional)
        :type new_name: str
        :param is_async: execute request asynchronously
        :type is_async: bool
        :param caller: caller function name (optional)
        :type caller: optional[string]
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_headers: optional[dict]
        :return:
            the return type is based on is_async parameter.
            If is_async parameter is True,
            the request is called asynchronously.
        rtype: ~_restclient.models.ExperimentDto (is_async is False) or
            azureml._async.AsyncTask (is_async is True)
        """
        modify_experiment_dto = ModifyExperimentDto(archive=False, name=new_name)
        return self.update_experiment(experiment_id, modify_experiment_dto, caller, custom_headers, is_async)

    def set_tags(self, experiment_id, tags=None, caller=None, custom_headers=None, is_async=False):
        """
        Modify the tags on an experiment
        :param experiment_id: experiment id (required)
        :type experiment_id: str
        :param tags: tags to modify (optional)
        :type tags: dict[str]
        :param is_async: execute request asynchronously
        :type is_async: bool
        :param caller: caller function name (optional)
        :type caller: optional[string]
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_headers: optional[dict]
        :return:
            the return type is based on is_async parameter.
            If is_async parameter is True,
            the request is called asynchronously.
        rtype: ~_restclient.models.ExperimentDto (is_async is False) or
            azureml._async.AsyncTask (is_async is True)
        """
        sanitized_tags = self._sanitize_tags(tags)
        modify_experiment_dto = ModifyExperimentDto(tags=sanitized_tags)
        return self.update_experiment(experiment_id, modify_experiment_dto, caller, custom_headers, is_async)

    def update_experiment(self, experiment_id, modify_experiment_dto,
                          caller=None, custom_headers=None, is_async=False):
        """
        Update the experiment
        :param experiment_id: experiment id (required)
        :type experiment_id: str
        :param modify_experiment_dto: modify experiment dto
        :type modify_experiment_dto: ModifyExperimentDto
        :param is_async: execute request asynchronously
        :type is_async: bool
        :param caller: caller function name (optional)
        :type caller: optional[string]
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_headers: optional[dict]
        :return:
            the return type is based on is_async parameter.
            If is_async parameter is True,
            the request is called asynchronously.
        rtype: ~_restclient.models.ExperimentDto (is_async is False) or
            azureml._async.AsyncTask (is_async is True)
        """
        kwargs = _generate_client_kwargs(
            modify_experiment_dto=modify_experiment_dto,
            is_async=is_async, caller=caller, custom_headers=custom_headers)
        return self._execute_with_workspace_arguments(
            self._client.experiment.update, experiment_id=experiment_id, **kwargs)

    def delete_experiment_tags(self, experiment_id, tags, caller=None, custom_headers=None, is_async=False):
        """
        Delete the specified tags from the experiment
        :param experiment_id: experiment id (required)
        :type experiment_id: str
        :param tags: tag keys to delete
        :type tags: [str]
        :param is_async: execute request asynchronously
        :type is_async: bool
        :param caller: caller function name (optional)
        :type caller: optional[string]
        :param custom_headers: headers that will be added to the request (optional)
        :type custom_headers: optional[dict]
        :return:
            the return type is based on is_async parameter.
            If is_async parameter is True,
            the request is called asynchronously.
        rtype: ~_restclient.models.DeleteExperimentTagsResult (is_async is False) or
            azureml._async.AsyncTask (is_async is True)
        """
        if tags is None:
            return
        tags = DeleteTagsCommandDto(tags)
        kwargs = _generate_client_kwargs(is_async, caller=caller, custom_headers=custom_headers)

        return self._execute_with_workspace_arguments(
            self._client.experiment.delete_tags, experiment_id=experiment_id, delete_tags_command=tags, **kwargs)

    def _sanitize_tags(self, tag_or_prop_dict):
        # type: (...) -> {str}
        ret_tags = {}
        # dict comprehension would be nice but logging suffers without more functions
        for key, val in tag_or_prop_dict.items():
            if not isinstance(val, (str, type(None))):  # should be six.str/basestring or something
                self._logger.warn('Converting non-string tag to string: (%s: %s)', key, val)
                ret_tags[key] = str(val)
            else:
                ret_tags[key] = val
        return ret_tags
