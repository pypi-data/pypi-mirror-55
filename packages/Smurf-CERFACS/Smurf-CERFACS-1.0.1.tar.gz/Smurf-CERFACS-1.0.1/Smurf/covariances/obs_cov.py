"""
ObsCov
========

Observation error covariance matrix R:
"""

import logging
from copy import deepcopy
from ..common.matrix import Matrix

# ======================================================


class ObsCov(Matrix):

    logger = logging.getLogger('Observation Error Covariance')
    logging.Logger.setLevel(logger, logging.INFO)

    # =================================== #
    #               Methods               #
    # =================================== #

    def __init__(self, yo, config):
        """Constructor
            - yo:     observation vector
            - config: configuration for defining the matrix
        """
        
        self.yo = yo                                  # Observation vector associated with R
        self.conf = deepcopy(config)                  # Configuration for R
        
        Matrix.__init__(self, dim=self.yo.dim)
        
        # Standard deviation
        if 'sigma' not in self.conf:
            # Define std from obs sigma
            self.conf['sigma'] = {}
            self.conf['sigma']['type'] = 'list'
            self.conf['sigma']['value'] = self.yo.sigma

        # Spatial correlations
        self.spatial_covariances(self.conf, 0, self.yo.dim)
        
        self.init = True

    def __repr__(self):
        """Information"""

        string = 'Observation error covariance matrix \n'
        if self.init:
            string += '   Initialised with dimension {}\n'.format(self.shape)
        else:
            string += '   Not yet initialised\n'
        return string
