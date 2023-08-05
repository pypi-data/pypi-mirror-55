# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Access base class to handle _restclient calls"""
import copy
import json
import logging
import os
import time
import uuid

from json import JSONEncoder
from abc import ABCMeta, abstractmethod
from six import raise_from, add_metaclass

from .constants import (ATTRIBUTE_CONTINUATION_TOKEN_NAME, ATTRIBUTE_VALUE_NAME, CUSTOM_HEADERS_KEY, QUERY_PARAMS_KEY,
                        RequestHeaders)
from .._base_sdk_common import _ClientSessionId

from azureml._async import AsyncTask, WorkerPool
from azureml._logging import ChainedIdentity
from azureml.exceptions import UserErrorException
from msrest.serialization import Model
from msrest.exceptions import HttpOperationError

from .retry_exceptions import RETRY_EXCEPTIONS

try:
    from azureml.telemetry.log_scope import LogScope
    _telemetry_enabled = True
except ImportError:
    _telemetry_enabled = False

NUMBER_TO_DOWNLOAD = "total_count"
ASYNC_KEY = "is_async"
PAGINATED_KEY = "is_paginated"
NEW_IDENT = "new_ident"

DEFAULT_BACKOFF_ENV_VAR = "AZUREML_DEFAULT_BACKOFF"
DEFAULT_RETRIES_ENV_VAR = "AZUREML_DEFAULT_RETRIES"
DEFAULT_503_BACKOFF_ENV_VAR = "AZUREML_DEFAULT_503_BACKOFF"

DEFAULT_BACKOFF = int(os.environ.get(DEFAULT_BACKOFF_ENV_VAR, "32"))
DEFAULT_RETRIES = int(os.environ.get(DEFAULT_RETRIES_ENV_VAR, "3"))
DEFAULT_503_BACKOFF = int(os.environ.get(DEFAULT_503_BACKOFF_ENV_VAR, "2"))

module_logger = logging.getLogger(__name__)


def execute_func_custom(backoff, retries, func, *args, **kwargs):
    backoff = DEFAULT_BACKOFF if backoff is None else backoff
    retries = DEFAULT_RETRIES if retries is None else retries
    return ClientBase._execute_func_internal(backoff, retries, module_logger, func, _noop_reset, *args, **kwargs)


def execute_func_with_reset(backoff, retries, func, reset_func, *args, **kwargs):
    """
    Execute a function with backoff and up to retries count retries. If a retry is required, run reset_func on
    *args and **kwargs prior to retrying the function.
    :param backoff:
    :param retries:
    :param func:
    :param reset_func: function that modifies *args and **kwargs to undo side-effects of func.
    Example is resetting a stream to it's original position.
    :param args:
    :param kwargs:
    :return:
    """
    backoff = DEFAULT_BACKOFF if backoff is None else backoff
    retries = DEFAULT_RETRIES if retries is None else retries
    return ClientBase._execute_func_internal(backoff, retries, module_logger, func, reset_func, *args, **kwargs)


def _noop_reset(*args, **kwargs):
    pass


class _ErrorEncoder(JSONEncoder):
    def default(self, obj):
        return getattr(obj, "__dict__", {})


