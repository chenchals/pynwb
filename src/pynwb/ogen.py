import numpy as np
from collections import Iterable

from form.utils import docval, popargs

from . import register_class, CORE_NAMESPACE
from .base import TimeSeries, _default_resolution, _default_conversion
from .core import NWBContainer

@register_class('OptogeneticStimulusSite', CORE_NAMESPACE)
class OptogeneticStimulusSite(NWBContainer):
    '''
    '''

    __nwbfields__ = ('device',
                     'description',
                     'excitation_lambda',
                     'location')

    @docval({'name': 'device', 'type': str, 'doc': 'Name of device in /general/devices'},
            {'name': 'description', 'type': str, 'doc': 'Description of site.'},
            {'name': 'excitation_lambda', 'type': str, 'doc': 'Excitation wavelength.'},
            {'name': 'location', 'type': str, 'doc': 'Location of stimulation site.'})
    def __init__(self, **kwargs):
        device, description, excitation_lambda, location = popargs('device', 'description', 'excitation_lambda', 'location', kwargs)
        super(OptogeneticStimulusSite, self).__init__(**kwargs)
        self.device = device
        self.description = description
        self.excitation_lambda = excitation_lambda
        self.location = location

@register_class('OptogeneticSeries', CORE_NAMESPACE)
class OptogeneticSeries(TimeSeries):
    '''
    Optogenetic stimulus. The data field is in unit of watts.
    '''

    __nwbfields__ = ('site',)

    _ancestry = "TimeSeries,OptogeneticSeries"
    _help = "Optogenetic stimulus."

    @docval({'name': 'name', 'type': str, 'doc': 'The name of this TimeSeries dataset'},
            {'name': 'source', 'type': str, 'doc': ('Name of TimeSeries or Modules that serve as the source for the data '
                                                   'contained here. It can also be the name of a device, for stimulus or '
                                                   'acquisition data')},
            {'name': 'data', 'type': (list, np.ndarray, TimeSeries), 'doc': 'The data this TimeSeries dataset stores. Can also store binary data e.g. image frames'},
            {'name': 'unit', 'type': str, 'doc': 'Value is the string "Watt".', 'default': 'Watt'},

            {'name': 'site', 'type': OptogeneticStimulusSite, 'doc': 'Name of site description in general/optogentics.'},

            {'name': 'resolution', 'type': float, 'doc': 'The smallest meaningful difference (in specified unit) between values in data', 'default': _default_resolution},
            {'name': 'conversion', 'type': float, 'doc': 'Scalar to multiply each element by to conver to volts', 'default': _default_conversion},

            {'name': 'timestamps', 'type': (list, np.ndarray, TimeSeries), 'doc': 'Timestamps for samples stored in data', 'default': None},
            {'name': 'starting_time', 'type': float, 'doc': 'The timestamp of the first sample', 'default': None},
            {'name': 'rate', 'type': float, 'doc': 'Sampling rate in Hz', 'default': None},

            {'name': 'comments', 'type': str, 'doc': 'Human-readable comments about this TimeSeries dataset', 'default':None},
            {'name': 'description', 'type': str, 'doc': 'Description of this TimeSeries dataset', 'default':None},
            {'name': 'control', 'type': Iterable, 'doc': 'Numerical labels that apply to each element in data', 'default': None},
            {'name': 'control_description', 'type': Iterable, 'doc': 'Description of each control value', 'default': None},
            {'name': 'parent', 'type': 'NWBContainer', 'doc': 'The parent NWBContainer for this NWBContainer', 'default': None})
    def __init__(self, **kwargs):
        name, source, data, unit = popargs('name', 'source', 'data', 'unit', kwargs)
        site = popargs('site', kwargs)
        super(OptogeneticSeries, self).__init__(name, source, data, unit, **kwargs)
        self.site = site
