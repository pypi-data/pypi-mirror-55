import copy
from anytree import Node
from pydnameth.config.config import Config
from pydnameth.config.experiment.types import Task, Method
from pydnameth.config.experiment.experiment import Experiment
from pydnameth.config.attributes.attributes import Observables, Cells, Attributes
from pydnameth.model.tree import build_tree, calc_tree


def table(
    data,
    annotations,
    attributes,
    data_type,
    method,
    data_params=None,
    task_params=None,
    method_params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            data=data_type,
            task=Task.table,
            method=method,
            data_params=copy.deepcopy(data_params),
            task_params=copy.deepcopy(task_params),
            method_params=copy.deepcopy(method_params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True
    )

    root = Node(name=str(config_root), config=config_root)
    build_tree(root)
    calc_tree(root)


def table_aggregator_linreg(
    data_type,
    data,
    annotations,
    attributes,
    observables_list,
    data_params=None,
    task_params=None,
    method_params=None
):
    child_methods_lvl_1 = [Method.polygon, Method.z_test_linreg]
    child_methods_lvl_2 = [Method.linreg]

    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            data=data_type,
            task=Task.table,
            method=Method.aggregator,
            data_params=copy.deepcopy(data_params),
            task_params=copy.deepcopy(task_params),
            method_params=copy.deepcopy(method_params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True
    )
    root = Node(name=str(config_root), config=config_root)

    for child_method_lvl_1 in child_methods_lvl_1:

        if child_method_lvl_1 == Method.polygon:
            method_params = {'method': Method.linreg}
            is_load_child = True
        elif child_method_lvl_1 == Method.z_test_linreg:
            method_params = {}
            is_load_child = True
        elif child_method_lvl_1 == Method.ancova:
            method_params = {}
            is_load_child = True
        else:
            method_params = {}
            is_load_child = False

        config_lvl_1 = Config(
            data=copy.deepcopy(data),
            experiment=Experiment(
                data=data_type,
                task=Task.table,
                method=child_method_lvl_1,
                data_params=copy.deepcopy(data_params),
                method_params=method_params
            ),
            annotations=copy.deepcopy(annotations),
            attributes=copy.deepcopy(attributes),
            is_run=True,
            is_root=False,
            is_load_child=is_load_child
        )
        node_lvl_1 = Node(name=str(config_lvl_1), config=config_lvl_1, parent=root)

        for child_method_lvl_2 in child_methods_lvl_2:
            for d in observables_list:
                observables_lvl_2 = Observables(
                    name=copy.deepcopy(attributes.observables.name),
                    types=d
                )

                cells_lvl_2 = Cells(
                    name=copy.deepcopy(attributes.cells.name),
                    types=copy.deepcopy(attributes.cells.types)
                )

                attributes_lvl_2 = Attributes(
                    target=copy.deepcopy(attributes.target),
                    observables=observables_lvl_2,
                    cells=cells_lvl_2,
                )

                config_lvl_2 = Config(
                    data=copy.deepcopy(data),
                    experiment=Experiment(
                        data=data_type,
                        task=Task.table,
                        method=copy.deepcopy(child_method_lvl_2),
                        data_params=copy.deepcopy(data_params),
                    ),
                    annotations=copy.deepcopy(annotations),
                    attributes=attributes_lvl_2,
                    is_run=True,
                    is_root=False,
                    is_load_child=is_load_child
                )
                Node(name=str(config_lvl_2), config=config_lvl_2, parent=node_lvl_1)

    build_tree(root)
    calc_tree(root)


def table_z_test_linreg(
    data_type,
    data,
    annotations,
    attributes,
    observables_list,
    data_params=None,
    task_params=None,
    method_params=None
):

    config_z_test_linreg = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            data=data_type,
            task=Task.table,
            method=Method.z_test_linreg,
            data_params=copy.deepcopy(data_params),
            method_params=method_params,
            task_params=task_params
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=False
    )
    root = Node(name=str(config_z_test_linreg), config=config_z_test_linreg)

    for d in observables_list:
        observables_linreg = Observables(
            name=copy.deepcopy(attributes.observables.name),
            types=d
        )

        cells_linreg = Cells(
            name=copy.deepcopy(attributes.cells.name),
            types=copy.deepcopy(attributes.cells.types)
        )

        attributes_linreg = Attributes(
            target=copy.deepcopy(attributes.target),
            observables=observables_linreg,
            cells=cells_linreg,
        )

        config_linreg = Config(
            data=copy.deepcopy(data),
            experiment=Experiment(
                data=data_type,
                task=Task.table,
                method=Method.linreg,
                data_params=copy.deepcopy(data_params),
            ),
            annotations=copy.deepcopy(annotations),
            attributes=attributes_linreg,
            is_run=True,
            is_root=False
        )
        Node(name=str(config_linreg), config=config_linreg, parent=root)

    build_tree(root)
    calc_tree(root)