@add_metaclass(ABCMeta)
class ClientBase(ChainedIdentity):
    """
    Client Base class

    :param host: The base path for the server to call.
    :type host: str
    :param auth: Client authentication
    :type auth: azureml.core.authentication.AbstractAuthentication
    """
    _worker_pool = None

    def __init__(self, worker_pool=None, logger=None, user_agent=None, **kwargs):
        """
        Constructor of the class.
        """

        # TODO: Resolve _restclient's dependency on core so this block can be moved
        from azureml._restclient.models import (DebugInfoResponse, InnerErrorResponse, RootError,
                                                ErrorResponse)

        def pretty_print(self):
            return json.dumps(self, indent=4, cls=_ErrorEncoder)

        classes_to_pretty_print = [DebugInfoResponse, InnerErrorResponse, RootError, ErrorResponse]
        for class_to_pretty_print in classes_to_pretty_print:
            class_to_pretty_print.__str__ = class_to_pretty_print.__repr__ = pretty_print
        # end TODO block

        super(ClientBase, self).__init__(**kwargs)
        if logger is not None:
            self._logger.warning("Deprecated kwarg logger, renamed to _parent_logger. "
                                 "logger kwarg was ignored.")

        self._client = self.get_rest_client(user_agent=user_agent)
        # Enable logging for all requests and responses if log level is logging.DEBUG
        # logs request body and response body, does not log authentication tokens
        self._client.config.enable_http_logger = True
        # We override a config in the retry policy to throw exceptions after retry.
        # By default this is True. We set it to false to get the full error trace, including url and
        # status code of the last retry. Otherwise, the error message is 'too many 500 error responses',
        # which is not useful.
        self._client.config.retry_policy.policy.raise_on_status = False

        self._pool = worker_pool if worker_pool is not None else ClientBase._get_worker_pool()

    @property
    def retries(self):
        """Total number of allowed retries."""
        return self._client.config.retry_policy.retries

    @retries.setter
    def retries(self, value):
        self._client.config.retry_policy.retries = value

    @property
    def backoff_factor(self):
        """
        Factor by which back-off delay is incrementally increased.
        back-off delay = {backoff factor} * (2 ^ ({number of total retries} - 1))
        """
        return self._client.config.retry_policy.backoff_factor

    @backoff_factor.setter
    def backoff_factor(self, value):
        self._client.config.retry_policy.backoff_factor = value

    @property
    def max_backoff(self):
        """Max retry back-off delay."""
        return self._client.config.retry_policy.max_backoff

    @max_backoff.setter
    def max_backoff(self, value):
        self._client.config.retry_policy.max_backoff = value

    @abstractmethod
    def get_rest_client(self, user_agent=None):
        """get service rest client"""
        raise NotImplementedError

    @classmethod
    def _get_worker_pool(cls):
        if cls._worker_pool is None:
            cls._worker_pool = WorkerPool(_parent_logger=module_logger)
            module_logger.info("Created a worker pool for first use")
        return cls._worker_pool

    @property
    def _host(self):
        return self._client.config.base_url

    @property
    def auth(self):
        return self._client.config.credentials

    def _call_api(self, func, *args, **kwargs):
        """make a function call with arguments
        This method makes a synchronous call by default. To make an
        asynchronous call, please pass is_async=True
        >>> task = self.call_api(func, *args, **kwargs, is_async=True)
        >>> result = task.wait()

        :param func function object: function to execute
        :param is_async bool: execute request asynchronously
        :param args list: list of arguments
        :param kwargs dict: arguments as dictionary
        :return:
            If is_async parameter is True,
            the request is called asynchronously.
            The method returns azureml._async.AsyncTask object
            If parameter is_async is False or missing,
            the method returns the response directly.
        """
        if not callable(func):
            raise TypeError("Argument is not callable")

        is_async = kwargs.pop(ASYNC_KEY, False)

        custom_headers = kwargs.pop(CUSTOM_HEADERS_KEY, {})
        # handle x-ms-client-request-id and request-id header
        ClientBase._add_request_id_to_headers(custom_headers)

        # get correlation info from log scope and add to correlation context header
        if _telemetry_enabled:
            ctx = LogScope.get_current()
            if ctx is not None:
                ClientBase._add_ctx_info_to_headers(custom_headers, ctx, _ClientSessionId)

        kwargs[CUSTOM_HEADERS_KEY] = custom_headers

        with self._log_context("{}-async:{}".format(func.__name__, is_async)):
            if is_async:
                future = self._pool.submit(self._execute_with_base_arguments, func, *args, **kwargs)
                new_ident = kwargs.pop(NEW_IDENT, None)
                ident = new_ident if new_ident is not None else func.__name__
                return AsyncTask(future, _ident=ident, _parent_logger=self._logger)
            else:
                return self._execute_with_base_arguments(func, *args, **kwargs)

    def _call_paginated_api(self, func, *args, **kwargs):
        """make a paginated api call with arguments
        :param func function object: function to execute
        :param total_count int: the most number of items to return
        :param args list: list of arguments
        :param kwargs dict: arguments as dictionary
        :return:
            a generator of dto_items
        """
        if not callable(func):
            raise TypeError("Argument is not callable")

        total = kwargs.pop(NUMBER_TO_DOWNLOAD, 0)
        kwargs[ASYNC_KEY] = True
        count = 0
        next_page = self._call_api(func, *args, **kwargs)
        while (True):
            paginated_dto = next_page.wait(awaiter_name="ApiPagination")
            if not paginated_dto:
                break

            token = ClientBase._get_attribute(paginated_dto, ATTRIBUTE_CONTINUATION_TOKEN_NAME)
            if token:
                existing_token = kwargs.get(ATTRIBUTE_CONTINUATION_TOKEN_NAME, None)
                if existing_token == token:
                    token = None
                else:
                    if QUERY_PARAMS_KEY in kwargs:
                        setattr(kwargs[QUERY_PARAMS_KEY], ATTRIBUTE_CONTINUATION_TOKEN_NAME, token)
                    else:
                        kwargs[ATTRIBUTE_CONTINUATION_TOKEN_NAME] = token
                    next_page = self._call_api(func, *args, **kwargs)

            value_as_list = ClientBase._get_attribute(paginated_dto, ATTRIBUTE_VALUE_NAME)
            if not value_as_list:
                break

            for dto in value_as_list:
                if getattr(dto, "hidden", False) is not True:
                    yield dto
                count += 1
                if count == total:
                    return

            if not token:
                break

    def _execute_with_base_arguments(self, func, *args, **kwargs):
        back_off = self.backoff_factor
        total_retry = 0 if self.retries < 0 else self.retries
        return ClientBase._execute_func_internal(
            back_off, total_retry, self._logger, func, _noop_reset, *args, **kwargs)

    @classmethod
    def _execute_func_internal(cls, back_off, total_retry, logger, func, reset_func, *args, **kwargs):
        if not callable(func):
            raise TypeError("Argument func is not callable")

        if not callable(reset_func):
            raise TypeError("Argument reset_func is not callable")

        left_retry = total_retry
        while left_retry >= 0:
            try:
                return func(*args, **kwargs)
            except Exception as error:
                left_retry = cls._handle_retry(back_off, left_retry, total_retry, error, logger, func)

            reset_func(*args, **kwargs)  # reset_func is expected to undo any side effects from a failed func call.

    @classmethod
    def _execute_func(cls, func, *args, **kwargs):
        return cls._execute_func_internal(
            DEFAULT_BACKOFF, DEFAULT_RETRIES, module_logger, func, _noop_reset, *args, **kwargs)

    @classmethod
    def _handle_retry(cls, back_off, left_retry, total_retry, error, logger, func):
        """
        Apply backoff for the current retry if retries are available

        :param back_off: Base value for backoff time in seconds.
        :type back_off: int
        :param left_retry: Remaining retry budget.
        :type left_retry: int
        :param total_retry: Total retry budget.
        :type total_retry: int
        :param error: The raised error.
        :type error: int
        :param logger:
        :type logger: logging.Logger
        :param func: The called function.
        :type func: function
        :return: The amount of retries remaining.
        :rtype: int
        """
        if left_retry == 0:
            raise error
        elif isinstance(error, HttpOperationError):
            if error.response.status_code == 403:
                error_msg = """
Operation returned an invalid status code 'Forbidden'. The possible reason could be:
1. You are not authorized to access this resource, or directory listing denied.
2. you may not login your azure service, or use other subscription, you can check your
default account by running azure cli commend:
'az account list -o table'.
3. You have multiple objects/login session opened, please close all session and try again.
                """
                raise_from(UserErrorException(error_msg), error)

            elif error.response.status_code == 429:
                logger.debug("There were too many requests. Try again soon.")
                back_off = DEFAULT_BACKOFF
            elif error.response.status_code == 503:
                back_off = DEFAULT_503_BACKOFF
            elif error.response.status_code < 500:
                raise error
        elif not isinstance(error, RETRY_EXCEPTIONS):
            raise error

        delay = back_off * 2 ** (total_retry - left_retry)

        left_retry -= 1

        logger.debug("Retrying operation: {} failed with Error: {}, Delay: {}, and Retry count: {}.".format(
            str(func), error, delay, total_retry - left_retry))
        time.sleep(delay)

        return left_retry

    def _combine_paginated_base(self, exec_func, func, count_to_download=0, *args, **kwargs):
        if not callable(exec_func):
            raise TypeError("Argument is not callable")

        paginated_dto = exec_func(func,
                                  *args,
                                  **kwargs)

        not_exists = "Not_Exists"
        is_return_as_dict = kwargs.get("return_as_dict", True)
        token = getattr(
            paginated_dto, ATTRIBUTE_CONTINUATION_TOKEN_NAME, not_exists)
        if token == not_exists:
            raise TypeError("property '{0}' is expected in return of function '{1}'."
                            .format(ATTRIBUTE_CONTINUATION_TOKEN_NAME, func.__name__))

        value = getattr(paginated_dto, ATTRIBUTE_VALUE_NAME, not_exists)
        if value == not_exists:
            raise TypeError("property '{0}' is expected in return of function '{1}'."
                            .format(ATTRIBUTE_VALUE_NAME, func.__name__))

        is_get_all_data = count_to_download < 1
        data = []
        if is_return_as_dict:
            data.extend(v.__dict__ for v in value)
        else:
            data.extend(value)
        total_item_got = len(data)
        more_to_come = is_get_all_data if is_get_all_data else count_to_download > total_item_got

        if not kwargs:
            kwargs_copy = dict()
        else:
            kwargs_copy = copy.deepcopy(kwargs)

        data_list = []
        while token and more_to_come is True:
            kwargs_copy[ATTRIBUTE_CONTINUATION_TOKEN_NAME] = token
            paginated_dto = exec_func(func,
                                      *args,
                                      **kwargs_copy)
            if is_return_as_dict:
                data_list.extend(v.__dict__ for v in getattr(
                    paginated_dto, ATTRIBUTE_VALUE_NAME))
            else:
                data_list.extend(getattr(paginated_dto, ATTRIBUTE_VALUE_NAME))

            data.extend(data_list)
            token = getattr(paginated_dto, ATTRIBUTE_CONTINUATION_TOKEN_NAME)
            total_item_got += len(data_list)
            more_to_come = is_get_all_data if is_get_all_data else count_to_download > total_item_got
            del data_list[:]

        if is_get_all_data is False and total_item_got > count_to_download:
            del data[count_to_download:total_item_got]
        return data

    @staticmethod
    def dto_to_dictionary(dto, keep_readonly=True, key_transformer=None):
        """Return a dict that can be JSONify using json.dump.
        :param ~_restclient.models dto: object to transform
        :param bool keep_readonly: If you want to serialize the readonly attributes
        :param function key_transformer: A key transformer function.
                                         Example: attribute_transformer() in msrest.serialization.
        :returns: A dict JSON compatible object
        :rtype: dict
        """
        if dto is None:
            return None

        if not isinstance(dto, Model):
            raise TypeError("Argument is not a Model type")

        if key_transformer is not None:
            return dto.as_dict(keep_readonly=keep_readonly, key_transformer=key_transformer)

        return dto.as_dict(keep_readonly=keep_readonly)

    @staticmethod
    def _get_attribute(value, attr_name):
        try:
            return getattr(value, attr_name)
        except AttributeError:
            raise AttributeError("property '{0}' is expected in object type '{1}'."
                                 .format(attr_name, type(value)))

    @staticmethod
    def _add_request_id_to_headers(headers):
        if RequestHeaders.CLIENT_REQUEST_ID in headers:
            client_request_id = headers[RequestHeaders.CLIENT_REQUEST_ID]
        else:
            client_request_id = str(uuid.uuid4())
            headers[RequestHeaders.CLIENT_REQUEST_ID] = client_request_id

        if RequestHeaders.REQUEST_ID not in headers:
            headers[RequestHeaders.REQUEST_ID] = client_request_id

    @staticmethod
    def _add_ctx_info_to_headers(headers, ctx, client_session_id):
        component_name = ctx['ComponentName'] or ctx.component_name
        ctx_info = dict(
            ScopeId=ctx.id, ClientComponentName=component_name, ClientSessionId=client_session_id
        )
        correlation_context = headers.get(RequestHeaders.CORRELATION_CONTEXT, "")
        ctx_info_str = ','.join(map(lambda kv: "{}={}".format(kv[0], kv[1]), ctx_info.items()))
        correlation_context = \
            ctx_info_str if len(correlation_context) == 0 else ','.join([correlation_context, ctx_info_str])
        headers[RequestHeaders.CORRELATION_CONTEXT] = correlation_context
