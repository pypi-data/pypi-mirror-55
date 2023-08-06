from pydnameth.scripts.develop.table import table_z_test_linreg, table_ancova, table_aggregator_linreg, table_aggregator_variance
from pydnameth.config.experiment.types import DataType


def entropy_table_z_test_linreg(
    data,
    annotations,
    attributes,
    observables_list,
    data_params=None,
    task_params=None,
    method_params=None
):
    table_z_test_linreg(
        data_type=DataType.entropy,
        data=data,
        annotations=annotations,
        attributes=attributes,
        observables_list=observables_list,
        data_params=data_params,
        task_params=task_params,
        method_params=method_params
    )


def entropy_table_ancova(
    data,
    annotations,
    attributes,
    observables_list,
    data_params=None,
    task_params=None,
    method_params=None
):
    table_ancova(
        data_type=DataType.entropy,
        data=data,
        annotations=annotations,
        attributes=attributes,
        observables_list=observables_list,
        data_params=data_params,
        task_params=task_params,
        method_params=method_params
    )


def entropy_table_aggregator_linreg(
    data,
    annotations,
    attributes,
    observables_list,
    data_params=None,
    method_params=None
):
    table_aggregator_linreg(
        DataType.entropy,
        data,
        annotations,
        attributes,
        observables_list,
        data_params,
        method_params,
    )


def entropy_table_aggregator_variance(
    data,
    annotations,
    attributes,
    observables_list,
    data_params,
):
    table_aggregator_variance(
        DataType.entropy,
        data,
        annotations,
        attributes,
        observables_list,
        data_params=data_params,
    )
