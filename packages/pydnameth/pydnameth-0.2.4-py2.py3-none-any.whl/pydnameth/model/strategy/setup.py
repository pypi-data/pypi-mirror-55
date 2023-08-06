import abc
from pydnameth.config.experiment.params import get_default_method_params
from pydnameth.config.experiment.metrics import get_method_metrics_keys
import math


class SetupStrategy(metaclass=abc.ABCMeta):

    def __init__(self, get_strategy):
        self.get_strategy = get_strategy

    @abc.abstractmethod
    def setup(self, config, configs_child):
        pass

    def setup_method_params(self, config):
        default_params = get_default_method_params(config)
        if not bool(config.experiment.method_params):
            config.experiment.method_params = default_params
        else:
            for dp in default_params:
                if dp not in config.experiment.method_params:
                    config.experiment.method_params[dp] = default_params[dp]

    def setup_method_metrics(self, config):
        config.metrics = {}
        for key in get_method_metrics_keys(config):
            config.metrics[key] = []


class TableSetUpStrategy(SetupStrategy):

    def setup(self, config, configs_child):
        self.setup_method_params(config)
        self.setup_method_metrics(config)

        metrics_keys = get_method_metrics_keys(config)

        if config.is_load_child:

            for config_child in configs_child:

                for key in config_child.advanced_data:
                    if key not in metrics_keys:
                        suffix = str(config_child.attributes.observables)
                        if suffix != '' and suffix not in key:
                            key += '_' + suffix
                        config.metrics[key] = []
                        metrics_keys.append(key)


class ClockSetUpStrategy(SetupStrategy):

    def setup(self, config, configs_child):
        self.setup_method_params(config)
        self.setup_method_metrics(config)

        max_size = len(config.attributes_dict[config.attributes.target])
        test_size = math.floor(max_size * config.experiment.method_params['part'])
        train_size = max_size - test_size

        # In clock task only first base config matters
        table = configs_child[0].advanced_data
        items = table['item'][0:max_size]
        values = self.get_strategy.get_single_base(config, items)

        config.experiment_data = {
            'items': items,
            'values': values,
            'test_size': test_size,
            'train_size': train_size
        }


class PlotSetUpStrategy(SetupStrategy):

    def setup(self, config, configs_child):
        self.setup_method_params(config)
        self.setup_method_metrics(config)

        config.experiment_data = {
            'item': [],
            'data': [],
            'fig': []
        }


class CreateSetUpStrategy(SetupStrategy):

    def setup(self, config, configs_child):
        pass
