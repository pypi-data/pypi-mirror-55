"""
Instanciate model depending on type
"""

import logging
from ..common.errors import ModelError


def instanciate(model_type, config, prm, statdir='.', wdir='Work', archdir='Archive', member=0,
                start=None, start0=None, postproc=False):
    """Create the model instance depending on the type"""
    
    logger = logging.getLogger('Model Instance')
    logging.Logger.setLevel(logger, logging.INFO)

    if model_type == 'Mascaret':
        from .mascaret import Mascaret
        return Mascaret(config, prm, statdir, wdir, archdir, member, start, start0, postproc)

    elif model_type == 'Barbatruc':
        from .barbatruc import Barbatruc
        return Barbatruc(config, prm, statdir, wdir, archdir, member, start, start0, postproc)

    elif model_type == 'Pixie':
        try:
            from .pixie import Pixie
        except ImportError:
            msg = 'Model {} is not available.'.format(model_type)
            logger.error(msg)
            raise ModelError(msg)
        else:
            return Pixie(config, prm, statdir, wdir, archdir, member, start, start0, postproc)
    
    elif model_type == 'Opm':
        try:
            from .opm import Opm
        except ImportError:
            msg = 'Model {} is not available.'.format(model_type)
            logger.error(msg)
            raise ModelError(msg)
        else:
            return Opm(config, prm, statdir, wdir, archdir, member, start, start0, postproc)

    else:
        msg = 'Model {} does not exist.'.format(model_type)
        logger.error(msg)
        raise ModelError(msg)
