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


class ActionDto(Model):
    """ActionDto.

    :param action_id:
    :type action_id: str
    :param action_type:
    :type action_type: str
    :param definition_version:
    :type definition_version: str
    :param dataflow_artifact_id:
    :type dataflow_artifact_id: str
    :param dataset_snapshot_name:
    :type dataset_snapshot_name: str
    :param workspace_id:
    :type workspace_id: str
    :param dataset_id:
    :type dataset_id: str
    :param compute_target:
    :type compute_target: str
    :param arguments:
    :type arguments: dict[str, str]
    :param result_artifact_ids:
    :type result_artifact_ids: list[str]
    :param experiment_name:
    :type experiment_name: str
    :param run_id:
    :type run_id: str
    :param created_time:
    :type created_time: datetime
    :param status:
    :type status: str
    :param error:
    :type error: ~_restclient.models.ErrorResponse
    :param warnings:
    :type warnings: list[~_restclient.models.RunDetailsWarningDto]
    :param start_time_utc:
    :type start_time_utc: datetime
    :param end_time_utc:
    :type end_time_utc: datetime
    :param is_up_to_date:
    :type is_up_to_date: bool
    :param is_up_to_date_error:
    :type is_up_to_date_error: str
    """

    _attribute_map = {
        'action_id': {'key': 'actionId', 'type': 'str'},
        'action_type': {'key': 'actionType', 'type': 'str'},
        'definition_version': {'key': 'definitionVersion', 'type': 'str'},
        'dataflow_artifact_id': {'key': 'dataflowArtifactId', 'type': 'str'},
        'dataset_snapshot_name': {'key': 'datasetSnapshotName', 'type': 'str'},
        'workspace_id': {'key': 'workspaceId', 'type': 'str'},
        'dataset_id': {'key': 'datasetId', 'type': 'str'},
        'compute_target': {'key': 'computeTarget', 'type': 'str'},
        'arguments': {'key': 'arguments', 'type': '{str}'},
        'result_artifact_ids': {'key': 'resultArtifactIds', 'type': '[str]'},
        'experiment_name': {'key': 'experimentName', 'type': 'str'},
        'run_id': {'key': 'runId', 'type': 'str'},
        'created_time': {'key': 'createdTime', 'type': 'iso-8601'},
        'status': {'key': 'status', 'type': 'str'},
        'error': {'key': 'error', 'type': 'ErrorResponse'},
        'warnings': {'key': 'warnings', 'type': '[RunDetailsWarningDto]'},
        'start_time_utc': {'key': 'startTimeUtc', 'type': 'iso-8601'},
        'end_time_utc': {'key': 'endTimeUtc', 'type': 'iso-8601'},
        'is_up_to_date': {'key': 'isUpToDate', 'type': 'bool'},
        'is_up_to_date_error': {'key': 'isUpToDateError', 'type': 'str'},
    }

    def __init__(self, action_id=None, action_type=None, definition_version=None, dataflow_artifact_id=None, dataset_snapshot_name=None, workspace_id=None, dataset_id=None, compute_target=None, arguments=None, result_artifact_ids=None, experiment_name=None, run_id=None, created_time=None, status=None, error=None, warnings=None, start_time_utc=None, end_time_utc=None, is_up_to_date=None, is_up_to_date_error=None):
        super(ActionDto, self).__init__()
        self.action_id = action_id
        self.action_type = action_type
        self.definition_version = definition_version
        self.dataflow_artifact_id = dataflow_artifact_id
        self.dataset_snapshot_name = dataset_snapshot_name
        self.workspace_id = workspace_id
        self.dataset_id = dataset_id
        self.compute_target = compute_target
        self.arguments = arguments
        self.result_artifact_ids = result_artifact_ids
        self.experiment_name = experiment_name
        self.run_id = run_id
        self.created_time = created_time
        self.status = status
        self.error = error
        self.warnings = warnings
        self.start_time_utc = start_time_utc
        self.end_time_utc = end_time_utc
        self.is_up_to_date = is_up_to_date
        self.is_up_to_date_error = is_up_to_date_error
