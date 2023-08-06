"""
Barbametre
=============

Instrument: Barbametre

"""

import logging
import numpy as np
import os
import csv
from datetime import timedelta
from .instrument import Instrument


# ======================================================


class Barbametre(Instrument):

    logger = logging.getLogger('Barbametre')
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

        # Basic initialisation
        self.name = 'Barbametre'
        Instrument.__init__(self, config, prm, dateref, size)

        # For postprocessing purpose
        if config == {}:
            return

        # Coordinates
        self.spatial_coord = ('y', 'x')
        self.dim = 2
        self.y = np.empty(0, dtype=np.float32)
        self.x = np.empty(0, dtype=np.float32)

        # Read observation files
        self.read_observation_files()

        # Finalise the initialisation
        self.quality = 5 * np.ones(self.nobs, dtype=np.int8)
        self.rejevent = np.zeros(self.nobs)
        self.measure.mask = np.zeros(self.nobs)
        self.omb = np.ma.array(np.zeros((self.size, self.nobs)),
                               mask=np.zeros((self.size, self.nobs)), dtype=np.float32)
        self.nvalobs = self.nobs

        # Reject observations with no value
        self.reject_no_value()

        # Reject observations with poor quality
        self.reject_quality()

        # Selection of observations
        self.reject_not_selected()

    def read_observation_files(self):
        """Read the observation files"""

        # Loop on files:
        for fobs in self.files:

            # Open file and read data
            with open(os.path.join(self.path, fobs), 'r') as fin:
                data = csv.reader(fin, delimiter=',')
                list_obs_type = []
                for row in data:
                    if self.obs_type is None or row[0] in self.obs_type:
                        list_obs_type.append(row[0])
                        self.tcoord = np.append(self.tcoord, float(row[1]))
                        self.y = np.append(self.y, float(row[2]))
                        self.x = np.append(self.x, float(row[3]))
                        self.measure = np.append(self.measure, float(row[4]))
                        self.sigma = np.append(self.sigma, float(row[5]))
                        if row[0] not in self.index_obs_type:
                            self.index_obs_type[row[0]] = np.empty(0, dtype=np.int8)
                        self.index_obs_type[row[0]] = np.append(self.index_obs_type[row[0]], self.nobs)
                        self.nobs += 1

            # Obs type
            if self.obs_type is None:
                self.obs_type = list(set(list_obs_type))

    def get_spatial_coord(self):
        """Return a list of spatial coordinates for not rejected observations"""

        coords = [(y, x) for i, y, x in zip(range(self.nobs), self.y, self.x) if self.rejevent[i] == 0]
        return list(set(coords))

    def get_observations(self, otype, listtime):
        """Return observations of type otype at time t
            - otype:       type of observation
            - listtime:    list of datetime
        """

        ind = []
        for t in listtime:
            ind.extend(np.intersect1d(self.index_obs_type[otype], np.where(self.tcoord == t)[0]))
        indval = [i for i in ind if self.rejevent[i] == 0]
        measure = self.measure[indval]
        spcoord = [(self.y[i], self.x[i]) for i in indval]
        sigma = self.sigma[indval]

        return indval, spcoord, measure, sigma

    def reject_time_out(self, start, stop):
        """Reject observations out of time window
           Observations at start time are rejected
           Observations at stop time are valid
            - start:    datetime start of time window
            - stop:     datetime stop of time window
        """

        self.tcoord = np.array([start + timedelta(seconds=t) for t in self.tcoord])

    def reject_domain_out(self, limits, convert_coord):
        """Reject observations out of domain
            limits:          limits of domain
            convert_coord:   dictionary for coordinate conversion {'original': [], 'model': []}
        """

        ind = np.where(self.y < limits[0][0])[0]
        ind = np.append(ind, np.where(self.y > limits[0][1])[0])
        ind = np.append(ind, np.where(self.x < limits[1][0])[0])
        ind = np.append(ind, np.where(self.x > limits[1][1])[0])
        self.reject(ind, 'out of domain')

    def write_observations(self, fname, obs, reftime, timeline, loc_name=None):
        """Write an observation file
            - fname:    file name without extension
            - obs:      dictionary of observations { variable: { location: { 0: np.array( len(timeline) ),
                                                                             'sigma': sigma }}}
            - reftime:  datetime of the reference time
            - timeline: time of the observation  in seconds since reftime
            - loc_name: name of location
        """

        fname += '.csv'
        variables = obs.keys()

        with open(fname, 'w') as fout:
            writer = csv.writer(fout, delimiter=',')
            for var in variables:
                for loc in obs[var]:
                    if loc == 'all':
                        for tim in timeline:
                            dim = obs[var][loc][tim].shape
                            if obs[var][loc][tim][0, 0, 0] == 1.e+20:
                                break
                            for y in range(dim[1]):
                                for x in range(dim[2]):
                                    writer.writerow([var, tim, y, x, '{}'.format(obs[var][loc][tim][0, y, x]),
                                                     '{}'.format(obs[var][loc]['sigma'])])
                    else:
                        for t, tim in enumerate(timeline):
                            if obs[var][loc][0][0, t] == 1.e+20:
                                break
                            writer.writerow([var, tim, loc[0], loc[1], '{}'.format(obs[var][loc][0][0, t]),
                                             '{}'.format(obs[var][loc]['sigma'])])

    def __repr__(self):
        """Information"""

        string = 'Barbametre: \n'
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
