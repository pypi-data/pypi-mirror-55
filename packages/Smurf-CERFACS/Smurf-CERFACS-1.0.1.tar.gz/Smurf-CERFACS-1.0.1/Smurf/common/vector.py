"""
Vector
=============
"""

import numpy as np
import logging
from ..common.errors import VectorError

# ======================================================


class Vector(object):

    """Vector"""

    logger = logging.getLogger('Vector')
    logging.Logger.setLevel(logger, logging.INFO)

    # Dimension of the vector
    @property
    def dim(self):
        return self._dim
    
    @dim.setter
    def dim(self, value):
        if isinstance(value, (int, float)) and value >= 0:
            self._dim = int(value)
        else:
            msg = 'Unknown dimension {}.'.format(value)
            self.logger.exception(msg)
            raise VectorError(msg)

    # =================================== #
    #               Methods               #
    # =================================== #

    def __init__(self, array=None, dim=None):
        """Constructor
            array:     array with dimension >= 1
            dim:        int
        """
    
        try:
            if array is None:
                if dim is None:
                    dim = 0
                self.dim = dim
                self.array = np.zeros(self.dim)
                self.init = False
            else:
                ar = np.array(array, copy=True).ravel()
                self.dim = len(ar)
                self.array = 1. * ar
                self.init = True
        except ValueError as err:
            msg = 'Cannot set the vector:\n{}'.format(err)
            self.logger.error(msg)
            raise VectorError(msg)

    def invert(self):
        """Invert a vector"""
        
        v = np.copy(self.array)
        ind = np.where(v != 0.)
        v[ind] = 1. / v[ind]
        return Vector(v)
    
    def abs(self):
        """Absolute value"""
        
        return Vector(abs(self.array))
    
    def sign(self):
        """Return sign"""
        
        return Vector(np.sign(self.array))
    
    def __getitem__(self, index):
        """Get item of the vector"""
        
        try:
            return Vector(self.array[index])
        except IndexError:
            msg = 'Cannot get the item {}.'.format(index)
            self.logger.error(msg)
            raise VectorError(msg)

    def __setitem__(self, index, value):
        """Get item of the vector"""
        
        try:
            self.array[index] = value
        except ValueError:
            self.array[index] = value.array[:]
        except IndexError:
            msg = 'Cannot set the item {}.'.format(index)
            self.logger.error(msg)
            raise VectorError(msg)

    def __contains__(self, value):
        """Check if value is in vector"""
        
        try:
            if value in self.array:
                return True
            else:
                return False
        except ValueError:
            msg = 'Cannot check the value {}.'.format(value)
            self.logger.error(msg)
            raise VectorError(msg)

    def __add__(self, other):
        """Addition"""
        
        try:
            if isinstance(other, Vector):
                v = self.array + other.array
            else:
                v = self.array + other
        except ValueError as err:
            msg = 'Cannot perform the addition:\n{}'.format(err)
            self.logger.error(msg)
            raise VectorError(msg)
        else:
            return Vector(v)

    def __radd__(self, other):
        """Addition"""
        
        try:
            if isinstance(other, Vector):
                v = self.array + other.array
            else:
                v = self.array + other
        except ValueError as err:
            msg = 'Cannot perform the addition:\n{}'.format(err)
            self.logger.error(msg)
            raise VectorError(msg)
        else:
            return Vector(v)

    def __sub__(self, other):
        """Subtraction"""
        
        try:
            if isinstance(other, Vector):
                v = self.array - other.array
            else:
                v = self.array - other
        except ValueError as err:
            msg = 'Cannot perform the subtraction:\n{}'.format(err)
            self.logger.error(msg)
            raise VectorError(msg)
        else:
            return Vector(v)

    def __rsub__(self, other):
        """Subtraction"""
        
        try:
            if isinstance(other, Vector):
                v = other.array - self.array
            else:
                v = other - self.array
        except ValueError as err:
            msg = 'Cannot perform the subtraction:\n{}'.format(err)
            self.logger.error(msg)
            raise VectorError(msg)
        else:
            return Vector(v)

    def __mul__(self, other):
        """Product"""
        
        try:
            if isinstance(other, Vector):
                v = self.array * other.array
            else:
                v = self.array * other
        except ValueError as err:
            msg = 'Cannot perform the multiplication:\n{}'.format(err)
            self.logger.error(msg)
            raise VectorError(msg)
        else:
            return Vector(v)

    def __rmul__(self, other):
        """Product"""
        
        try:
            if isinstance(other, Vector):
                v = self.array * other.array
            else:
                v = self.array * other
        except ValueError as err:
            msg = 'Cannot perform the multiplication:\n{}'.format(err)
            self.logger.error(msg)
            raise VectorError(msg)
        else:
            return Vector(v)

    def __pow__(self, value):
        """Power"""
        try:
            v = self.array ** value
        except ValueError as err:
            msg = 'Cannot set to the power:\n{}'.format(err)
            self.logger.error(msg)
            raise VectorError(msg)
        else:
            return Vector(v)

    def __div__(self, other):
        """Division"""
        
        try:
            if isinstance(other, Vector):
                v = self.array / other.array
            else:
                v = self.array / other
        except ZeroDivisionError:
            msg = 'Division by 0.'
            self.logger.error(msg)
            raise VectorError(msg)
        except ValueError as err:
            msg = 'Cannot perform the division:\n{}'.format(err)
            self.logger.error(msg)
            raise VectorError(msg)
        else:
            return Vector(v)

    def __rdiv__(self, other):
        """Division"""
        
        try:
            if isinstance(other, Vector):
                v = other.array / self.array
            else:
                v = other / self.array
        except ZeroDivisionError:
            msg = 'Division by 0.'
            self.logger.error(msg)
            raise VectorError(msg)
        except ValueError as err:
            msg = 'Cannot perform the division:\n{}'.format(err)
            self.logger.error(msg)
            raise VectorError(msg)
        else:
            return Vector(v)

    def __eq__(self, other):
        """Comparison =="""
        
        if isinstance(other, Vector):
            res = self.array == other.array
        else:
            res = self.array == other
        return res

    def __ne__(self, other):
        """Comparison !="""
        
        if isinstance(other, Vector):
            res = self.array != other.array
        else:
            res = self.array != other
        return res

    def __ge__(self, other):
        """Comparison >="""
        
        if isinstance(other, Vector):
            res = self.array >= other.array
        else:
            res = self.array >= other
        return res

    def __le__(self, other):
        """Comparison <="""
        
        if isinstance(other, Vector):
            res = self.array <= other.array
        else:
            res = self.array <= other
        return res

    def __gt__(self, other):
        """Comparison >"""
        
        if isinstance(other, Vector):
            res = self.array > other.array
        else:
            res = self.array > other
        return res

    def __lt__(self, other):
        """Comparison <"""
        
        if isinstance(other, Vector):
            res = self.array < other.array
        else:
            res = self.array < other
        return res

    def __repr__(self):
        """Information"""
        
        string = 'Vector with dimension {}\n'.format(self.dim)
        if self.init:
            string += '   Initialised\n'
        else:
            string += '   Not yet initialised\n'
        return string
