# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains helper methods for dataprep."""


def dataprep():
    try:
        import azureml.dataprep as _dprep
        return _dprep
    except ImportError:
        raise ImportError(_dataprep_missing_error)


def dataprep_fuse():
    try:
        import azureml.dataprep.fuse.dprepfuse as _dprep_fuse
        return _dprep_fuse
    except ImportError:
        raise ImportError(_dataprep_missing_error)


def ensure_dataflow(dataflow):
    if not isinstance(dataflow, dataprep().Dataflow):
        raise RuntimeError('dataflow must be instance of azureml.dataprep.Dataflow')


def get_dataflow_for_execution(dataflow, action, source, **kwargs):
    from copy import deepcopy
    meta = deepcopy(dataflow._meta)
    if 'activityApp' not in meta:
        meta['activityApp'] = source
    if 'activity' not in meta:
        meta['activity'] = action
    if len(kwargs) > 0:
        kwargs.update(meta)
        meta = kwargs
    return dataprep().Dataflow(dataflow._engine_api, dataflow._steps, meta)


_dataprep_missing_error = (
    'Could not import package "azureml-dataprep". Please ensure it is installed by running: ' +
    'pip install "azureml-dataprep[fuse,pandas]"'
)
