"""
Errors
=======

"""


class UserError(Exception):
    """Base class for exception"""

    pass


class AssimError(UserError):
    """Exceptions comming from Assim"""

    def __init__(self, msg):
        print('Assimilation ERROR: {}'.format(msg))
        raise SystemExit


class BarbametreError(UserError):
    """Exceptions comming from Barbametre"""

    def __init__(self, msg):
        print('Barbametre ERROR: {}'.format(msg))
        raise SystemExit


class BarbatrucError(UserError):
    """Exceptions comming from Barbatruc"""

    def __init__(self, msg):
        print('Barbatruc ERROR: {}'.format(msg))
        raise SystemExit


class BError(UserError):
    """Exceptions comming from BkgCov"""

    def __init__(self, msg):
        print('Background Error Covariance ERROR: {}'.format(msg))
        raise SystemExit


class ChronosError(UserError):
    """Exceptions comming from Chronos"""

    def __init__(self, msg):
        print('Chronos ERROR: {}'.format(msg))
        raise SystemExit


class ClickerError(UserError):
    """Exceptions comming from Clicker"""

    def __init__(self, msg):
        print('Clicker ERROR: {}'.format(msg))
        raise SystemExit


class EnKFError(UserError):
    """Exceptions comming from EnKF"""

    def __init__(self, msg):
        print('Ensemble Kalman Filter ERROR: {}'.format(msg))
        raise SystemExit


class ExperimentError(UserError):
    """Exceptions comming from experiment"""

    def __init__(self, msg):
        print('Experiment ERROR: {}'.format(msg))
        raise SystemExit


class GaugeError(UserError):
    """Exceptions comming from Gauge"""

    def __init__(self, msg):
        print('Gauge ERROR: {}'.format(msg))
        raise SystemExit


class InstrError(UserError):
    """Exceptions comming from Instrument"""

    def __init__(self, msg):
        print('Instrument ERROR: {}'.format(msg))
        raise SystemExit


class KFError(UserError):
    """Exceptions comming from KF"""

    def __init__(self, msg):
        print('Kalman Filter ERROR: {}'.format(msg))
        raise SystemExit


class MascaretError(UserError):
    """Exceptions comming from Mascaret"""

    def __init__(self, msg):
        print('Mascaret ERROR: {}'.format(msg))
        raise SystemExit


class MatrixError(UserError):
    """Exceptions comming from Matrix"""

    def __init__(self, msg):
        print('Matrix ERROR: {}'.format(msg))
        Exception.__init__(self)


class ModelError(UserError):
    """Exceptions comming from Model"""

    def __init__(self, msg):
        print('Model ERROR: {}'.format(msg))
        raise SystemExit


class PertError(UserError):
    """Exceptions comming from perturbation"""

    def __init__(self, msg):
        print('Perturbation ERROR: {}'.format(msg))
        raise SystemExit


class PixieError(UserError):
    """Exceptions coming from Pixie model"""

    def __init__(self, msg):
        print('Pixie model ERROR: {}'.format(msg))
        raise SystemExit


class PPError(UserError):
    """Exceptions comming from PostProcessing"""

    def __init__(self, msg):
        print('Post Processing ERROR: {}'.format(msg))
        raise SystemExit


class RError(UserError):
    """Exceptions comming from ObsCov"""

    def __init__(self, msg):
        print('Observation Error Covariance ERROR: {}'.format(msg))
        raise SystemExit


class SwotError(UserError):
    """Exceptions comming from Swot"""

    def __init__(self, msg):
        print('Swot ERROR: {}'.format(msg))
        raise SystemExit


class VectorError(UserError):
    """Exceptions comming from Vector"""

    def __init__(self, msg):
        print('Vector ERROR: {}\n'.format(msg))
        Exception.__init__(self)


class YoError(UserError):
    """Exceptions comming from Vector"""

    def __init__(self, msg):
        print('Vector ERROR: {}'.format(msg))
        raise SystemExit
