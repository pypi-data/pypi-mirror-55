"""
Instanciate assimilation depending on scheme
"""

import logging
from ..common.errors import AssimError
from .ens_kalman_filter import EnsKalmanFilter as EnKF


def instanciate(assim_type, config, model, window, overlap, wdir='Work', archdir='Archive',
                step=1, nbstep=1, parallel=False, nbproc=0, postproc=False):
    """Create the assimilation instance depending on the type"""

    logger = logging.getLogger('Assimilation Instance')
    logging.Logger.setLevel(logger, logging.INFO)

    if assim_type == 'EnKF':
        return EnKF(config, model, window, overlap, wdir, archdir, step, nbstep, parallel, nbproc, postproc)

    else:
        msg = 'Assimilation scheme {} is not available.'.format(assim_type)
        logger.error(msg)
        raise AssimError(msg)
