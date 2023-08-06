"""
Matrix
=============

    Matrix of dimension dim x dim
"""

import numpy as np
import logging
from .vector import Vector
from ..common.errors import MatrixError

# ======================================================


class Matrix(object):

    """Matrix"""

    logger = logging.getLogger('Matrix')
    logging.Logger.setLevel(logger, logging.INFO)

    # Dimension of the matrix
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
            raise MatrixError(msg)
     
    # Transpose
    @property
    def T(self):
        return Matrix(self.array.T)

    # =================================== #
    #               Methods               #
    # =================================== #

    def __init__(self, array=None, dim=None, cst=1):
        """Constructor
            array:     array with dimension >= 1
            dim:        int for square matrix, list of dimension otherwise
            cst:        constant to initialise eye matrix
        """
    
        try:
            if array is None:
                if dim is None:
                    dim = 0
                if isinstance(dim, (int, float)):
                    # Square matrix          
                    self.dim = 2
                    self.shape = (int(dim), int(dim))
                    if dim == 0:
                        self.array = np.array((np.zeros(dim), np.zeros(dim)))
                        self.init = False
                    else:
                        self.array = cst * np.eye(dim)
                        self.init = True
                else:
                    # Other matrix
                    self.dim = len(dim)
                    self.shape = tuple(dim)
                    self.array = np.zeros(self.shape)
                    self.init = False
            else:
                if isinstance(array, (list, tuple, np.ndarray)):
                    ar = 1. * np.array(array, copy=True)
                    if ar.ndim == 1:
                        self.array = np.diag(ar)
                    else:
                        self.array = ar
                self.dim = np.ndim(self.array)
                self.shape = np.shape(self.array)
                self.init = True
        except ValueError as err:
            msg = 'Cannot set the matrix:\n{}'.format(err)
            self.logger.error(msg)
            raise MatrixError(msg)

    def spatial_covariances(self, dico, ind0, ind1):
        """Define spatial covariances
            - dico:   configuration dictionary
            - ind0:   starting index for the block diagonal matrix
            - ind1:   ending index for the block diagonal matrix
        """
    
        # Correlations
        if dico['type'] == 'diagonal':
            # Diagonal matrix
            self.array[ind0:ind1, ind0:ind1] = np.eye(ind1-ind0)
        elif dico['type'] == 'gauss':
            # Gaussian covariances
            self.array[ind0:ind1, ind0:ind1] = self.gaussian(dico['length_scale'], ind1-ind0)
        else:
            msg = 'Cannot understand correlation type {}.'.format(dico['type'])
            self.logger.error(msg)
            raise MatrixError(msg)
        
        # Variances
        if 'sigma' in dico:
            self.array[ind0:ind1, ind0:ind1] *= self.const_vector(dico['sigma'], ind1-ind0, square=True)
    
    def gaussian(self, dico, dim):
        """Construct a correlation matrix with a gaussian function kernel
            - dico:    dictionary of configuration
            - dim:     dimension of the matrix
        """
        
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #  The length scales are defined as ratio
        # It is assumed that the grid is continuous
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        m = np.zeros((dim, dim))
        if dico['type'] == 'constant':
            for i in range(dim):
                m[i, :i] = np.exp(-(np.arange(i, 0, -1))**2 / (2.*dico["L_down"]**2))
                m[i, i:] = np.exp(-(i-np.arange(i, dim))**2 / (2.*dico["L_up"]**2))
        else:
            msg = 'Incorrect configuration {}.'.format(dico['type'])
            self.logger.exception(msg)
            raise MatrixError(msg)
        
        return m        

    def const_vector(self, dico, dim, square=False):
        """Construct a vector
            - dico:    dictionary of configuration
            - dim:     dimension of the vector
            - square:  square the value
        """
                    
        if dico['type'] == 'constant':
            # Constant variance
            vec = np.ones((dim, 1)) * dico['value']
        elif dico['type'] == 'list':
            vec = np.array(dico['value']).reshape((dim, 1))
        else:
            msg = 'Incorrect configuration {}.'.format(dico['type'])
            self.logger.exception(msg)
            raise MatrixError(msg)
        
        if square:
            return vec**2
        else:
            return vec

    def transpose(self):
        """Transpose of the matrix"""
        
        return Matrix(self.array.T)
    
    def diag(self):
        """Diagonal of the matrix"""
        
        return Vector(np.diag(self.array))
    
    def invert(self, method='linalg'):
        """Invert the matrix"""
        
        try:
            if method == 'linalg':
                return Matrix(np.linalg.inv(self.array))
            else:
                msg = 'Unknown method {}.'.format(method)
                self.logger.error(msg)
                raise AttributeError(msg)
        except np.linalg.linalg.LinAlgError as err:
            msg = 'Cannot invert the matrix:\n{}'.format(err)
            self.logger.error(msg)
            raise MatrixError(msg)

    def norm(self):
        """Get the Frobenius norm of the matrix"""
        
        return np.linalg.norm(self.array)

    def mean(self, axis=None):
        """Get the mean
            - axis:  axis for which the mean is calculated
        """
        
        try:
            m = np.mean(self.array, axis=axis)
        except IndexError:
            msg = 'Cannot calculate the mean: no axis {}.'.format(axis)
            self.logger.error(msg)
            raise MatrixError(msg)
        except ArithmeticError as err:
            msg = 'Cannot calculate the mean:\n{}'.format(err)
            self.logger.error(msg)
            raise MatrixError(err)
        else:
            if axis is None:
                return m
            elif m.ndim == 1:
                return Vector(m)
            else:
                return Matrix(m)

    def std(self, axis=None):
        """Get the standard deviation
            - axis:  axis for which the std is calculated
        """
        
        try:
            m = np.std(self.array, axis=axis)
        except IndexError:
            msg = 'Cannot calculate the std: no axis {}.'.format(axis)
            self.logger.error(msg)
            raise MatrixError(msg)
        except ArithmeticError as err:
            msg = 'Cannot calculate the std:\n{}'.format(err)
            self.logger.error(msg)
            raise MatrixError(err)
        else:
            if axis is None:
                return m
            elif m.ndim == 1:
                return Vector(m)
            else:
                return Matrix(m)

    def sort(self, axis=None):
        """Sort the matrix"""
        
        return Matrix(self.array.sort(axis=axis))
    
    def covariance(self, other=None):
        """Get the covariance matrix associated to a matrix of anomalies
            It is assumed that the first dimension is the ensemble dimension
            - other:    matrix to calculate covariance between self and other"""
        
        try:
            dim = self.shape[1]
            if other is None:
                cov = np.zeros((dim, dim))
                for m in range(self.shape[0]):
                    cov += self.array[m, :].reshape((dim, 1)).dot(self.array[m, :].reshape((1, dim)))
            else:
                dimo = other.shape[1]
                cov = np.zeros((dim, dimo))
                for m in range(self.shape[0]):
                    cov += self.array[m, :].reshape((dim, 1)).dot(other.array[m, :].reshape((1, dimo)))
            cov /= self.shape[0] - 1.
        except ArithmeticError as err:
            msg = 'Cannot calculate the covariance:\n{}'.format(err)
            self.logger.error(msg)
            raise MatrixError(msg)
        else:
            return Matrix(cov)

    def copy(self):
        """Copy a matrix"""
        
        return Matrix(self.array)
    
    def __getitem__(self, index):
        """Get item of the matrix"""
        
        try:
            m = self.array[index]
        except IndexError:
            msg = 'Cannot get the item {}.'.format(index)
            self.logger.error(msg)
            raise MatrixError(msg)
        else:
            if m.ndim == 1:
                return Vector(m)
            else:
                return Matrix(m)

    def __setitem__(self, index, value):
        """Set item of the matrix"""
        
        try:
            if isinstance(value, Vector):
                self.array[index] = value.array
            elif isinstance(value, Matrix):
                self.array[index] = value.array
            else:
                self.array[index] = value
        except IndexError:
            msg = 'Cannot set the item {}.'.format(index)
            self.logger.error(msg)
            raise MatrixError(msg)

    def __contains__(self, value):
        """Check if value is in matrix"""
        
        try:
            if value in self.array:
                return True
            else:
                return False
        except ValueError:
            msg = 'Cannot check the value {}.'.format(value)
            self.logger.error(msg)
            raise MatrixError(msg)

    def __add__(self, other):
        """Addition"""
        
        try:
            if isinstance(other, (Vector, Matrix)):
                v = self.array + other.array
            else:
                v = self.array + other
        except ValueError as err:
            msg = 'Cannot perform the addition:\n{}'.format(err)
            self.logger.error(msg)
            raise MatrixError(msg)
        else:
            return Matrix(v)

    def __radd__(self, other):
        """Addition"""
        
        try:
            if isinstance(other, (Vector, Matrix)):
                v = self.array + other.array
            else:
                v = self.array + other
        except ValueError as err:
            msg = 'Cannot perform the addition:\n{}'.format(err)
            self.logger.error(msg)
            raise MatrixError(msg)
        else:
            return Matrix(v)

    def __sub__(self, other):
        """Subtraction"""
        
        try:
            if isinstance(other, (Vector, Matrix)):
                v = self.array - other.array
            else:
                v = self.array - other
        except ValueError as err:
            msg = 'Cannot perform the subtraction:\n{}'.format(err)
            self.logger.error(msg)
            raise MatrixError(msg)
        else:
            return Matrix(v)

    def __rsub__(self, other):
        """Subtraction"""
        
        try:
            if isinstance(other, (Vector, Matrix)):
                v = other.array - self.array
            else:
                v = other - self.array
        except ValueError as err:
            msg = 'Cannot perform the subtraction:\n{}'.format(err)
            self.logger.error(msg)
            raise MatrixError(msg)
        else:
            return Matrix(v)

    def __mul__(self, other):
        """Product"""
        
        try:
            
            if isinstance(other, (Vector, Matrix)):
                v = self.array * other.array
            else:
                v = self.array * other
        except ValueError as err:
            msg = 'Cannot perform the multiplication:\n{}'.format(err)
            self.logger.error(msg)
            raise MatrixError(msg)
        else:
            return Matrix(v)

    def __rmul__(self, other):
        """Product"""
        
        try:
            if isinstance(other, (Vector, Matrix)):
                v = self.array * other.array
            else:
                v = self.array * other
        except ValueError as err:
            msg = 'Cannot perform the multiplication:\n{}'.format(err)
            self.logger.error(msg)
            raise MatrixError(msg)
        else:
            return Matrix(v)

    def __pow__(self, value):
        """Power"""
        try:
            v = self.array ** value
        except ValueError as err:
            msg = 'Cannot set to the power:\n{}'.format(err)
            self.logger.error(msg)
            raise MatrixError(msg)
        else:
            return Matrix(v)

    def __div__(self, other):
        """Division"""
        
        try:
            if isinstance(other, (Vector, Matrix)):
                v = self.array / other.array
            else:
                v = self.array / other
        except ZeroDivisionError:
            msg = 'Division by 0.'
            self.logger.error(msg)
            raise MatrixError(msg)
        except ValueError as err:
            msg = 'Cannot perform the division:\n{}'.format(err)
            self.logger.error(msg)
            raise MatrixError(msg)
        else:
            return Matrix(v)

    def __rdiv__(self, other):
        """Division"""
        
        try:
            if isinstance(other, (Vector, Matrix)):
                v = other.array / self.array
            else:
                v = other / self.array
        except ZeroDivisionError:
            msg = 'Division by 0.'
            self.logger.error(msg)
            raise MatrixError(msg)
        except ValueError as err:
            msg = 'Cannot perform the division:\n{}'.format(err)
            self.logger.error(msg)
            raise MatrixError(msg)
        else:
            return Matrix(v)

    def dot(self, other):
        """Dot product"""
        
        try:
            if isinstance(other, (Vector, Matrix)):
                v = np.dot(self.array, other.array)
            else:
                v = np.dot(self.array, other)
        except ValueError as err:
            msg = 'Cannot perform the dot product:\n{}'.format(err)
            self.logger.error(msg)
            raise MatrixError(msg)
        else:
            if v.ndim == 1:
                return Vector(v)
            else:
                return Matrix(v)

    def __eq__(self, other):
        """Comparison =="""

        if isinstance(other, Matrix):
            res = self.array == other.array
        else:
            res = self.array == other
        return res

    def __ne__(self, other):
        """Comparison !="""
        
        if isinstance(other, Matrix):
            res = self.array != other.array
        else:
            res = self.array != other
        return res

    def __ge__(self, other):
        """Comparison >="""
        
        if isinstance(other, Matrix):
            res = self.array >= other.array
        else:
            res = self.array >= other
        return res

    def __le__(self, other):
        """Comparison <="""
        
        if isinstance(other, Matrix):
            res = self.array <= other.array
        else:
            res = self.array <= other
        return res

    def __gt__(self, other):
        """Comparison >"""
        
        if isinstance(other, Matrix):
            res = self.array > other.array
        else:
            res = self.array > other
        return res

    def __lt__(self, other):
        """Comparison <"""
        
        if isinstance(other, Matrix):
            res = self.array < other.array
        else:
            res = self.array < other
        return res

    def __repr__(self):
        """Information"""
        
        string = 'Matrix {}-dimensional {}\n'.format(self.dim, self.shape)
        if self.init:
            string += '   Initialised\n'
        else:
            string += '   Not yet initialised\n'
        return string
