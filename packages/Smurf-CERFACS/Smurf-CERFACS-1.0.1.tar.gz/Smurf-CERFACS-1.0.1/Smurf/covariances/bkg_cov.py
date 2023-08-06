"""
BkgCov
========

Background error covariance matrix B:
"""

import logging
from ..common.matrix import Matrix
from ..common.errors import BError

# ======================================================


class BkgCov(Matrix):

    logger = logging.getLogger('Background Error Covariance')
    logging.Logger.setLevel(logger, logging.INFO)

    # =================================== #
    #               Methods               #
    # =================================== #

    def __init__(self, model, config):
        """Constructor
            - model:    model
            - config:   configuration for defining the matrix
        """
        
        self.model = id(model)                    # Model instance id associated with B
        self.control = model.control              # Dictionary of control variables
        self.first_node = model.first_node        # List of variable indices in xb
        self.conf = config                        # Configuration for B

        if self.conf['type'] is None:
            Matrix.__init__(self, dim=0)
            return
        else:
            Matrix.__init__(self, dim=model.ctl_length)
        
        # Spatial covariances
        for v, var in enumerate(self.control):
            # Indices
            try:
                confvar = self.conf[var]
            except KeyError:
                msg = 'No configuration for control variable {}.'.format(var)
                self.logger.error(msg)
                raise BError(msg)
            ind0 = self.first_node[v]
            ind1 = self.first_node[v+1]
            # Spatial covariances
            self.spatial_covariances(confvar, ind0, ind1)

        # Balance relationships
        for v, var in enumerate(self.control):
            # Indices
            confvar = self.conf[var]
            ind0 = self.first_node[v]
            ind1 = self.first_node[v+1]
            # Balance
            if 'balance' in confvar:
                # Loop on related variables
                for key in confvar['balance']:
                    # Indices
                    try:
                        confbal = confvar['balance'][key]
                    except (KeyError, TypeError):
                        msg = 'No balance for control variable {} and {}.'.format(var, key)
                        self.logger.error(msg)
                        raise BError(msg)
                    vind = self.control.keys().index(key)
                    indb0 = self.first_node[vind]
                    indb1 = self.first_node[vind+1]
                    if indb1 - indb0 != ind1 - ind0:
                        msg = 'Balance relationships must be defined on same length.'
                        self.logger.error(msg)
                        raise BError(msg)
                    # Balance relationshipt 
                    if confbal['type'] == 'constant':
                        # Constant coefficient
                        self.array[ind0:ind1, indb0:indb1] = self.array[indb0:indb1, indb0:indb1]
                        self.array[ind0:ind1, indb0:indb1] *= self.const_vector(confbal, ind1-ind0)

        self.init = True
        
    def update(self):
        """Update the background error covariance matrix"""
        
        try:
            if self.conf['update'] == 'static':
                return
        except (KeyError, TypeError):
            msg = 'No B update available.'
            self.logger.error(msg)
            raise BError(msg)
        else:
            msg = 'No B update available.'
            self.logger.error(msg)
            raise BError(msg)

    def __repr__(self):
        """Information"""

        string = 'Background error covariance matrix \n'
        if self.init:
            string += '   Initialised with dimension {}\n'.format(self.shape)
        else:
            string += '   Not yet initialised\n'
        return string
