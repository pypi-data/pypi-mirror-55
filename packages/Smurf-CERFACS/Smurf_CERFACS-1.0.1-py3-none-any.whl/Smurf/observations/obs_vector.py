"""
ObsVector
========

Observation vector y^o:
"""

import logging
import numpy as np
from datetime import datetime
from ..common.vector import Vector
from ..common.matrix import Matrix
from .events import events
from .instrument import instrument_id

# List of observation instrument instances
observation = []

# ======================================================


class ObsVector(Vector):

    logger = logging.getLogger('Observation Vector')
    logging.Logger.setLevel(logger, logging.INFO)

    # =================================== #
    #               Methods               #
    # =================================== #

    def __init__(self, list_obs, start=None, stop=None):
        """Constructor
            - list_obs:    list of observations (instrument instanciation)
            - start:       datetime start of the window
            - stop:        datetime stop of the window
        """
        
        global observation

        # Basic initialisation
        Vector.__init__(self, dim=0)
        if not list_obs:
            return

        # General attributes
        observation = list_obs                       # list of observations (instrument instanciation)
        self.start = start                                # datetime start of the window
        self.stop = stop                                  # datetime stop of the window

        # Observation attributes
        self.obs_type = list(set([t for obs in observation
                                 for t in obs.obs_type]))         # observation types
        self.nobstot = sum([o.nobs for o in observation])    # number of observations in all instruments

        # Check time window
        for obs in observation:
            obs.reject_time_out(self.start, self.stop)
        self.nobs = sum([o.nvalobs for o in observation])    # number of valid observations

        # Coordinates
        self.coord = {'spatial': {}, 'time': []}          # coordinates of observations, all lists contain unique values
        #                                                   { 'spatial': {coord_type1: [], coord_type2: []},
        #                                                     'time': [datetime] }
        self.get_coord()
        self.model_coord = {'spatial': {}, 'time': []}    # coordinates of observations understandable by the model
        #                                                   correponding to coordinates of observations
        #                                                   { 'spatial': {coord_type1: [], coord_type2: []},
        #                                                     'time': [seconds] }
        # Example:
        # self.coord = {'spatial': {('s',): [(3250.,)], ('lat', 'lon'): [(45., 120.)]}, 'time': [(2019, 04, 16, 00)]}
        # self.model_coord = {'spatial': {('s',): [(3250.,)], ('lat', 'lon'): [(2980.)]}, 'time': [10800}

        # Observation information
        self.obs_info = None                              # Observation information
        #                                                   {'index': [], 'time': [], 'scoord': [], 'obs_type': []}
        # For each valid observation, provides
        #   index: a tuple (x,y) where x is the instrument index (self.observation), and y the observation index
        #   time: the datetime
        #   scoord: the spatial coordinate
        #   obs_type: the observation type
        self.sigma = np.empty(0, dtype=np.float32)        # Standard deviation of observations

    def get_coord(self):
        """Gather all coordinates and times"""

        global observation

        # Spatial coordinates
        for obs in observation:
            if obs.spatial_coord not in self.coord['spatial']:
                self.coord['spatial'][obs.spatial_coord] = []
            self.coord['spatial'][obs.spatial_coord].extend(obs.get_spatial_coord())
        for tc in self.coord['spatial']:
            self.coord['spatial'][tc] = sorted(set(self.coord['spatial'][tc]))

        # Time coordinates
        for obs in observation:
            self.coord['time'].extend(obs.get_time_coord())
        self.coord['time'] = sorted(set(self.coord['time']))

    def reject_domain_out(self, limits):
        """Reject observations out of domain"""

        global observation

        # Conversion dictionary
        convert = {}
        for ctype in self.coord['spatial']:
            convert[ctype] = {'original': self.coord['spatial'][ctype],
                              'model': self.model_coord['spatial'][ctype]}

        for obs in observation:
            obs.reject_domain_out(limits, convert[obs.spatial_coord])

        self.nobs = sum([o.nvalobs for o in observation])

    def qc_check(self):
        """Quality check - To be implemented"""

        global observation

        self.nobs = sum([o.nvalobs for o in observation])

    def get_observations(self):
        """Get observations values and information"""

        global observation

        self.obs_info = {'index': [], 'time': [], 'scoord': [], 'obs_type': [], 'instrument': []}
        measure = np.empty(0, dtype=np.float32)

        # Get model time steps with observations
        runlist = sorted(set(self.model_coord['time']))

        # loop on time steps
        for t in runlist:

            # Get corresponding observation times
            tloc = [d for i, d in enumerate(self.coord['time']) if self.model_coord['time'][i] == t]

            # Loop on observation type
            for ot in self.obs_type:

                # Loop on observations
                for o, obs in enumerate(observation):
                    ind, scoord, obsval, sigma = obs.get_observations(ot, tloc)
                    self.obs_info['index'].extend([(o, i) for i in ind])
                    for c in scoord:
                        self.obs_info['scoord'].append(self.model_coord['spatial'][obs.spatial_coord]
                                                       [self.coord['spatial'][obs.spatial_coord].index(c)])
                    self.obs_info['time'].extend([t] * len(ind))
                    self.obs_info['obs_type'].extend([ot] * len(ind))
                    self.obs_info['instrument'].extend([obs.id] * len(ind))
                    measure = np.append(measure, obsval)
                    self.sigma = np.append(self.sigma, sigma)

        # Vector initialisation
        Vector.__init__(self, measure)
        return runlist

    def set_omb(self, d, ist, iend):
        """Set the obs minus bkg values
            - d:       innovation vector, possibly an ensemble vector
            - ist:     observation start index
            - iend:    observation stop index
        """

        global observation

        # The innovation must be a matrix
        if isinstance(d, Vector):
            d = Matrix([d.array])

        indval = self.obs_info['index'][ist:iend]
        for o, obs in enumerate(observation):
            ind_d = [i for i in range(len(indval)) if indval[i][0] == o]
            ind_o = [r[1] for r in indval if r[0] == o]
            obs.set_omb(d[:, ind_d], ind_o)

    def report(self, file, arg=None):
        """Report on observations before updating step
            - file:  path and name of the file for logging the report
            - arg:   arguments to print in the report
        """

        global observation

        if arg is None:
            string = ''
        else:
            string = arg

        string += 'Report on observations:\n'
        string += '   Number of instruments:            {}\n'.format(len(observation))
        string += '   Number of observation type:       {}\n'.format(len(self.obs_type))
        string += '   Total number of observations:     {}\n'.format(self.nobstot)
        string += '   Accepted observations:            {}\n\n'.format(self.nobs)

        for obs in observation:
            string += '{}:\n'.format(obs.name)
            string += '   Path:    {}\n'.format(obs.path)
            try:
                string += '   Files:   {}\n'.format(obs.files[0])
                for f in obs.files[1:]:
                    string += '            {}\n'.format(f)
            except (IndexError, TypeError):
                string += '   Files:   None\n'
            else:
                for ot in obs.obs_type:
                    string += '   Observation type {}:\n'.format(ot)
                    string += '      Total:     {}\n'.format(len(obs.measure[obs.index_obs_type[ot]]))
                    string += '      Acepted:   {}\n'.format(len(obs.measure[obs.index_obs_type[ot]].compressed()))
                    string += '      Rejection event:\n'
                    for r in sorted(set(obs.rejevent[obs.index_obs_type[ot]])):
                        if r == 0:
                            continue
                        string += '         {}: {}\n'.format(events[r], len(np.where(
                            obs.rejevent[obs.index_obs_type[ot]] == r)[0]))
                    string += '\n'

        with open(file, 'w') as fin:
            fin.write(string)

    def write_omb(self, file):
        """Report on assimilated observations
            - file:    path and name of the file
        """

        global observation

        with open(file, 'w') as fout:
            fout.write('Analysis calculated on: {}\n'.format(datetime.now().strftime('%d/%m/%Y %H:%M')))
            fout.write('=======================================================================\n\n')
            fout.write('Instruments:\n')
            for instr in instrument_id:
                if isinstance(instrument_id[instr], dict):
                    for pr in instrument_id[instr]:
                        fout.write('   {} {}: {}\n'.format(instr, pr, instrument_id[instr][pr]))
                else:
                    fout.write('   {}: {}\n'.format(instr, instrument_id[instr]))
            fout.write('\n')
            fout.write('=======================================================================\n\n')
            fout.write(' instr    coord         time         var   obs     sigma   omb \n')
            for o in range(self.nobs):
                t = self.coord['time'][self.model_coord['time'].index(self.obs_info['time'][o])]\
                        .strftime('%d/%m/%Y-%H:%M:%S.%f')
                fout.write('  {}      {}  {}   {}   {}   {}  '.format(self.obs_info['instrument'][o],
                                                                      self.obs_info['scoord'][o], t,
                                                                      self.obs_info['obs_type'][o],
                                                                      self.array[o], self.sigma[o]))
                ind = self.obs_info['index'][o]
                for omb in observation[ind[0]].omb[:, ind[1]]:
                    fout.write('{:+} '.format(omb))
                fout.write('\n')

    @staticmethod
    def read_omb(file):
        """Read report on assimilated observations
            - file:    path and name of the file to read
        """

        try:
            with open(file, 'r') as fin:
                data = fin.readlines()
        except IOError:
            return None

        omb = {}
        for line in data:
            line = line.strip().split()
            if not line or not line[0].isdigit():
                continue
            if line[2][-1] == ')':
                line[1] += line[2]
                del line[2]
            if line[3] not in omb:
                omb[line[3]] = {}
            if line[0] not in omb[line[3]]:
                omb[line[3]][line[0]] = {}
            if line[1] not in omb[line[3]][line[0]]:
                omb[line[3]][line[0]][line[1]] = {}
            time = datetime.strptime(line[2], '%d/%m/%Y-%H:%M:%S.%f')
            omb[line[3]][line[0]][line[1]][time] = np.array([float(o) for o in line[6:]])

        return omb

    @staticmethod
    def reset_time_out():
        """Reset the rejection for time_out"""

        global observation

        for obs in observation:
            obs.reset_time_out()

    def __repr__(self):
        """Information"""

        string = 'Observation vector '
        if self.init:
            string += 'contains {} observations: \n'.format(self.nobs)
        else:
            string += 'not yet initialised \n'
        return string
