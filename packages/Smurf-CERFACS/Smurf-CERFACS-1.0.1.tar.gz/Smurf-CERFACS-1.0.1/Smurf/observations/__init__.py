"""
observations module
*******************
"""

from .obs_vector import ObsVector
from .instrument import Instrument
from .gauge import Gauge
from .barbametre import Barbametre


__all__ = ['ObsVector', 'Instrument', 'Barbametre', 'Gauge'] 

try:
    from .swot import Swot
    from .swot_pixel_cloud import SwotPixelCloud
    from .swot_river_node import SwotRiverNode
    from .swot_river_reach import SwotRiverReach
    __all__.extend(['Swot', 'SwotPixelCloud', 'SwotRiverNode'])
except ImportError:
    pass

try:
    from .chronos import Chronos
    from .Clicker import Clicker
    __all__.extend(['Chonos', 'Clicker'])
except ImportError:
    pass

try:
    from .well_instrument import WellInstrument
    __all__.append('WellInstrument')
except ImportError:
    pass

