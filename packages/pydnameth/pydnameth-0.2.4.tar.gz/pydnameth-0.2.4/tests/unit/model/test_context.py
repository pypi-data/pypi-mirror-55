import unittest
from tests.definitions import ROOT_DIR
from pydnameth import Data
from pydnameth import Experiment
from pydnameth import Annotations
from pydnameth import Observables
from pydnameth import Cells
from pydnameth import Attributes
from pydnameth import Config
from pydnameth.model.context import Context
from pydnameth.model.strategy.load import BetasLoadStrategy
from pydnameth.model.strategy.load import ObservablesLoadStrategy
from pydnameth.model.strategy.get import BetasGetStrategy
from pydnameth.model.strategy.get import ObservablesGetStrategy
from pydnameth.model.strategy.setup import TableSetUpStrategy
from pydnameth.model.strategy.setup import ClockSetUpStrategy
from pydnameth.model.strategy.setup import PlotSetUpStrategy
from pydnameth.model.strategy.run import TableRunStrategy
from pydnameth.model.strategy.run import ClockRunStrategy
from pydnameth.model.strategy.run import PlotRunStrategy
from pydnameth.model.strategy.release import TableReleaseStrategy
from pydnameth.model.strategy.release import ClockReleaseStrategy
from pydnameth.model.strategy.release import PlotReleaseStrategy
from pydnameth.model.strategy.save import TableSaveStrategy
from pydnameth.model.strategy.save import ClockSaveStrategy
from pydnameth.model.strategy.save import PlotSaveStrategy
from pydnameth.config.experiment.types import Task
from pydnameth.config.experiment.types import DataType
from tests.tear_down import clear_cache


class TestContext(unittest.TestCase):
    def setUp(self):
        data = Data(
            path=ROOT_DIR,
            base='fixtures'
        )

        annotations = Annotations(
            name='annotations',
            type='450k',
            exclude='excluded',
            select_dict={
                'CROSS_R': ['0'],
                'Probe_SNPs': ['empty'],
                'Probe_SNPs_10': ['empty'],
                'CHR': ['-X', '-Y'],
                'UCSC_REFGENE_NAME': ['non-empty'],
                'Class': ['ClassA', 'ClassB']
            }
        )

        observables = Observables(
            name='observables',
            types={}
        )

        cells = Cells(
            name='cells',
            types='any'
        )

        attributes = Attributes(
            target='age',
            observables=observables,
            cells=cells
        )

        self.config = Config(
            data=data,
            experiment=None,
            annotations=annotations,
            attributes=attributes,
            is_run=True,
            is_root=True
        )
        self.config.initialize()

    def tearDown(self):
        clear_cache(self.config)

    def check_strategy(self, data_type, task, needed_list):
        experiment = Experiment(
            data=data_type,
            task=task,
            method=None,
        )
        self.config.experiment = experiment
        context = Context(self.config)
        condition = True

        real_list = ['load_strategy', 'get_strategy', 'setup_strategy',
                     'run_strategy', 'release_strategy', 'save_strategy']
        real_list = [getattr(context, x) for x in real_list]
        for real, needed in zip(real_list, needed_list):
            if type(real) != needed:
                condition = False
                break

        return condition

    def test_strategy_creation_cpg_table(self):
        condition = self.check_strategy(DataType.betas, Task.table,
                                        [BetasLoadStrategy, BetasGetStrategy, TableSetUpStrategy,
                                         TableRunStrategy, TableReleaseStrategy, TableSaveStrategy])
        self.assertEqual(condition, True)

    def test_strategy_creation_cpg_clock(self):
        condition = self.check_strategy(DataType.betas, Task.clock,
                                        [BetasLoadStrategy, BetasGetStrategy, ClockSetUpStrategy,
                                         ClockRunStrategy, ClockReleaseStrategy, ClockSaveStrategy])
        self.assertEqual(condition, True)

    def test_strategy_creation_plot(self):
        condition = self.check_strategy(DataType.observables, Task.plot,
                                        [ObservablesLoadStrategy, ObservablesGetStrategy, PlotSetUpStrategy,
                                         PlotRunStrategy, PlotReleaseStrategy, PlotSaveStrategy])
        self.assertEqual(condition, True)
