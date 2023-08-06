from pydnameth.config.common import CommonTypes
import numpy as np
from pydnameth.routines.common import is_float


def pass_indexes(config, target, variable, any):
    passed_indexes = []
    attributes = config.attributes_dict[target]
    if variable == any:
        passed_indexes = list(range(0, len(attributes)))
    else:

        if variable not in attributes:
            raise ValueError(f'No {str(variable)} in {target} column.')

        for index in range(0, len(attributes)):
            if variable == attributes[index]:
                passed_indexes.append(index)
    return passed_indexes


def pass_indexes_interval(config, target, left, right):
    passed_indexes = []
    attributes = config.attributes_dict[target]
    for index in range(0, len(attributes)):
        if left <= attributes[index] < right:
            passed_indexes.append(index)
    return passed_indexes


def get_indexes(config):
    indexes = list(range(0, len(list(config.attributes_dict.values())[0])))

    for obs, value in config.attributes.observables.types.items():
        any = CommonTypes.any.value
        if obs in config.attributes_dict:

            if obs == 'age':

                if len(value) == 2:
                    left = float(value[0])
                    right = float(value[1])
                    passed_indexes = pass_indexes_interval(config, obs, left, right)
                else:
                    raise ValueError('Wrong attributes_dict key for age. It should be (left, right).')

            else:

                if isinstance(value, list):
                    passed_indexes = []
                    for v in value:
                        if is_float(v):
                            v = float(v)
                            if v.is_integer():
                                v = int(v)
                        passed_indexes += pass_indexes(config, obs, v, any)
                else:
                    if is_float(value):
                        value = float(value)
                        if value.is_integer():
                            value = int(value)
                    passed_indexes = pass_indexes(config, obs, value, any)

            indexes = list(set(indexes).intersection(passed_indexes))
        else:
            raise ValueError('Wrong observables.types key.')

    indexes.sort()

    print(f'number of indexes: {len(indexes)}')

    return indexes


def subset_attributes(config):
    for key in config.attributes_dict:
        values = config.attributes_dict[key]
        passed_values = []
        for index in config.attributes_indexes:
            passed_values.append(values[index])
        config.attributes_dict[key] = passed_values


def subset_cells(config):

    if config.cells_dict is not None:

        if config.attributes.cells.types != CommonTypes.any:
            if isinstance(config.attributes.cells.types, list):
                all_cells_types = list(config.cells_dict.keys())
                for key in all_cells_types:
                    if key not in config.attributes.cells.types:
                        config.cells_dict.pop(key)

        for key in config.cells_dict:
            values = config.cells_dict[key]
            values = list(np.array(values)[config.attributes_indexes])
            config.cells_dict[key] = values
