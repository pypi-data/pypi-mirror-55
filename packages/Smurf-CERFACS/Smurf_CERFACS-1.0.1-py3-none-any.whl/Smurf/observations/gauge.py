# *- coding: utf-8 -*-
"""
Gauge
=============

Instrument: gauge

"""

import logging
import os
from datetime import datetime, timedelta
import numpy as np
import csv
from .instrument import Instrument
from ..common.functions import sec2unit
from ..common.errors import GaugeError

# ======================================================


class Gauge(Instrument):

    logger = logging.getLogger('Gauge')
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
        self.name = 'Gauge'
        Instrument.__init__(self, config, prm, dateref, size)

        # For postprocessing purpose
        if config == {}:
            return

        # Specific attributes
        try:
            self.station = self.conf['stations']             # Station names
        except (KeyError, TypeError):
            self.station = None
        else:
            if isinstance(self.station, str):
                self.station = [self.station]
        self.zNGF = self.conf['zNGF']                        # Shift of the observation value depending on station
        self.index_station = {}                              # Indices of observations related to a station

        # Coordinates
        self.spatial_coord = tuple(self.conf['coord_type'])  # Coordinate type. Tuple e.g. ('s',)
        self.spatial_dim = len(self.spatial_coord)           # Dimension of coordinates e.g. 1
        self.spcoord = {}                                    # Spatial coordinates array
        for st in self.conf['coordinate']:                   # { station: (curv abs,) }
            if isinstance(self.conf['coordinate'][st], list):
                self.spcoord[st] = tuple(self.conf['coordinate'][st])
            else:
                self.spcoord[st] = (self.conf['coordinate'][st],)

        # Quality
        self.sigma = self.conf['sigma']                      # Error standard deviation
        #                                                      { station: { var1: sigma1, var2: sigma2 }}

        # Temporary attributes
        self.station_tmp = []                                # Stations names from files
        self.obs_type_tmp = []                               # Observation types from files
        self.data = None                                     # Data read from file

        # Read observation files
        self.read_observation_files()

        # Finalise the initialisation
        self.station = self.station_tmp
        self.spcoord = {key: self.spcoord[key] for key in self.station}
        self.zNGF = {key: self.zNGF[key] for key in self.station}
        self.sigma = {key: self.sigma[key] for key in self.station}
        self.obs_type = self.obs_type_tmp
        self.quality = 5 * np.ones(self.nobs, dtype=np.int8)
        self.rejevent = np.zeros(self.nobs, dtype=np.int8)
        self.measure.mask = np.zeros(self.nobs)
        self.omb = np.ma.array(np.zeros((self.size, self.nobs)),
                               mask=np.zeros((self.size, self.nobs)), dtype=np.float32)
        self.data = None
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
            # Extension of the file
            ext = fobs.split('.')[-1]

            # Check configuration information
            try:
                delimiter = self.conf['format'][ext]['delimiter']
            except (KeyError, TypeError):
                delimiter = ';'
            try:
                time_format = self.conf['format'][ext]['time_format']
            except (KeyError, TypeError):
                time_format = "%d/%m/%y %H:%M"

            # Open file and read data
            if ext == 'csv' or ext == 'txt':
                self.open_txt(fobs, delimiter)
            else:
                msg = 'Extension {} for gauge observation not permitted'.format(ext)
                self.logger.error(msg)
                raise GaugeError(msg)

            # Append the data
            self.append_data(time_format, delimiter)

    def open_txt(self, filename, delimiter):
        """Observation data from file of type txt
            - filename:        filename to read
            - delimiter:       delimiter character
        """

        # Read file
        self.logger.debug('Read file {}.'.format(filename))
        try:
            with open(os.path.join(self.path, filename), 'r') as fin:
                data = fin.readlines()
                self.data = [line[:-1].split(delimiter) for line in data]
        except IOError:
            msg = 'The observation file {} does not exist in the path\n{}'.format(filename, self.path)
            self.logger.error(msg)
            raise GaugeError(msg)

    def append_data(self, time_format, delimiter):
        """Append data read in file
            - time_format:    format of the time in the data
            - delimiter:      delimiter used to open file
        """

        # Initialisation
        station = []
        obs_type = []
        time = []
        values = []

        # Read the lines
        for row in self.data:
            try:
                time.append(datetime.strptime(row[0], time_format))
            except ValueError:
                if row[0] == 'types':
                    obs_type = row[1:]
                elif row[0] == 'Jours':
                    station = row[1:]
            else:
                values.append([float(val) for val in row[1:]])

        # Check obs_type
        obs_type = self.check_obs_type(obs_type)

        # Check which stations should be kept
        try:
            length = len(values[0])
        except IndexError:
            msg = 'Delimiter {} or time format {} is probably incorrect'.format(delimiter, time_format)
            self.logger.error(msg)
            raise GaugeError(msg)
        ind_keep_station, keep_station = self.check_which_to_keep('station', station, length)
        # Check which stations and obs types should be kept
        ind_keep_otype, keep_otype = self.check_which_to_keep('obs_type', obs_type, length)
        # Keep intersection
        ind_keep = set(ind_keep_station).intersection(ind_keep_otype)
        keep = [(keep_station[ind_keep_station.index(i)], keep_otype[ind_keep_otype.index(i)]) for i in ind_keep]

        # Append the data
        nbdata = len(time)
        for ind, info in zip(ind_keep, keep):

            # Station information
            try:
                self.index_station[info[0]] = np.append(self.index_station[info[0]],
                                                        range(self.nobs, self.nobs + nbdata))
            except KeyError:
                self.station_tmp.append(info[0])
                self.index_station[info[0]] = np.array(range(self.nobs, self.nobs + nbdata))

            # Observation type information
            try:
                self.index_obs_type[info[1]] = np.append(self.index_obs_type[info[1]],
                                                         range(self.nobs, self.nobs + nbdata))
            except KeyError:
                self.obs_type_tmp.append(info[1])
                self.index_obs_type[info[1]] = np.array(range(self.nobs, self.nobs + nbdata))

            # Time coordinates
            self.tcoord = np.append(self.tcoord, time)

            # Observation values
            self.measure = np.append(self.measure, [v[ind] for v in values])
            self.measure[self.nobs:] += self.zNGF[info[0]]

            # Update number of observations
            self.nobs += nbdata

    def check_which_to_keep(self, check, info, length):
        """Check which station or obs_type to keep
            - check:     'station' or 'obs_type'
            - info:      list of stations or obs types given by the file
            - length:    length of data series
        """

        # Station or observation types
        if check == 'station':
            info_self = self.station
        elif check == 'obs_type':
            info_self = self.obs_type
        else:
            info_self = None

        # Check which observations to keep
        ind_keep = []
        keep = []
        if info_self is None:
            # No information from user, take information from file
            if not info:
                msg = 'Observations from unknown {}'.format(check)
                self.logger.error(msg)
                raise GaugeError(msg)
            else:
                ind_keep = range(length)
                keep = info
        else:
            if not info:
                # No information from file, take information from user
                if len(info_self) != length:
                    msg = 'Mismatch {} number'.format(check)
                    self.logger.error(msg)
                    raise GaugeError(msg)
                ind_keep = range(length)
                keep = info_self
            else:
                # Keep only the stations required by user
                for nf in info_self:
                    try:
                        ind = [i for i in range(len(info)) if info[i] == nf]
                        ind_keep.extend(ind)
                        keep.extend([nf]*len(ind))
                    except ValueError:
                        pass

        return ind_keep, keep

    def get_spatial_coord(self):
        """Return a list of spatial coordinates"""

        return [self.spcoord[st] for st in self.station if np.ma.count(self.measure[self.index_station[st]]) > 0]

    def reject_domain_out(self, limits, convert_coord):
        """Reject observations out of domain
            limits:          limits of domain
            convert_coord:   dictionary for coordinate conversion {'original': [], 'model': []}
        """

        # Find out of domain coordinates
        # -----------------------------
        # Mascaret like for the moment
        # -----------------------------
        model = np.array([f[0] for f in convert_coord['model']])
        mini = limits[0][0]
        maxi = limits[1][0]
        ind = np.union1d(np.where(model < mini)[0], np.where(model > maxi)[0])

        # Reject the observations for these coordinates
        ind_rej = []
        for i in ind:
            station = list(filter(lambda d: (d[1] == convert_coord['original'][i][0]),
                                  self.spcoord.items()))[0][0]
            ind_rej.extend(self.index_station[station])
        self.reject(ind_rej, 'out of domain')

    def get_observations(self, otype, listtime):
        """Return observations of type otype at time t
            - otype:       type of observation
            - listtime:    list of datetime
        """

        ind = []
        for t in listtime:
            ind.extend(np.intersect1d(self.index_obs_type[otype], np.where(self.tcoord == t)[0]))
        indval = [i for i in ind if self.rejevent[i] == 0]
        station = [list(filter(lambda d: (i in d[1]), self.index_station.items()))[0][0] for i in indval]
        spcoord = [self.spcoord[st] for st in station]
        sigma = [self.sigma[st][otype] for st in station]

        return indval, spcoord, self.measure[indval], sigma

    def write_observations(self, fname, obs, reftime, timeline, loc_name=None):
        """Write an observation file
            - fname:    file name without extension
            - obs:      dictionary of observations { variable: { location: { 0: np.array( len(timeline) ),
                                                                             'sigma': sigma }}}
            - reftime:  datetime of the reference time
            - timeline: time of the observation  in seconds since reftime
            - loc_name: name of location
        """

        variable = list(obs.keys())
        location = list(obs[variable[0]].keys())
        loc_name = [list(filter(lambda d: (d[0] == l), loc_name))[0][1] for l in location]
        fname += '.csv'

        with open(fname, 'w') as fout:
            writer = csv.writer(fout, delimiter=';')

            # Write the code stations
            row = ['Codes']
            row.extend([0] * len(variable))
            writer.writerow(row)

            # Write the variables
            row = ['types']
            for var in variable:
                row.extend([var] * len(location))
            writer.writerow(row)

            # Write the columns header
            row = ['Jours']
            row.extend(loc_name * len(variable))
            writer.writerow(row)

            # Write observations
            for t, tl in enumerate(timeline):
                date = reftime + timedelta(seconds=tl)
                row = [date.strftime('%d/%m/%y %H:%M')]
                for var in variable:
                    for loc in location:
                        row.append('{:.2f}'.format(obs[var][loc][0][0, t]))
                writer.writerow(row)

    def __repr__(self):
        """Information"""

        string = 'Gauge: \n'
        if self.keep:
            string += '   Keep:                          {}\n'.format(self.keep)
        else:
            string += '   Cycling date:                  {}\n'.format(self.dateref.strftime("%d/%m/%Y %H:%M"))
        string += '   Type:                          {}\n'.format(self.obs_type)
        string += '   Station:                       {}\n'.format(self.station)
        if self.frequency > 0:
            val, unit = sec2unit(self.frequency)
            val2, unit2 = sec2unit(self.shift)
            string += '   Selection:                     frequency: {} {}, shift: {} {}\n'\
                .format(val, unit, val2, unit2)
        else:
            string += '   Selection:                     All observations \n'
        string += '   Number of observations:        {}\n'.format(self.nobs)
        string += '   Number of valid observations:  {}\n'.format(self.nvalobs)
        return string
