import copy
from anytree import Node
from pydnameth.config.config import Config
from pydnameth.config.experiment.types import Task, Method
from pydnameth.config.experiment.experiment import Experiment
from pydnameth.config.attributes.attributes import Observables, Cells, Attributes
from pydnameth.model.tree import build_tree, calc_tree


def plot_scatter(
    data_type,
    data,
    annotations,
    attributes,
    observables_list,
    child_method=Method.linreg,
    data_params=None,
    method_params=None
):
    task_params = {'type': 'run'}

    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            data=data_type,
            task=Task.plot,
            method=Method.scatter,
            data_params=copy.deepcopy(data_params),
            method_params=copy.deepcopy(method_params),
            task_params=task_params
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True,
        is_load_child=False
    )

    root = Node(name=str(config_root), config=config_root)

    for d in observables_list:
        observables_child = Observables(
            name=copy.deepcopy(attributes.observables.name),
            types=d
        )

        cells_child = Cells(
            name=copy.deepcopy(attributes.cells.name),
            types=copy.deepcopy(attributes.cells.types)
        )

        attributes_child = Attributes(
            target=copy.deepcopy(attributes.target),
            observables=observables_child,
            cells=cells_child,
        )

        config_child = Config(
            data=copy.deepcopy(data),
            experiment=Experiment(
                data=data_type,
                task=Task.table,
                method=copy.deepcopy(child_method),
                data_params=copy.deepcopy(data_params),
            ),
            annotations=copy.deepcopy(annotations),
            attributes=attributes_child,
            is_run=False,
            is_root=False,
            is_load_child=False
        )
        Node(name=str(config_child), config=config_child, parent=root)

    build_tree(root)
    calc_tree(root)


def plot_scatter_comparison(
    data_type,
    data_list,
    annotations_list,
    attributes_list,
    observables_list,
    data_params_list,
    rows_dict,
    cols_dict,
    child_method=Method.linreg,
    method_params=None,
):

    data = copy.deepcopy(data_list[0])
    data.base = 'comparison'
    annotations = annotations_list[0]
    attributes = attributes_list[0]

    items = rows_dict['items']
    data_bases = cols_dict['data_bases']

    task_params = {'type': 'run'}

    method_params['items'] = items
    method_params['data_bases'] = data_bases
    if 'aux' in rows_dict:
        method_params['aux'] = rows_dict['aux']
    method_params['x_ranges'] = []
    for data_base_id, data_base in enumerate(data_bases):
        method_params['x_ranges'].append([cols_dict['begins'][data_base_id], cols_dict['ends'][data_base_id]])

    method_params['y_ranges'] = []
    for item_id in range(0, len(items)):
        method_params['y_ranges'].append([rows_dict['begins'][item_id], rows_dict['ends'][item_id]])

    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            data=data_type,
            task=Task.plot,
            method=Method.scatter_comparison,
            method_params=copy.deepcopy(method_params),
            task_params=task_params
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True,
        is_load_child=False,
        is_init=False,
        is_init_child=False
    )
    root = Node(name=str(config_root), config=config_root)

    for data_base_id, data_base in enumerate(data_bases):
        method_params_lvl_1 = copy.deepcopy(method_params)
        method_params_lvl_1['items'] = items
        method_params_lvl_1['x_ranges'] = [cols_dict['begins'][data_base_id], cols_dict['ends'][data_base_id]]
        method_params_lvl_1['y_ranges'] = []

        for item_id in range(0, len(items)):
            method_params_lvl_1['y_ranges'].append([rows_dict['begins'][item_id], rows_dict['ends'][item_id]])

        task_params_lvl_1 = {'type': 'prepare'}

        config_lvl_1 = Config(
            data=copy.deepcopy(data_list[data_base_id]),
            experiment=Experiment(
                data=data_type,
                task=Task.plot,
                method=Method.scatter,
                data_params=copy.deepcopy(data_params_list[data_base_id]),
                task_params=task_params_lvl_1,
                method_params=method_params_lvl_1
            ),
            annotations=copy.deepcopy(annotations_list[data_base_id]),
            attributes=copy.deepcopy(attributes_list[data_base_id]),
            is_run=True,
            is_root=False,
            is_load_child=False
        )

        node_lvl_1 = Node(name=str(config_lvl_1), config=config_lvl_1, parent=root)

        for d in observables_list[data_base_id]:
            observables_child = Observables(
                name=copy.deepcopy(attributes_list[data_base_id].observables.name),
                types=d
            )

            cells_child = Cells(
                name=copy.deepcopy(attributes_list[data_base_id].cells.name),
                types=copy.deepcopy(attributes_list[data_base_id].cells.types)
            )

            attributes_child = Attributes(
                target=copy.deepcopy(attributes_list[data_base_id].target),
                observables=observables_child,
                cells=cells_child,
            )

            config_child = Config(
                data=copy.deepcopy(data_list[data_base_id]),
                experiment=Experiment(
                    data=data_type,
                    task=Task.table,
                    method=copy.deepcopy(child_method),
                    data_params=copy.deepcopy(data_params_list[data_base_id]),
                ),
                annotations=copy.deepcopy(annotations_list[data_base_id]),
                attributes=attributes_child,
                is_run=False,
                is_root=False,
                is_load_child=False
            )
            Node(name=str(config_child), config=config_child, parent=node_lvl_1)

    build_tree(root)
    calc_tree(root)