def table_ancova(
    data_type,
    data,
    annotations,
    attributes,
    observables_list,
    data_params=None,
    task_params=None,
    method_params=None
):

    config_ancova = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            data=data_type,
            task=Task.table,
            method=Method.ancova,
            data_params=copy.deepcopy(data_params),
            method_params=method_params,
            task_params=task_params
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True,
        is_load_child=False,
    )
    root = Node(name=str(config_ancova), config=config_ancova)

    for d in observables_list:
        observables_linreg = Observables(
            name=copy.deepcopy(attributes.observables.name),
            types=d
        )

        cells_linreg = Cells(
            name=copy.deepcopy(attributes.cells.name),
            types=copy.deepcopy(attributes.cells.types)
        )

        attributes_linreg = Attributes(
            target=copy.deepcopy(attributes.target),
            observables=observables_linreg,
            cells=cells_linreg,
        )

        config_linreg = Config(
            data=copy.deepcopy(data),
            experiment=Experiment(
                data=data_type,
                task=Task.table,
                method=Method.linreg,
                data_params=copy.deepcopy(data_params),
            ),
            annotations=copy.deepcopy(annotations),
            attributes=attributes_linreg,
            is_run=False,
            is_root=False
        )
        Node(name=str(config_linreg), config=config_linreg, parent=root)

    build_tree(root)
    calc_tree(root)


def table_aggregator_variance(
    data_type,
    data,
    annotations,
    attributes,
    observables_list,
    data_params,
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            data=data_type,
            task=Task.table,
            method=Method.aggregator,
            data_params=copy.deepcopy(data_params),
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True
    )
    root = Node(name=str(config_root), config=config_root)

    config_lvl_1 = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            data=data_type,
            task=Task.table,
            method=Method.polygon,
            data_params=copy.deepcopy(data_params),
            method_params={'method': Method.variance}
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=False
    )
    node_lvl_1 = Node(name=str(config_lvl_1), config=config_lvl_1, parent=root)

    for d in observables_list:
        observables_lvl_2 = Observables(
            name=copy.deepcopy(attributes.observables.name),
            types=d
        )

        cells_lvl_2 = Cells(
            name=copy.deepcopy(attributes.cells.name),
            types=copy.deepcopy(attributes.cells.types)
        )

        attributes_lvl_2 = Attributes(
            target=copy.deepcopy(attributes.target),
            observables=observables_lvl_2,
            cells=cells_lvl_2,
        )

        config_lvl_2 = Config(
            data=copy.deepcopy(data),
            experiment=Experiment(
                data=data_type,
                task=Task.table,
                method=Method.variance,
                data_params=copy.deepcopy(data_params),
                method_params={
                    'semi_window': 8,
                    'box_b': 'Q5',
                    'box_t': 'Q95',
                }
            ),
            annotations=copy.deepcopy(annotations),
            attributes=attributes_lvl_2,
            is_run=True,
            is_root=False
        )
        Node(name=str(config_lvl_2), config=config_lvl_2, parent=node_lvl_1)

    cluster_types = copy.deepcopy(observables_list[0])
    cluster_types.pop('gender', None)
    cluster_types.pop('sex', None)
    observables_cluster = Observables(
        name=copy.deepcopy(attributes.observables.name),
        types=cluster_types
    )

    cells_cluster = Cells(
        name=copy.deepcopy(attributes.cells.name),
        types=copy.deepcopy(attributes.cells.types)
    )

    attributes_cluster = Attributes(
        target=copy.deepcopy(attributes.target),
        observables=observables_cluster,
        cells=cells_cluster,
    )

    config_cluster = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            data=data_type,
            task=Task.table,
            method=Method.cluster,
            data_params=copy.deepcopy(data_params),
            method_params={
                'eps': 0.2,
                'min_samples_percentage': 1
            }
        ),
        annotations=copy.deepcopy(annotations),
        attributes=attributes_cluster,
        is_run=True,
        is_root=False
    )
    Node(name=str(config_cluster), config=config_cluster, parent=root)

    build_tree(root)
    calc_tree(root)
