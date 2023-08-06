"""
Instrument
=============

Mother class instrument

"""

import logging
import os
import numpy as np
from datetime import timedelta
from .events import events
from ..common.functions import format2sec, sec2unit
from ..common.errors import InstrError


instrument_id = {'Gauge':                1,
                 'Swot': {'river reach': 2,
                          'river node':  3,
                          'pixel cloud': 4},
                 'Chronos':              20,
                 'Clicker':              21,
                 'Barbametre':           30,
                 'WellInstrument':       40}


def get_instrument_name(instr_id):
    """Define the name of the instrument
        instr_id:   id of the instrument
    """

    instr_name = None
    for d in instrument_id.items():
        instr_name = d[0]
        if isinstance(d[1], int):
            if '{}'.format(d[1]) == instr_id:
                break
        else:
            flag = False
            for p in d[1]:
                if '{}'.format(instrument_id[d[0]][p]) == instr_id:
                    instr_name += ' {}'.format(p)
                    flag = True
                    break
            if flag:
                break
    return instr_name


def rejevent_id(event):
    """Return id of a rejection event"""

    return list(filter(lambda d: (d[1] == event), events.items()))[0][0]

# ======================================================


class Instrument(object):

    logger = logging.getLogger('Instrument')
    logging.Logger.setLevel(logger, logging.INFO)

    # =================================== #
    #               Methods               #
    # =================================== #

    def __init__(self, config, prm, dateref=None, size=1):
        """Constructor
            - config:     dictionary of configuration
            - prm:        model parameters
            - dateref:    datetime of the cycle
            - size:       size of the ensemble for omb
        """

        # Instrument Id
        self.id = instrument_id[self.name]
        if isinstance(self.id, dict):
            self.product = config['product']
            self.id = instrument_id[self.name][self.product]
        else:
            self.product = None

        # For postprocessing purpose
        if config == {}:
            return

        # General attributes
        self.conf = config                                 # Dictionary of configuration
        self.parameter = prm                               # Model parameters
        self.dateref = dateref                             # Datetime of the cycle
        self.size = size                                   # Size of the ensemble for omb
        self.name = self.conf['instrument']                # Name of observation instrument
        self.keep = self.conf['keep']                      # Keep the observations for the whole experiment
        try:
            self.no_value = self.conf['no_value']          # Value when observation is not valid (no measurement)
        except(KeyError, TypeError):
            self.no_value = -9999.9
        self.nobs = 0                                      # Number of observations
        self.nvalobs = 0                                   # Number of valid observations

        # Observation types
        try:
            self.obs_type = self.conf['obs_type']          # observation types
        except (KeyError, TypeError):
            self.obs_type = None
        else:
            self.obs_type = self.check_obs_type(self.obs_type)
        self.index_obs_type = {}                           # Indices of observations related to an obs_type

        # Coordinates
        self.spatial_coord = None                          # Coordinate type. Must be a tuple e.g. ('s',)
        self.spatial_dim = 0                               # Dimension of coordinates e.g. 1
        self.tcoord = np.empty(0, dtype=np.float32)        # Time coordinates array in datetime

        # Observation files
        self.path = config['path']                         # Path to the directory
        subname = ''
        if not self.keep:
            try:
                subdir = self.dateref.strftime(self.conf['subdir_format'])
                self.path = '{}/{}'.format(self.path, subdir)
            except (KeyError, TypeError):
                pass
            try:
                subname = self.dateref.strftime(self.conf['subname_format']) + '_'
            except (KeyError, TypeError):
                subname = ''
        if not os.path.exists(self.path):
            msg = 'The path {} does not exist'.format(self.path)
            self.logger.error(msg)
            raise InstrError(msg)
        listdir = list(filter(lambda f: (os.path.isfile(os.path.join(self.path, f))), os.listdir(self.path)))
        try:                                      # These files only in the path
            tmp = ['{}{}'.format(subname, f) for f in self.conf['files']]
            self.files = [f for f in tmp if f in listdir]
        except (KeyError, TypeError):             # All files in the path
            self.files = [f for f in listdir if f[:len(subname)] == subname]
        else:
            if self.files is None:
                self.files = [f for f in listdir if f[:len(subname)] == subname]

        # Selection of observations
        try:
            self.frequency = format2sec(self.conf['selection']['frequency'])  # Frequency of observations to keep
        except (KeyError, TypeError):
            self.frequency = 0
        try:
            self.shift = format2sec(self.conf['selection']['shift'])          # Frequency of observations to keep
        except (KeyError, TypeError):
            self.shift = 0

        # Rejection event
        self.rejevent = np.empty(0, dtype=np.int8)           # Rejection event array
        try:
            self.quality_min = self.conf['quality_min']      # Minimum quality of observations
        except (KeyError, TypeError):
            self.quality_min = None
        self.quality = np.empty(0, dtype=np.int8)            # Quality of the observations

        # Values
        self.measure = np.ma.empty(0, dtype=np.float32)      # Observation array
        self.omb = np.ma.empty(0, dtype=np.float32)          # Observation minus Background array
        self.sigma = np.ma.empty(0, dtype=np.float32)       # Error standard deviation

    def read_observation_files(self):
        """Read the observation files"""

        msg = 'The Instrument method read_observation_files is not implemented'
        raise NotImplementedError(msg)

    def get_spatial_coord(self):
        """Return a list of spatial coordinates for not rejected observations"""

        return [0]

    def get_time_coord(self):
        """Return a list of time coordinates for not rejected observations"""

        return list(self.tcoord[np.where(self.rejevent == 0)])

    def get_observations(self, otype, listtime):
        """Return observations of type otype at time t
            - otype:       type of observation
            - listtime:    list of datetime
        """

        msg = 'The Instrument method get_observations is not implemented'
        raise NotImplementedError(msg)

    def set_omb(self, d, ind):
        """Set obs minus bkg values
            - d:    innovation vector, possibly an ensemble vector
            - ind:  indices of observations
        """

        for i, ii in enumerate(ind):
            self.omb[:, ii] = d[:, i].array

    def check_obs_type(self, obs_type):
        """Check if the observation type is valid
            - obs_type:    list of observation types
        """

        if obs_type is not None:
            obs_var = list(self.parameter['variables'].keys())
            obs_var_low = [s.lower() for s in obs_var]
            for i, ot in enumerate(obs_type):
                if ot.lower() in obs_var_low:
                    obs_type[i] = obs_var[obs_var_low.index(ot.lower())]
                elif ot not in obs_var:
                    msg = 'Observation type {} not understood'.format(ot)
                    self.logger.error(msg)
                    raise InstrError(msg)
        return obs_type

    def reject(self, ind, event):
        """Reject observations
            - ind:     indices of observations to reject
            - event:   rejection event
        """

        self.measure.mask[ind] = True
        self.omb.mask[:, ind] = True
        self.rejevent[ind] = rejevent_id(event)
        self.nvalobs = np.ma.count(self.measure)

    def reset(self, ind):
        """Reset observation rejection
            - ind:     indices of observations to reject
        """

        self.measure.mask[ind] = False
        self.omb.mask[:, ind] = False
        self.rejevent[ind] = 0
        self.nvalobs = np.ma.count(self.measure)

    def reject_no_value(self):
        """Reject observations with no valid measurement"""

        ind = np.where(self.measure == self.no_value)
        self.reject(ind, 'no measurement')

    def reject_quality(self):
        """Reject observations under quality requirement"""

        if self.quality_min is not None:
            ind = np.where(self.quality < self.quality_min)
            self.reject(ind, 'poor quality')

    def reject_not_selected(self):
        """Reject observations that do not correspond to the selection"""

        if self.frequency == 0:
            return
        t0 = np.min(self.tcoord) + timedelta(seconds=self.shift)
        t1 = np.max(self.tcoord) + timedelta(seconds=self.shift)
        dif = (t1 - t0).days * 86400 + (t1 - t0).seconds
        t_keep = [t0 + timedelta(seconds=t) for t in range(0, dif+1, self.frequency)]

        ind = [i for i, t in enumerate(self.tcoord) if t not in t_keep]
        self.reject(ind, 'not selected')

    def reject_time_out(self, start, stop):
        """Reject observations out of time window
           Observations at start time are rejected
           Observations at stop time are valid
            - start:    datetime start of time window
            - stop:     datetime stop of time window
        """

        ind = np.union1d(np.where(self.tcoord <= start)[0], np.where(self.tcoord > stop)[0])
        self.reject(ind, 'out of time window')

    def reject_domain_out(self, limits, convert_coord):
        """Reject observations out of domain
            limits:          limits of domain
            convert_coord:   dictionary for coordinate conversion {'original': [], 'model': []}
        """

        ind_rej = []
        self.reject(ind_rej, 'out of domain')

    def reset_time_out(self):
        """Reset observations rejected for being out of time window"""

        ind = np.where(self.rejevent == rejevent_id('out of time window'))
        self.reset(ind)

    def write_observations(self, fname, obs, reftime, timeline, loc_name=None):
        """Write an observation file
            - fname:    file name without extension
            - obs:      dictionary of observations { variable: { location: { 0: np.array( len(timeline) ),
                                                                             'sigma': sigma }}}
            - reftime:  datetime of the reference time
            - timeline: time of the observation  in seconds since reftime
            - loc_name: name of location
        """

        msg = 'The Instrument method write_observations is not implemented'
        raise NotImplementedError(msg)

    def __repr__(self):
        """Information"""

        string = 'Instrument: \n'
        if self.keep:
            string += '   Keep:                          {}\n'.format(self.keep)
        else:
            string += '   Cycling date:                  {}\n'.format(self.dateref.strftime("%d/%m/%Y %H:%M"))
        string += '   Type:                          {}\n'.format(self.obs_type)
        if self.frequency > 0:
            val, unit = sec2unit(self.frequency)
            val2, unit2 = sec2unit(self.shift)
            string += '   Selection:                     frequency: {} {}, shift: {} {}\n'.\
                format(val, unit, val2, unit2)
        else:
            string += '   Selection:                     All observations \n'
        string += '   Minimum quality:               {}\n'.format(self.quality_min)
        string += '   Number of observations:        {}\n'.format(self.nobs)
        string += '   Number of valid observations:  {}\n'.format(self.nvalobs)
        return string
