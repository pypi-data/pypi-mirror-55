"""
Instanciate observation depending on instrument
"""

import logging
from ..common.errors import InstrError


def instanciate(instrument, config, prm, dateref=None, size=1):
    """Create the observation instance depending on the instrument"""

    logger = logging.getLogger('Instrument Instance')
    logging.Logger.setLevel(logger, logging.INFO)

    if instrument == 'Gauge':
        from .gauge import Gauge
        return Gauge(config, prm, dateref, size)

    elif instrument == 'Barbametre':
        from .barbametre import Barbametre
        return Barbametre(config, prm, dateref, size)

    elif instrument == 'Swot':
        try:
            if config['product'] == 'pixel cloud':
                from .swot_pixel_cloud import SwotPixelCloud
            elif config['product'] == 'river node':
                from .swot_river_node import SwotRiverNode
            elif config['product'] == 'river reach':
                from .swot_river_reach import SwotRiverReach
        except(ValueError, TypeError):
            return SwotRiverReach(config, dateref, size)
        else:
            if config['product'] == 'pixel cloud':
                return SwotPixelCloud(config, prm, dateref, size)
            elif config['product'] == 'river node':
                return SwotRiverNode(config, prm, dateref, size)
            elif config['product'] == 'river reach':
                return SwotRiverReach(config, prm, dateref, size)

    elif instrument == 'Chronos':
        try:
            from .chronos import Chronos
        except ImportError:
            msg = 'Instrument {} is not available.'.format(instrument)
            logger.error(msg)
            raise InstrError(msg)
        else:
            return Chronos(config, prm, dateref, size)

    elif instrument == 'Clicker':
        try:
            from .clicker import Clicker
        except ImportError:
            msg = 'Instrument {} is not available.'.format(instrument)
            logger.error(msg)
            raise InstrError(msg)
        else:
            return Clicker(config, prm, dateref, size)

    elif instrument == 'WellInstrument':
        try:
            from .well_instrument import WellInstrument
        except ImportError:
            msg = 'Instrument {} is not available.'.format(instrument)
            logger.error(msg)
            raise InstrError(msg)
        else:
            return WellInstrument(config, prm, dateref, size)

    else:
        msg = 'Instrument {} does not exist.'.format(instrument)
        logger.error(msg)
        raise InstrError(msg)
