import unittest
import numpy as np
import json
from datetime import datetime
import os

from form.build import GroupBuilder, DatasetBuilder

from pynwb import TimeSeries

from . import base

class TestTimeSeriesIO(base.TestNWBContainerIO):

    def setUpContainer(self):
        self.container = TimeSeries('test_timeseries', 'example_source', list(range(100,200,10)), 'SIunit', timestamps=list(range(10)), resolution=0.1)

    def setUpBuilder(self):
        self.builder = GroupBuilder('test_timeseries',
                                attributes={'ancestry': 'TimeSeries',
                                            'source': 'example_source',
                                            'namespace': base.CORE_NAMESPACE,
                                            'neurodata_type': 'TimeSeries',
                                            'data_link': list(),
                                            'timestamp_link': list(),
                                            'help': 'General time series object'},
                                datasets={'data': DatasetBuilder('data', list(range(100,200,10)),
                                                                 attributes={'unit': 'SIunit',
                                                                             'conversion': 1.0,
                                                                             'resolution': 0.1}),
                                          'num_samples': DatasetBuilder('num_samples', 10),
                                          'timestamps': DatasetBuilder('timestamps', list(range(10)),
                                                                 attributes={'unit': 'Seconds', 'interval': 1})})

