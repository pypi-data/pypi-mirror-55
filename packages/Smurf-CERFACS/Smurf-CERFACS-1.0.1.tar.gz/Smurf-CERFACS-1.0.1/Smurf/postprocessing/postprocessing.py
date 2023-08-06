"""
Off-Line Post Processing
========================

"""

import logging
import os
from datetime import datetime, timedelta
import numpy as np
import itertools as it
import copy
import pickle
import ctypes
import matplotlib
import matplotlib.pyplot as plt
from ..experiments.experiment import Experiment as Exp
from ..common.functions import sec2unit, format2sec
from ..observations.instrument import get_instrument_name
from ..observations.instanciate import instanciate as instance_obs
from ..common.errors import PPError

matplotlib.rcParams['lines.linewidth'] = 2
matplotlib.rcParams['axes.labelsize'] = 'large'
default_color = ['k', 'b', 'r', 'g', 'm', 'c', 'y']


# ======================================================


# Functions
def covariance_avg(cov):
    """Compute the covariance average
        - cov: covariance concatenated along time
    """

    cov_avg = np.mean(cov, axis=0)
    return cov_avg


# Class
class PostProcessing(object):

    logger = logging.getLogger('Post Processing')
    logging.Logger.setLevel(logger, logging.INFO)

    # Post processing directory
    @property
    def ppdir(self):
        return self._ppdir
    
    @ppdir.setter 
    def ppdir(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
            self._ppdir = directory
            if not os.path.exists('{}/data'.format(directory)):
                os.makedirs('{}/data'.format(directory))
            if not os.path.exists('{}/plot'.format(directory)):
                os.makedirs('{}/plot'.format(directory))
            if not os.path.exists('{}/obs'.format(directory)):
                os.makedirs('{}/obs'.format(directory))
        except IOError:
            msg = 'Cannot create post processing directory \n{}'.format(directory)
            self.logger.error(msg)
            raise PPError(msg)

    # =================================== #
    #               Methods               #
    # =================================== #
    
    def __init__(self, archdir, name):
        """Constructor for offline post processing
            - archdir:  archiving directory
            - name:     name of the experiment
        """
    
        self.archdir = '{}/{}'.format(archdir, name)             # Archiving path
        self.name = name                                        # Experiment name

        # Directories
        self.ppdir = '{}/post_processing'.format(self.archdir)  # Post processing directory

        # Instanciate the experiment
        self.exp = Exp(archivepath=self.archdir)                # Experiment instance
        # Transform overlap from "time before end" into "time after start"
        self.exp.overlap = sec2unit(self.exp.overlap)
        
        # Define cycling information
        self.cycles = []                  # List of start date for each reanalysis cycle (datetime)
        self.startsec = []                # List of start date for each reanalysis cycle (seconds since start0)
        self.cycles_forecast = []         # List of start date for each forecast cycle (datetime)
        self.startsec_forecast = []       # List of start date for each forecast cycle (seconds since start0)
        self.define_cycles()
        
    def define_cycles(self):
        """Define the cycling information"""
        
        # Reanalysis and Assimilation
        start = self.exp.start
        startsec = self.exp.spinup
        stopsec = startsec + self.exp.length - self.exp.reanalysis        
        while startsec <= stopsec:
            self.cycles.append(start)
            self.startsec.append(startsec)
            if self.exp.overlap == 0:
                start += timedelta(seconds=self.exp.reanalysis)
                startsec += self.exp.reanalysis
            else:
                start += timedelta(seconds=self.exp.overlap)
                startsec += self.exp.overlap
        
        # Forecast
        if self.exp.forecast == 0:
            self.cycles_forecast = []
            self.startsec_forecast = []
            return
        start = self.exp.start + timedelta(seconds=self.exp.reanalysis)
        startsec = self.exp.spinup + self.exp.reanalysis
        stopsec = self.exp.spinup + self.exp.length
        
        while startsec <= stopsec:
            self.cycles_forecast.append(start)
            self.startsec_forecast.append(startsec)
            if self.exp.overlap == 0:
                start += timedelta(seconds=self.exp.reanalysis)
                startsec += self.exp.reanalysis
            else:
                start += timedelta(seconds=self.exp.overlap)
                startsec += self.exp.overlap

    def get_cycling_info(self, shift_start=None, length=None, lead_time=None,
                         shift_base=None, frequency=None):
        """Return the cycling information
            - shift_start: shift the start of the post processing in format [x, unit]
            - length:      partial length in format [x, unit]
            - lead_time:   lead time, [0,'hour'] = base time (end of reanalysis cycle)
                                      None for processing assimilation data
                                      list of lead times for forecast data in format [x, unit]
                           taken into account only if frequency is None
            - shift_base:  shift the base time in the reanalysis window: time = base time - shift,
                           taken into account only if frequency is None and lead_time = [0, 'hour'],
                           for Assim and Dry Run only
            - frequency:   frequency of retrieval in format [x, unit], or list of datetime,
                           for Free Run only
        """

        # Starting index of the cycles
        if shift_start is None or self.exp.exp_type == 'Free Run':
            ind_start = 0
        else:
            ind_start = [t for t, ts in enumerate(self.startsec)
                         if ts >= self.startsec[0] + format2sec(shift_start)][0]
        
        # Length 
        if length is None:
            length = self.exp.length
        else:
            length = format2sec(length)

        # Number of cycles
        if self.exp.exp_type == 'Free Run':
            nbcycles = 1
        else:
            if self.exp.overlap == 0:
                nbcycles = int(length / self.exp.reanalysis)
            else:
                nbcycles = int(length / self.exp.overlap)
            if nbcycles == 0: 
                nbcycles = 1
            elif nbcycles > len(self.cycles[ind_start:]):
                nbcycles = len(self.cycles[ind_start:])

        # Retrieval with a frequency for free runs
        if frequency is not None:
            # Check this is a free run
            if self.exp.exp_type != 'Free Run':
                msg = '{} is not a free run'.format(self.name)
                self.logger.error(msg)
                raise PPError(msg)
            if isinstance(frequency[0], datetime):
                timeline = [(d - self.exp.start0).days * 86400 + (d - self.exp.start0).seconds
                            for d in frequency]
            else:
                frequency = format2sec(frequency)
                start = self.startsec[0] + format2sec(shift_start)
                stop = start + length
                if stop > self.exp.spinup + self.exp.length:
                    stop = self.exp.spinup + self.exp.length
                timeline = [t for t in range(start, stop+1, frequency)]
            return [self.cycles[0].strftime('%Y%m%d-%H%M')], [timeline]

        # Reanalysis
        elif lead_time == [0, 'hour'] or lead_time == [[0, 'hour']]:
            cycles = [c.strftime('%Y%m%d-%H%M') for c in self.cycles[ind_start:ind_start+nbcycles]]
            startsec = self.startsec[ind_start:ind_start+nbcycles]
            # Extract the possibly shifted base time in seconds
            if self.exp.exp_type == 'Free Run':
                shift = format2sec(shift_start)
            else:
                shift = self.exp.reanalysis - format2sec(shift_base)
                if shift < 0:
                    shift = 0
                elif shift > self.exp.reanalysis:
                    shift = self.exp.reanalysis
            timeline = [[t + shift] for t in startsec]
            return cycles, timeline

        # Assimilation
        elif lead_time is None:
            cycles = [c.strftime('%Y%m%d-%H%M') for c in self.cycles[ind_start:ind_start+nbcycles]]
            timeline = self.startsec[ind_start:ind_start+nbcycles]
            return cycles, timeline
        
        # Forecast
        else:
            cycles = [c.strftime('%Y%m%d-%H%M') for c in self.cycles_forecast[ind_start:ind_start+nbcycles]]
            startsec = self.startsec_forecast[ind_start:ind_start+nbcycles]
            # Check that lead_time is a list of format [x,unit]
            if isinstance(lead_time[0], (int, float)):
                lead_time = [lead_time]
            # Lead times in second
            tmp = np.array([format2sec(lt) for lt in lead_time])
            lts = tmp[np.where(tmp <= self.exp.forecast)]            
            timeline = [list(lts+t) for t in startsec]
            return cycles, timeline

    def get_date_info(self, lead_time, date, shift_base=None):
        """Return the cycling information for extracting dates
            - lead_time:   lead time to extract, in format [x, unit], must be a list for forecast lead times,
                           or None for assimilation
            - date:        datetime to extract, can be a list of datetime; all forecast lead times are
                           applied to each datetime
            - shift_base:  shift the base time in the reanalysis window: time = base time - shift,
                           taken into account only if lead_time = [0, 'hour']
        """

        tmp_c = []
        tmp_t = []

        # Assimilation
        if lead_time is None:
            for d in date:
                tmp_c.append([t for t in self.cycles if t <= d][-1])
                tmp_t.append(self.startsec[self.cycles.index(tmp_c[-1])])
            return tmp_c, tmp_t

        # Reanalysis
        if lead_time == [0, 'hour'] or lead_time == [[0, 'hour']]:
            sb = self.exp.reanalysis - format2sec(shift_base)
            if sb < 0:
                sb = 0
            elif sb > self.exp.reanalysis:
                sb = self.exp.reanalysis
            for d in date:
                if self.exp.exp_type == 'Free Run':
                    ind_start = 0
                    mod = d - self.exp.start
                    mod = int(mod.days * 86400 + mod.seconds)
                else:
                    shift = d - self.exp.start
                    shift = int(shift.days * 86400 + shift.seconds) - sb
                    if self.exp.overlap == 0:
                        shift_start = int(shift / self.exp.reanalysis) * self.exp.reanalysis
                        mod = shift % self.exp.reanalysis
                    else:
                        shift_start = int(shift / self.exp.overlap) * self.exp.overlap
                        mod = shift % self.exp.overlap
                    ind_start = [t for t, ts in enumerate(self.startsec) if ts >= self.startsec[0] + shift_start][0]
                    mod += sb
                tmp_c.append(self.cycles[ind_start].strftime('%Y%m%d-%H%M'))
                tmp_t.append(self.startsec[ind_start] + mod)
        
        # Forecast
        else:
            for d in date:
                for ld in lead_time:
                    lds = format2sec(ld)
                    shift = d - self.exp.start
                    shift = int(shift.days * 86400 + shift.seconds)
                    if shift < lds:
                        msg = 'There is no lead time {} for {}'.format(ld, d.strftime('%Y-%m-%d %H:%M'))
                        self.logger.error(msg)
                        raise PPError(msg)
                    if self.exp.exp_type == 'Free Run':
                        tmp_c.append(self.cycles[0].strftime('%Y%m%d-%H%M'))
                        tmp_t.append(self.startsec[0] + shift)
                    else:
                        shift -= lds
                        if self.exp.overlap == 0:
                            shift_start = int(shift / self.exp.reanalysis) * self.exp.reanalysis
                        else:
                            shift_start = int(shift / self.exp.overlap) * self.exp.overlap
                        ind_start = [t for t, ts in enumerate(self.startsec_forecast)
                                     if ts >= self.startsec[0] + shift_start][0]
                        tmp_c.append(self.cycles_forecast[ind_start].strftime('%Y%m%d-%H%M'))
                        tmp_t.append(self.startsec_forecast[ind_start] + lds)
        # Sort the info by cycles
        tmp_c_sort = sorted(list(set(tmp_c)))
        cycles = []
        timeline = []
        dates = []
        for c in tmp_c_sort:
            cycles.append(c)
            ind = np.where(np.array(tmp_c) == c)[0]
            timeline.append([tmp_t[i] for i in ind])
            dates.append([(date[int(i / len(lead_time))], lead_time[i % len(lead_time)]) for i in ind])

        return cycles, timeline, dates

    # =================================== #
    #             Extraction              #
    # =================================== #

    def extract_chronicle(self, location, variable, lead_time=None, shift_start=None, length=None,
                          shift_base=None, frequency=None, bkg=False, step=1, subwindow=1,
                          write=True, svgname=None, overwrite=True):
        """Extract a chronicle of a variable at a particular location
            - location:    model-like coordinate (tuple), can be a list of locations
            - variable:    variable to extract, can be a list of variables
            - lead_time:   lead time to extract, in format [x, unit], must be a list for forecast lead times,
                           default is [0, 'hour'], taken into account only if frequency is None
            - shift_start: shift the start of the post processing in format [x, unit]
            - length:      partial length in format [x, unit]
            - shift_base:  shift the base time in the reanalysis window: time = base time - shift,
                           taken into account only if frequency is None and lead_time = [0, 'hour']
            - frequency:   frequency of retrieval in format [x, unit], or list of datetime,
                           for free run only
            - bkg:         extract background, not analysis
            - step:        assimilation step if bkg is True
            - subwindow:   subwindow to retrieve if bkg is True
            - write:       write the extraction in ppdir/data
            - svgname:     if write = True, file name without extension, can be a list, 1 name per variable
            - overwrite:   if write = True, overwrite the existing file name
        """

        # Location
        if not isinstance(location, list):
            location = [location]

        # Variables
        if not isinstance(variable, list):
            variable = [variable]

        # Lead time
        if lead_time is None:
            lead_time = [0, 'hour']
        if isinstance(lead_time[0], list):
            lead_time.sort()
        else:
            lead_time = [lead_time]
        if lead_time == [[0, 'hour']]:
            subdir = 'reanalysis'
        else:
            subdir = 'forecast'
        lead_time_sec = [format2sec(ld) for ld in lead_time]

        # Background chronicle
        fname = 'step{}/assim/bkg_{:02d}'.format(step, subwindow)

        # Get cycling information
        cycles, timeline = self.get_cycling_info(shift_start, length, lead_time, shift_base, frequency)

        # Prepare result dictionary
        chron = {}
        for var in variable:
            chron[var] = {}
            for loc in location:
                chron[var][loc] = {}
                if frequency is None:
                    for ld in lead_time_sec:
                        chron[var][loc][ld] = np.zeros((self.exp.ens_size, len(cycles)))
                else:
                    chron[var][loc][0] = np.zeros((self.exp.ens_size, len(timeline[0])))

        # Get extraction information
        if bkg:
            self.exp.model.extract_info(location, variable, cycles[0], timeline[0], self.exp.ens_size, fname)
        else:
            self.exp.model.extract_info(location, variable, '{}/{}'.format(cycles[0], subdir),
                                        timeline[0], self.exp.ens_size)

        # Extraction
        # { variable: { location: { lead time in sec: array(ensemble size, experiment length) } } }
        for i, cyc, tl in zip(it.count(), cycles, timeline):
            if bkg:
                res = self.exp.model.extract_from_file(location, variable, cyc, tl, self.exp.ens_size, fname)
            else:
                datedir = '{}/{}'.format(cyc, subdir)
                res = self.exp.model.extract_from_file(location, variable, datedir, tl, self.exp.ens_size)
            for var in variable:
                for loc in location:
                    if frequency is None:
                        for tld, ld in enumerate(lead_time_sec):
                            chron[var][loc][ld][:, i] = res[var][loc][tl[tld]]
                    else:
                        for t, tlf in enumerate(timeline[0]):
                            chron[var][loc][0][0, t] = res[var][loc][tlf]

        # Reformat time line
        tline = {}
        if self.exp.exp_type == 'Free Run':
            tline[0] = timeline[0]
        else:
            for i, ld in enumerate(lead_time_sec):
                tline[ld] = [t[i] for t in timeline]

        # Write the extraction
        if write:

            # File names
            if svgname is None:
                fnames = ['{}/data/chronicle_{}.pic'.format(self.ppdir, var) for var in variable]
            elif isinstance(svgname, list):
                fnames = ['{}/data/{}.pic'.format(self.ppdir, fn) for fn in svgname]
            else:
                fnames = '{}/data/{}.pic'.format(self.ppdir, svgname)

            # Dump
            if isinstance(fnames, list):
                for fn, var in zip(fnames, variable):
                    if not overwrite:
                        fnsvg = fn[:-4]
                        i = 0
                        while os.path.exists(fn):
                            i += 1
                            fn = '{}_{}.pic'.format(fnsvg, i)
                    gherkins = [[location, [var], lead_time, shift_start, length, shift_base, frequency],
                                tline, self.exp.ens_size, chron[var]]
                    pickle.dump(gherkins, open(fn, 'wb'))
            else:
                if not overwrite:
                    fnsvg = fnames[:-4]
                    i = 0
                    while os.path.exists(fnames):
                        i += 1
                        fnames = '{}_{}.pic'.format(fnsvg, i)
                gherkins = [[location, variable, lead_time, shift_start, length, shift_base, frequency],
                            tline, self.exp.ens_size, chron]
                pickle.dump(gherkins, open(fnames, 'wb'))

        return chron, tline

    def extract_field(self, variable, lead_time=None, date=None, bkg=False, step=1, subwindow=1,
                      shift_base=None, write=True, svgname=None, overwrite=True):
        """Extract a variable field at a particular date
            - variable:    variable to extract, can be a list of variables
            - lead_time:   lead time to extract, in format [x, unit], must be a list for forecast lead times,
                           default is [0, 'hour'],
            - date:        datetime to extract, can be a list of datetime; all forecast lead times are
                           applied to each datetime
            - bkg:         extract background, not analysis
            - step:        assimilation step if bkg is True
            - subwindow:   subwindow to retrieve if bkg is True
            - shift_base:  shift the base time in the reanalysis window: time = base time - shift,
                           taken into account only if lead_time = [0, 'hour']
            - write:       write the extraction in ppdir/data
            - svgname:     if write = True, file name without extension, can be a list, 1 name per variable
            - overwrite:   if write = True, overwrite the existing file name
        """

        # Variables
        if not isinstance(variable, list):
            variable = [variable]

        # Lead time
        if lead_time is None:
            lead_time = [0, 'hour']
        if isinstance(lead_time[0], list):
            lead_time.sort()
        else:
            lead_time = [lead_time]
        if lead_time == [[0, 'hour']] or self.exp.exp_type == 'Free Run':
            subdir = 'reanalysis'
        else:
            subdir = 'forecast'
        lead_time_sec = [format2sec(ld) for ld in lead_time]

        # Date
        if date is None:
            date = [self.exp.start + timedelta(seconds=self.exp.reanalysis)]
        if not isinstance(date, list):
            date = [date]
        else:
            date.sort()
        
        # Background field
        fname = 'step{}/assim/bkg_{:02d}'.format(step, subwindow)

        # Get cycling information
        cycles, timeline, dates = self.get_date_info(lead_time, date, shift_base)

        # Prepare result dictionary
        field = {}
        for var in variable:
            field[var] = {}
            for dt in date:
                field[var][dt] = {}
                for ld in lead_time_sec:
                    field[var][dt][ld] = np.empty(0, dtype=np.float32)

        # Get extraction information
        if bkg:
            self.exp.model.extract_info('all', variable, cycles[0], timeline[0], self.exp.ens_size, fname)
        else:
            self.exp.model.extract_info('all', variable, '{}/{}'.format(cycles[0], subdir),
                                        timeline[0], self.exp.ens_size)

        # Extraction
        # { variable: { datetime date: { lead time in sec: array(ensemble size, model dimension) } } }
        for i, cyc, tl in zip(it.count(), cycles, timeline):
            if bkg:
                res = self.exp.model.extract_from_file('all', variable, cyc, tl, self.exp.ens_size, fname)
            else:
                datedir = '{}/{}'.format(cyc, subdir)
                res = self.exp.model.extract_from_file('all', variable, datedir, tl, self.exp.ens_size)
            for var in variable:
                for j in range(len(tl)):
                    dinfo = dates[i][j]
                    field[var][dinfo[0]][format2sec(dinfo[1])] = res[var]['all'][tl[j]]

        # Write the extraction
        if write:

            # File names
            if svgname is None:
                fnames = ['{}/data/field_{}.pic'.format(self.ppdir, var) for var in variable]
            elif isinstance(svgname, list):
                fnames = ['{}/data/{}.pic'.format(self.ppdir, fn) for fn in svgname]
            else:
                fnames = '{}/data/{}.pic'.format(self.ppdir, svgname)

            # Dump
            if isinstance(fnames, list):
                for fn, var in zip(fnames, variable):
                    if not overwrite:
                        fnsvg = fn[:-4]
                        i = 0
                        while os.path.exists(fn):
                            i += 1
                            fn = '{}_{}.pic'.format(fnsvg, i)
                    gherkins = [[[var], lead_time, date], None, self.exp.ens_size, field[var]]
                    pickle.dump(gherkins, open(fn, 'wb'))
            else:
                if not overwrite:
                    fnsvg = fnames[:-4]
                    i = 0
                    while os.path.exists(fnames):
                        i += 1
                        fnames = '{}_{}.pic'.format(fnsvg, i)
                gherkins = [[variable, lead_time, date], None, self.exp.ens_size, field]
                pickle.dump(gherkins, open(fnames, 'wb'))

        return field

    def extract_assim(self, variable, index, assim_type='inc', step=1, date=None, shift_start=None,
                      length=None, subwindow=1, write=True, svgname=None, overwrite=True):
        """Extract background, analysis and increment from assimilation files
            - variable:    control variable to extract, can be a composite element, can be a list of variables
            - index:       index for each variables, can be a list of indices
            - assim_type:  'bkg', 'anl', or 'inc' (default). Can be a list of types
            - step:        assimilation step
            - date:        datetime to extract, can be a list of datetime, or None for the whole chronicle
            - shift_start: shift the start of the post processing in format [x, unit], only if date is None
            - length:      partial length in format [x, unit], only if date is None
            - subwindow:   subwindow to retrieve, can be a list
            - write:       write the extraction in ppdir/data
            - svgname:     if write = True, file name without extension, can be a list, 1 name per variable
            - overwrite:   if write = True, overwrite the existing file name
        """

        # Check assimilation run
        if self.exp.exp_type != 'Assim Run':
            msg = '{} is not an assimilation run'.format(self.exp.name)
            self.logger.error(msg)
            raise PPError(msg)

        # Variables
        if not isinstance(variable, list):
            variable = [variable]

        # Indices
        if not isinstance(index, list):
            index = [index]
        if len(variable) == 1 and not isinstance(index[0], list):
            index = [index]
        tmp = []
        for v in range(len(variable)):
            if isinstance(index[v], list):
                tmp.append(index[v])
            else:
                tmp.append([index[v]])
        index = tmp

        # Assimilation type
        if not isinstance(assim_type, list):
            assim_type = [assim_type]

        # Subwindow
        if not isinstance(subwindow, list):
            subwindow = [subwindow]

        # Get cycling information
        if date is None:
            cycles, timeline = self.get_cycling_info(shift_start, length)
        else:
            if not isinstance(date, list):
                date = [date]
            else:
                date.sort()
            cycles, timeline = self.get_date_info(None, date)
            cycles = [d.strftime('%Y%m%d-%H%M') for d in cycles]

        # Prepare result dictionary
        asm = {}
        for v, var in enumerate(variable):
            asm[var] = {}
            for ind in index[v]:
                asm[var][ind] = {}
                for sub in subwindow:
                    asm[var][ind][sub] = {}
                    for tp in assim_type:
                        asm[var][ind][sub][tp] = np.empty(0, dtype=np.float32)

        # Extraction
        # { variable: { index: { subwindow: { assim type: array(ensemble size, variable length, date length) } } } }
        for cyc in cycles:
            res = self.exp.assim[step].extract_increment(variable, index, assim_type, cyc, subwindow)
            for v, var in enumerate(variable):
                for ind in index[v]:
                    for sub in subwindow:
                        for tp in assim_type:
                            r = res[sub-1][var][ind][tp]
                            dim = list(np.shape(r))
                            dim.append(1)
                            r = np.reshape(r, dim)
                            axis = len(dim) - 1
                            try:
                                asm[var][ind][sub][tp] = np.concatenate((asm[var][ind][sub][tp], r), axis=axis)
                            except ValueError:
                                asm[var][ind][sub][tp] = r

        # Write the extraction
        if write:

            # File names
            if svgname is None:
                fnames = ['{}/data/assim_{}.pic'.format(self.ppdir, var) for var in variable]
            elif isinstance(svgname, list):
                fnames = ['{}/data/{}.pic'.format(self.ppdir, fn) for fn in svgname]
            else:
                fnames = '{}/data/{}.pic'.format(self.ppdir, svgname)

            # Dump
            if isinstance(fnames, list):
                for fn, var in zip(fnames, variable):
                    if not overwrite:
                        fnsvg = fn[:-4]
                        i = 0
                        while os.path.exists(fn):
                            i += 1
                            fn = '{}_{}.pic'.format(fnsvg, i)
                    gherkins = [[[var], index, assim_type, step, date, shift_start, length],
                                timeline, self.exp.ens_size, asm[var]]
                    pickle.dump(gherkins, open(fn, 'wb'))
            else:
                if not overwrite:
                    fnsvg = fnames[:-4]
                    i = 0
                    while os.path.exists(fnames):
                        i += 1
                        fnames = '{}_{}.pic'.format(fnsvg, i)
                gherkins = [[variable, index, assim_type, step, date, shift_start, length],
                            timeline, self.exp.ens_size, asm]
                pickle.dump(gherkins, open(fnames, 'wb'))

        return asm, timeline

    # =================================== #
    #                Read                 #
    # =================================== #

    def read_extract(self, filename):
        """Read extract files
            -   filename:   name of the file to read in self.ppdir/data, can be a list of files
        """
            
        if not isinstance(filename, list):
            filename = [filename]

        gherkins = []
        for fname in filename:
            fname = '{}/data/{}.pic'.format(self.ppdir, fname)
            gherkins.append(pickle.load(open(fname, 'rb')))

        if len(gherkins) == 1:
            return gherkins[0]
        else:
            return gherkins

    def read_covariance(self, cov_type=None, step=1, date=None, shift_start=None, length=None, subwindow=1):
        """Read covariances from assimilation files
            - cov_type:    covariances 'B', 'A', 'HBHt', 'BHt', can be a list of covariances, or None for all
            - step:        assimilation step
            - date:        datetime to extract, can be a list of datetime, or None for the whole chronicle
            - shift_start: shift the start of the post processing in format [x, unit], only if date is None
            - length:      partial length in format [x, unit], only if date is None
            - subwindow:   subwindow to retrieve, can be a list
        """

        # Check assimilation run
        if self.exp.exp_type != 'Assim Run':
            msg = '{} is not an assimilation run'.format(self.exp.name)
            self.logger.error(msg)
            raise PPError(msg)

        covlist = ['B', 'A', 'HBHt', 'BHt']
        # Covariance
        if cov_type is None:
            cov_type = covlist
        elif not isinstance(cov_type, list):
            cov_type = [cov_type]

        # Subwindow
        if not isinstance(subwindow, list):
            subwindow = [subwindow]

        # Get cycling information
        if date is None:
            cycles, timeline = self.get_cycling_info(shift_start, length)

        else:
            if not isinstance(date, list):
                date = [date]
            else:
                date.sort()
            cycles, timeline = self.get_date_info(None, date)
            cycles = [d.strftime('%Y%m%d-%H%M') for d in cycles]
            timeline = None

        # Prepare result dictionary
        cov = {}
        for c in cov_type:
            cov[c] = {}
            for s in subwindow:
                cov[c][s] = np.empty(0, dtype=np.float32)

        # Read covariances
        # {  covariance type: { subwindow: array(date length, covariance dimension) } }
        control = None
        for s in subwindow:
            for datedir in cycles:
                tmp, control = self.exp.assim[step].read_cov(cov_type, datedir, s)
                for i, c in enumerate(cov_type):
                    cov_c = tmp[i]
                    dim = [1]
                    dim.extend(np.shape(cov_c))
                    cov_c = np.reshape(cov_c, dim)
                    try:
                        cov[c][s] = np.concatenate((cov[c][s], cov_c), axis=0)
                    except ValueError:
                        cov[c][s] = cov_c

        return cov, control, timeline

    def read_omb(self, variable=None, instrument=None, location=None, step=1, date=None,
                 shift_start=None, length=None):
        """Read observation minu background from assimilation files
            - variable:    observed variable to read, can be a list of variables, or None for all variables
            - instrument:  observation instrument, can be a list of instrument, or None for all instruments
            - location:    observation coordinate (tuple), can be a list of locations, or None for all locations
            - step:        assimilation step
            - date:        datetime to extract, can be a list of datetime, or None for the whole chronicle
            - shift_start: shift the start of the post processing in format [x, unit], only if date is None
            - length:      partial length in format [x, unit], only if date is None
        """

        # Check assimilation run
        if self.exp.exp_type != 'Assim Run':
            msg = '{} is not an assimilation run'.format(self.exp.name)
            self.logger.error(msg)
            raise PPError(msg)

        # Variable
        if variable is not None and not isinstance(variable, list):
            variable = [variable]

        # Instrument
        if instrument is not None and not isinstance(instrument, list):
            instrument = [instrument]

        # Location
        if location is not None and not isinstance(location, list):
            location = [location]

        # Get cycling information
        if date is None:
            cycles, timeline = self.get_cycling_info(shift_start, length)
        else:
            if not isinstance(date, list):
                date = [date]
            else:
                date.sort()
            cycles, timeline = self.get_date_info(None, date)
            cycles = [d.strftime('%Y%m%d-%H%M') for d in cycles]

        # Read omb
        # { variable: { instrument: { location: { timeline: array(date length),
        #                                         omb: array(ensemble size, date length) }}}}
        omb = {}
        for datedir, tl in zip(cycles, timeline):
            res = self.exp.assim[step].read_assim_output_files(datedir)
            if res is None:
                continue
            try:
                varbs = set(variable[:])
            except TypeError:
                varbs = set(res.keys())
            try:
                instrs = set(instrument[:])
            except TypeError:
                instrs = set([key for inst in res.values() for key in inst])
            try:
                locs = set(location[:])
            except TypeError:
                locs = []
                for v in varbs:
                    locs.extend([key for loc in res[v].values() for key in loc])
                locs = set(locs)
            for v in varbs.intersection(set(res.keys())):
                if v not in omb:
                    omb[v] = {}
                for i in instrs.intersection(set(res[v].keys())):
                    if i not in omb[v]:
                        omb[v][i] = {}
                    for l in locs.intersection(set(res[v][i].keys())):
                        if l not in omb[v][i]:
                            omb[v][i][l] = {'date': np.empty(0), 'timeline': np.empty(0),
                                            'omb': np.empty(0, dtype=np.float32)}
                        tmp = list(res[v][i][l].items())
                        omb[v][i][l]['timeline'] = np.concatenate((omb[v][i][l]['timeline'], [tl] * len(tmp)))
                        omb[v][i][l]['date'] = np.concatenate((omb[v][i][l]['date'], [t[0] for t in tmp]))
                        tmp = np.array([t[1] for t in tmp])
                        try:
                            omb[v][i][l]['omb'] = np.append(omb[v][i][l]['omb'], tmp.T, axis=1)
                        except (ValueError, TypeError):
                            omb[v][i][l]['omb'] = tmp.T

        return omb

    # =================================== #
    #                Plot                 #
    # =================================== #

    def time_axis(self, timeline, unit='sec'):
        """Translate the timeline in seconds into a date to define xtick labels
            - timeline:   timeline in seconds
            - unit:       unit to apply 'sec', 'min', 'hour', 'day'; if None calculate the best one
        """

        # Dates
        xdate = np.array([self.exp.start0 + timedelta(seconds=t) for t in timeline])

        # Time unit
        unit_dict = {'day':  ['%Y%m%d', '%d/%m %Hh'],
                     'hour': ['%Y%m%d %H', '%d/%m %Hh'],
                     'min':  ['%Y%m%d %H%M', '%H:%M'],
                     'sec':  ['%Y%m%d %H%M%S', '%H:%M%S']}

        # Define labels
        xticks = []
        xlabels = []
        for uu in ['day', 'hour', 'min', 'sec']:
            if unit is not None and unit != uu:
                continue
            xsearch = [d.strftime(unit_dict[uu][0]) for d in xdate]
            xsearch_set = sorted(set(xsearch))
            if len(xsearch_set) > 5 or unit == uu:
                xticks = [xsearch.index(d) for d in xsearch_set]
                if len(xticks) > 10:
                    x = xticks[:]
                    xticks = [x[i] for i in range(0, len(x), int(len(x) / 10))]
                xlabels = [xdate[i].strftime(unit_dict[uu][1]) for i in xticks]
                break

        return xticks, xlabels

    def plot_chronicle(self, variable, chron, timeline, index=None, time_unit=None, mean_only=False, color=None,
                       ens_color=None, alpha=0.3, title=None, labels=None, show=True, svgname=None, ext='png'):
        """Plot a chronicle.
            - variable:   variable to plot
            - chron:      2D chronicle to plot (ensemble size, timeline length), can be a list of chronicles
            - timeline:   list of date in seconds
            - index:      index of the parameter when variable has several, None otherwise with 0 is default
            - time_unit:  time unit for the x axis
            - mean_only:  plot the mean of the ensemble but not the members
            - color:      color of the chronicle to plot, must be a list of colors if chron is a list
            - ens_color:  if not None, the chronicles withe ensemble size > 1 are plot with ens_color,
                          and the mean of the ensemble is plot with color
            - alpha:      alpha for the ens_color if not None
            - title:      title of plot
            - labels:     label or list of labels for chron
            - show:       show the plot
            - svgname:    if not None name of file to save the plot without extension and path in ppdir/plot
            - ext:        extension of file name if svgname is not None
        """

        # Chronicle
        if not isinstance(chron, list):
            chron = [chron]

        # x axis
        xticks, xlabels = self.time_axis(timeline, time_unit)

        # Colors
        if color is None:
            nb = int(len(chron) / len(default_color))
            if len(chron) % len(default_color) > 0:
                nb += 1
            color = default_color * nb
        elif not isinstance(color, list):
            color = [color]

        # Labels
        if labels is None:
            labels = [''] * len(chron)

        # Plot chronicles
        plt.figure()
        for i, c in enumerate(chron):
            if np.ndim(c) == 3:
                if index is None:
                    c = c[:, 0, :]
                else:
                    c = c[:, index, :]
            if mean_only:
                plt.plot(np.mean(c, axis=0), color[i], label=labels[i])
            else:
                if np.shape(c)[0] == 1 or ens_color is None:
                    plt.plot(c.T, color[i], label=labels[i])
                else:
                    plt.plot(c.T, ens_color, alpha=alpha)
                    plt.plot(np.mean(c, axis=0), color[i], label=labels[i])

        # Plot title and labels
        if labels[0]:
            plt.legend()
        if title is not None:
            plt.title(title)
        plt.xticks(xticks, xlabels, rotation=20)
        try:
            vinfo = self.exp.model.parameter['variables'][variable]
            if isinstance(vinfo[0], list):
                if index is None:
                    vinfo = [vinfo[0][0], vinfo[1][0]]
                else:
                    vinfo = [vinfo[0][index], vinfo[1][index]]
        except KeyError:
            varctl = list(filter(lambda d: (variable in d[1][0]),
                                 self.exp.model.parameter['composite'].items()))[0][0]
            varind = self.exp.model.parameter['composite'][varctl][0].index(variable)
            vinfo = [self.exp.model.parameter['variables'][varctl][0][varind],
                     self.exp.model.parameter['composite'][varctl][1][varind]]
        if vinfo[1]:
            inunit = 'in {}'.format(vinfo[1])
        else:
            inunit = ''
        plt.ylabel('{} {}'.format(vinfo[0], inunit))

        # Grid
        plt.grid()
        plt.xlim(0, len(timeline)-1)

        # Save plot
        if svgname is not None:
            plt.savefig('{}/plot/{}.{}'.format(self.ppdir, svgname, ext), format=ext)

        # Show
        if show:
            plt.show()
        else:
            plt.close()

    def plot_field(self, variable, field, xaxis, xaxis_label=None, mean_only=False, color=None,
                   ens_color=None, alpha=0.3, title=None, labels=None, xticks=None, xtick_labels=None,
                   show=True, svgname=None, ext='png'):
        """Plot a field.
            - variable:     variable to plot
            - field:        2D field to plot (ensemble size, model dimension), can be a list of fields
            - xaxis:        x axis data
            - xaxis_label:  label for x axis
            - mean_only:    plot the mean of the ensemble but not the members
            - color:        color of the field to plot, must be a list of colors if chron is a list
            - ens_color:    if not None, the chronicles withe ensemble size > 1 are plot with ens_color,
                            and the mean of the ensemble is plot with color
            - alpha:        alpha for the ens_color if not None
            - title:        title of plot
            - labels:       label or list of labels for chron
            - xticks:       ticks for the x axis
            - xtick_labels  label for the x axis ticks
            - show:         show the plot
            - svgname:      if not None name of file to save the plot without extension and path in ppdir/plot
            - ext:          extension of file name if svgname is not None
        """

        # Field
        if not isinstance(field, list):
            field = [field]

        # Colors
        if color is None:
            if isinstance(field, list):
                nb = int(len(field) / len(default_color))
                if len(field) % len(default_color) > 0:
                    nb += 1
            else:
                nb = 1
            color = default_color * nb
        elif not isinstance(color, list):
            color = [color]

        # Labels
        if labels is None:
            labels = [''] * len(field)

        # Plot field
        plt.figure()
        for i, f in enumerate(field):
            if mean_only:
                plt.plot(xaxis, np.mean(f, axis=0), color[i], label=labels[i])
            else:
                if np.shape(f)[0] == 1 or ens_color is None:
                    plt.plot(xaxis, f.T, color[i], label=labels[i])
                else:
                    plt.plot(xaxis, f.T, ens_color, alpha=alpha)
                    plt.plot(xaxis, np.mean(f, axis=0), color[i], label=labels[i])

        # Plot title and labels
        if labels[0]:
            plt.legend()
        if title is not None:
            plt.title(title)
        if xticks is not None:
            plt.xticks(xticks, xtick_labels)
        if xaxis_label is not None:
            plt.xlabel(xaxis_label)
        vinfo = self.exp.model.parameter['variables'][variable]
        if vinfo[1]:
            inunit = 'in {}'.format(vinfo[1])
        else:
            inunit = ''
        plt.ylabel('{} {}'.format(vinfo[0], inunit))

        # Grid
        plt.grid()
        plt.xlim(xaxis[0], xaxis[-1])

        # Save plot
        if svgname is not None:
            plt.savefig('{}/plot/{}.{}'.format(self.ppdir, svgname, ext), format=ext)

        # Show
        if show:
            plt.show()
        else:
            plt.close()

    def plot_covariance(self, cov, cov_type, control=None, cmap='bwr', title=None,
                        vmin=None, vmax=None, show=True, svgname=None, ext='png'):
        """Plot covariance
            - cov:          covariance or correlation
            - cov_type:     covariance type 'B', 'A', 'HBHt', 'BHt'
            - control:      control variables, can be None if cov_type is 'HBHt'
            - cmap:         color map
            - title:        title of plot
            - vmin:         minimum value
            - vmax:         maximum value
            - show:         show the plot
            - svgname:      if not None name of file to save the plot without extension and path in ppdir/plot
            - ext:          extension of file name if svgname is not None
        """

        if control is None:
            control = [('obs', i, 0) for i in range(cov.shape[0])]

        # Plot covariance
        plt.figure()
        if vmin is None or vmax is None:
            cb = plt.pcolormesh(cov, cmap=cmap)
        else:
            cb = plt.pcolormesh(cov, cmap=cmap, vmin=vmin, vmax=vmax, edgecolors='face')
        plt.colorbar(cb)
        plt.gca().invert_yaxis()

        # Plot title and labels
        if title is not None:
            plt.title(title)
        label = [ctl[0] for ctl in control]
        if cov_type == 'B' or cov_type == 'A':
            plt.xticks(range(len(label)), label, ha='left', rotation=20)
            plt.yticks(range(len(label)), label, va='top', rotation=20)
        elif cov_type == 'BHt':
            plt.xlabel('Observations')
            plt.yticks(range(len(label)), label, va='top', rotation=20)
        elif cov_type == 'HBHt':
            plt.xlabel('Observations')
            plt.ylabel('Observations')

        # Save plot
        if svgname is not None:
            plt.savefig('{}/plot/{}.{}'.format(self.ppdir, svgname, ext), format=ext)

        # Show
        if show:
            plt.show()
        else:
            plt.close()

    def plot_covariance_norm(self, cov, timeline, subwindow=1, time_unit=None, title=None,
                             show=True, svgname=None, ext='png'):
        """Plot covariance norm of B against norm of A
            - cov:          covariance or correlation
            - timeline:     list of date in seconds
            - subwindow:    subwindow of covariance
            - time_unit:    time unit for the x axis
            - title:        title of plot
            - show:         show the plot
            - svgname:      if not None name of file to save the plot without extension and path in ppdir/plot
            - ext:          extension of file name if svgname is not None
        """

        # Calculate the norm of the covariance
        normb = self.cov_norm(cov['B'][subwindow])
        norma = self.cov_norm(cov['A'][subwindow])

        # x axis
        xticks, xlabels = self.time_axis(timeline, time_unit)

        # Plot
        plt.figure()
        plt.plot(normb, 'b', label='B')
        plt.plot(norma, 'r', label='A')

        # Plot title and labels
        plt.legend()
        if title is not None:
            plt.title(title)
        plt.xticks(xticks, xlabels, rotation=20)
        plt.ylabel('Norm')

        # Grid
        plt.grid()
        plt.xlim(0, len(timeline)-1)

        # Save plot
        if svgname is not None:
            plt.savefig('{}/plot/{}.{}'.format(self.ppdir, svgname, ext), format=ext)

        # Show
        if show:
            plt.show()
        else:
            plt.close()

    def plot_correlation_mean(self, cov, control, subwindow=1, vmin=None, vmax=None, title=None,
                              show=True, svgname=None, ext='png'):
        """Plot correlation mean of B and 'A'
            - cov:          covariance or correlation dictionary containing 'A' and 'B'
            - control:      control variables
            - subwindow:    subwindow of covariance
            - time_unit:    time unit for the x axis
            - vmin:         minimum value
            - vmax:         maximum value
            - title:        title of plot
            - show:         show the plot
            - svgname:      if not None name of file to save the plot without extension and path in ppdir/plot
            - ext:          extension of file name if svgname is not None
        """

        # Calculate the mean of the covariance
        meanb = self.cov_mean(cov['B'][subwindow])
        meana = self.cov_mean(cov['A'][subwindow])

        # Calculate the correlations
        corb, _ = self.cor_from_cov(meanb)
        cora, _ = self.cor_from_cov(meana)

        # Plot
        if title is None:
            titleb = None
            titlea = None
        else:
            titleb = 'Background error ' + title
            titlea = 'Analysis error ' + title
        if svgname is None:
            svgnameb = None
            svgnamea = None
        else:
            svgnameb = svgname + '_B'
            svgnamea = svgname + '_A'
        self.plot_covariance(corb, 'B', control, title=titleb, vmin=vmin, vmax=vmax,
                             show=show, svgname=svgnameb, ext=ext)
        self.plot_covariance(corb, 'A', control, title=titlea, vmin=vmin, vmax=vmax,
                             show=show, svgname=svgnamea, ext=ext)

    def plot_covariance_evolution(self, cov, timeline, cov_type, cor=False, control=None, index=0,
                                  time_unit=None, cmap='bwr', title=None, vmin=None, vmax=None,
                                  show=True, svgname=None, ext='png'):
        """Plot covariance evolution
            - cov:          covariance or correlation
            - timeline:     list of date in seconds
            - cov_type:     covariance type 'B', 'A', 'HBHt', 'BHt'
            - cor:          if True, plot correlation and not covariance
            - control:      control variables, can be None if cov_type is 'HBHt'
            - index:        index of the control variable to plot
            - time_unit:    time unit for the x axis
            - cmap:         color map
            - title:        title of plot
            - vmin:         minimum value
            - vmax:         maximum value
            - show:         show the plot
            - svgname:      if not None name of file to save the plot without extension and path in ppdir/plot
            - ext:          extension of file name if svgname is not None
        """

        if cor:
            cov_plot, _ = self.cor_from_cov(cov)
        else:
            cov_plot = cov

        # x axis
        xticks, xlabels = self.time_axis(timeline, time_unit)

        # Covariance
        cov_index = cov_plot[:, index, :].T

        # Plot covariance
        plt.figure()
        if vmin is None or vmax is None:
            cb = plt.pcolormesh(cov_index, cmap=cmap)
        else:
            cb = plt.pcolormesh(cov_index, cmap=cmap, vmin=vmin, vmax=vmax, edgecolors='face')
        plt.colorbar(cb)
        plt.gca().invert_yaxis()

        # Plot title and labels
        if title is not None:
            plt.title(title)
        plt.xticks(xticks, xlabels, rotation=20)
        label = [ctl[0] for ctl in control]
        if cov_type == 'B' or cov_type == 'A':
            plt.yticks(range(len(label)), label, va='top', rotation=20)
        elif cov_type == 'BHt' or cov_type == 'HBHt':
            plt.ylabel('Observations')

        # Save plot
        if svgname is not None:
            plt.savefig('{}/plot/{}.{}'.format(self.ppdir, svgname, ext), format=ext)

        # Show
        if show:
            plt.show()
        else:
            plt.close()

    def plot_stat_chronicle(self, variable, chron, time_unit=None, color=None,
                            title=None, show=True, svgname=None, ext='png'):
        """Plot statistics chronicle, e.g. omb statistics
            - variable:   variable whose statistics are plotted
            - chron:      dictionary { 'mean_t': array(len time), 'rms_t': array(len time),
                                       'spread_t': array(len time), 'timeline': array(len time) }
            - time_unit:  time unit for the x axis
            - color:      color for rms (and mean), and possibly spread, defautlt is red and blue
            - title:      title of plot
            - show:       show the plot
            - svgname:    if not None name of file to save the plot without extension and path in ppdir/plot
            - ext:        extension of file name if svgname is not None
        """

        # timeline
        timeline = chron['timeline']
        
        # x axis
        xticks, xlabels = self.time_axis(timeline, time_unit)
        
        # Colors
        if color is None:
            color = ['g', 'r', 'b']
        elif not isinstance(color, list):
            color = [color, 'b']

        # Plot chronicles
        plt.figure()
        plt.plot(chron['mean_t'], '{}'.format(color[0]), label='mean')
        plt.plot(chron['rms_t'], color[1], label='rms')
        if 'spread_t' in chron:
            plt.plot(chron['spread_t'], color[2], label='spread')
        plt.plot(np.zeros(len(timeline)), 'k')

        # Plot title and labels
        plt.legend()
        if title is not None:
            plt.title(title)
        plt.xticks(xticks, xlabels, rotation=20)
        vinfo = self.exp.model.parameter['variables'][variable]
        if vinfo[1]:
            inunit = 'in {}'.format(vinfo[1])
        else:
            inunit = ''
        plt.ylabel('{} {}'.format(vinfo[0], inunit))

        # Grid
        plt.grid()
        plt.xlim(0, len(timeline) - 1)

        # Save plot
        if svgname is not None:
            plt.savefig('{}/plot/{}.{}'.format(self.ppdir, svgname, ext), format=ext)

        # Show
        if show:
            plt.show()
        else:
            plt.close()

    def plot_rank(self, rank, title=None, show=True, svgname=None, ext='png'):
        """Plot the rank diagram
            - rank:         rank dictionary {'cnt': nb obs, 'rank': rank}
            - title:        title of plot
            - show:         show the plot
            - svgname:      if not None name of file to save the plot without extension and path in ppdir/plot
            - ext:          extension of file name if svgname is not None
        """

        size = rank['rank'].size
        rank_norm = rank['rank'] / rank['cnt']
        plt.figure()
        plt.bar(range(size), rank_norm, align='edge')
        plt.plot(np.ones(size + 1) / size, 'k', linewidth=1.5)

        # Title
        if title is not None:
            plt.title(title)

        # Grid
        plt.xlim((0, size))

        # Save plot
        if svgname is not None:
            plt.savefig('{}/plot/{}.{}'.format(self.ppdir, svgname, ext), format=ext)

        # Show
        if show:
            plt.show()
        else:
            plt.close()

    # =================================== #
    #              Statistics             #
    # =================================== #

    def cov_norm(self, cov):
        """Compute the Frobenius norm of the covariance
            - cov:   covariance
        """

        if np.ndim(cov) == 2:
            norm = np.linalg.norm(cov)
        elif np.ndim(cov) == 3:
            norm = np.linalg.norm(cov, axis=(1, 2))
        else:
            msg = 'Incorrect size of the matrix'
            self.logger.error(msg)
            raise PPError(msg)
        return norm

    def cov_mean(self, cov):
        """Compute the covariance mean on a period
            - cov:   covariance
        """

        if np.ndim(cov) == 2:
            cov_mean = cov.copy
        elif np.ndim(cov) == 3:
            cov_mean = np.mean(cov, axis=0)
        else:
            msg = 'Incorrect size of the matrix'
            self.logger.error(msg)
            raise PPError(msg)
        return cov_mean

    def cor_from_cov(self, cov):
        """Compute correlation and standard deviation from covariance
            - cov:   covariance
        """

        sz = np.shape(cov)
        flag_time = True

        # Check size of covariance
        if sz[-1] != sz[-2]:
            msg = 'The covariance matrix must be square'
            self.logger.error(msg)
            raise PPError(msg)
        if np.ndim(cov) == 2:
            cor = np.reshape(cov, (1, sz[0], sz[1]))
            sz = np.shape(cor)
            flag_time = False
        else:
            cor = cov.copy()

        # Transform
        sigma = np.zeros((sz[0], sz[1]))
        x = range(sz[1])
        for t in range(sz[0]):
            sigma[t, :] = np.sqrt(np.diag(cor[t, :, :]))
            for i, j in it.product(x, x):
                cor[t, i, j] /= sigma[t, i] * sigma[t, j]

        if flag_time:
            return cor, sigma
        else:
            return cor[0, :, :], sigma[0, :]

    def omb_statistics(self, omb):
        """Calculate the statistics of Observation minus Background:
            mean, rms (of the ensemble mean), spread (std of the ensemble),
            cnt (number of observations for 1 member)
            - omb: omb dictionary
        """

        omb_stat = {}

        # Loop on variables
        for var in omb:
            omb_stat[var] = {}
            var_mean = 0
            var_rms = 0
            var_spread = 0
            var_cnt = 0
            var_mean_t = None
            var_rms_t = None
            var_spread_t = None
            var_cnt_t = None
            var_tline = None
            
            # Loop on instrument
            for instr in omb[var]:
                omb_stat[var][instr] = {}
                instr_mean = 0
                instr_rms = 0
                instr_spread = 0
                instr_cnt = 0
                instr_mean_t = None
                instr_rms_t = None
                instr_spread_t = None
                instr_cnt_t = None
                instr_tline = None

                # Loop on location
                for loc in omb[var][instr]:
                    omb_stat[var][instr][loc] = {}

                    # Stats for the location
                    ens_mean = np.mean(omb[var][instr][loc]['omb'], axis=0)
                    ens_anom = omb[var][instr][loc]['omb'] - ens_mean
                    sh = omb[var][instr][loc]['omb'].shape[1]
                    omb_stat[var][instr][loc]['mean'] = np.mean(ens_mean)
                    omb_stat[var][instr][loc]['rms'] = np.sqrt(np.sum(ens_mean ** 2) / (sh - 1.))
                    omb_stat[var][instr][loc]['spread'] = np.std(ens_anom, ddof=1)
                    omb_stat[var][instr][loc]['cnt'] = sh
                    omb_stat[var][instr][loc]['timeline'] = np.unique(omb[var][instr][loc]['timeline'])
                    omb_stat[var][instr][loc]['mean_t'] = np.zeros(omb_stat[var][instr][loc]['timeline'].size)
                    omb_stat[var][instr][loc]['rms_t'] = np.zeros(omb_stat[var][instr][loc]['timeline'].size)
                    omb_stat[var][instr][loc]['spread_t'] = np.zeros(omb_stat[var][instr][loc]['timeline'].size)
                    omb_stat[var][instr][loc]['cnt_t'] = np.zeros(omb_stat[var][instr][loc]['timeline'].size)
                    for i, t in enumerate(omb_stat[var][instr][loc]['timeline']):
                        ind = np.where(omb[var][instr][loc]['timeline'] == t)[0]
                        omb_stat[var][instr][loc]['mean_t'][i] = np.mean(ens_mean[ind])
                        omb_stat[var][instr][loc]['rms_t'][i] = np.sqrt(np.sum(ens_mean[ind] ** 2) / (ind.size - 1.))
                        omb_stat[var][instr][loc]['spread_t'][i] = np.std(ens_anom[:, ind], ddof=1)
                        omb_stat[var][instr][loc]['cnt_t'][i] = ind.size

                    # Stats for the instrument
                    instr_mean += np.sum(ens_mean)
                    instr_rms += np.sum(ens_mean ** 2)
                    instr_spread += np.sum(ens_anom ** 2)
                    instr_cnt += sh
                    if instr_tline is None:
                        instr_tline = omb_stat[var][instr][loc]['timeline'].copy()
                        instr_mean_t = omb_stat[var][instr][loc]['mean_t'] * omb_stat[var][instr][loc]['cnt_t']
                        instr_rms_t = omb_stat[var][instr][loc]['rms_t'] ** 2 \
                            * (omb_stat[var][instr][loc]['cnt_t'] - 1.)
                        instr_spread_t = omb_stat[var][instr][loc]['spread_t'] ** 2 \
                            * (omb_stat[var][instr][loc]['cnt_t'] - 1.)
                        instr_cnt_t = omb_stat[var][instr][loc]['cnt_t'].copy()
                    else:
                        if instr_tline.all() == omb_stat[var][instr][loc]['timeline'].all():
                            instr_mean_t += omb_stat[var][instr][loc]['mean_t'] * omb_stat[var][instr][loc]['cnt_t']
                            instr_rms_t += omb_stat[var][instr][loc]['rms_t'] ** 2 \
                                * (omb_stat[var][instr][loc]['cnt_t'] - 1.)
                            instr_spread_t += omb_stat[var][instr][loc]['spread_t'] ** 2 \
                                * (omb_stat[var][instr][loc]['cnt_t'] - 1.)
                            instr_cnt_t += omb_stat[var][instr][loc]['cnt_t']
                        else:
                            tmp_tline = np.sort(np.union1d(instr_tline, omb[var][instr][loc]['timeline']))
                            tmp_mean_t = np.zeros(tmp_tline.size)
                            tmp_rms_t = np.zeros(tmp_tline.size)
                            tmp_spread_t = np.zeros(tmp_tline.size)
                            tmp_cnt_t = np.zeros(tmp_tline.size)
                            ind = [np.where(tmp_tline == t)[0][0] for t in instr_tline]
                            tmp_mean_t[ind] = instr_mean_t
                            instr_mean_t = tmp_mean_t
                            tmp_rms_t[ind] = instr_rms_t
                            instr_rms_t = tmp_mean_t
                            tmp_spread_t[ind] = instr_spread_t
                            instr_spread_t = tmp_spread_t
                            tmp_cnt_t[ind] = instr_cnt_t
                            instr_cnt_t = tmp_cnt_t
                            ind = [np.where(tmp_tline == t)[0][0] for t in omb[var][instr][loc]['timeline']]
                            instr_mean_t[ind] += omb_stat[var][instr][loc]['mean_t'] \
                                * omb_stat[var][instr][loc]['cnt_t']
                            instr_rms_t[ind] += omb_stat[var][instr][loc]['rms_t'] ** 2 \
                                * (omb_stat[var][instr][loc]['cnt_t'] - 1.)
                            instr_spread_t[ind] += omb_stat[var][instr][loc]['spread_t'] ** 2 \
                                * (omb_stat[var][instr][loc]['cnt_t'] - 1.)
                            instr_cnt_t[ind] += omb_stat[var][instr][loc]['cnt_t']

                # Stats for the variable
                var_mean += instr_mean
                var_rms += instr_rms
                var_spread += instr_spread
                var_cnt += instr_cnt
                if var_tline is None:
                    var_tline = instr_tline.copy()
                    var_mean_t = instr_mean_t.copy()
                    var_rms_t = instr_rms_t.copy()
                    var_spread_t = instr_spread_t.copy()
                    var_cnt_t = instr_cnt_t.copy()
                else:
                    if var_tline.all() == instr_tline.all():
                        var_mean_t += instr_mean_t
                        var_rms_t += instr_rms_t
                        var_spread_t += instr_spread_t
                        var_cnt_t += instr_cnt_t
                    else:
                        tmp_tline = np.sort(np.union1d(var_tline, instr_tline))
                        tmp_mean_t = np.zeros(tmp_tline.size)
                        tmp_rms_t = np.zeros(tmp_tline.size)
                        tmp_spread_t = np.zeros(tmp_tline.size)
                        tmp_cnt_t = np.zeros(tmp_tline.size)
                        ind = [np.where(tmp_tline == t)[0][0] for t in var_tline]
                        tmp_mean_t[ind] = var_mean_t
                        var_mean_t = tmp_mean_t
                        tmp_rms_t[ind] = var_rms_t
                        var_rms_t = tmp_rms_t
                        tmp_spread_t[ind] = var_spread_t
                        var_spread_t = tmp_spread_t
                        tmp_cnt_t[ind] = var_cnt_t
                        var_cnt_t = tmp_cnt_t
                        ind = [np.where(tmp_tline == t)[0][0] for t in instr_tline]
                        var_mean_t[ind] += instr_mean_t
                        var_rms_t[ind] += instr_rms_t
                        var_spread_t[ind] += instr_spread_t
                        var_cnt_t[ind] += instr_cnt_t

                # Finalise the instrument statistics
                omb_stat[var][instr]['mean'] = instr_mean / instr_cnt
                omb_stat[var][instr]['rms'] = np.sqrt(instr_rms / (instr_cnt - 1.))
                omb_stat[var][instr]['spread'] = np.sqrt(instr_spread / (instr_cnt * self.exp.ens_size - 1.))
                omb_stat[var][instr]['cnt'] = instr_cnt
                omb_stat[var][instr]['timeline'] = instr_tline.copy()
                omb_stat[var][instr]['mean_t'] = instr_mean_t / instr_cnt_t
                omb_stat[var][instr]['rms_t'] = np.sqrt(instr_rms_t / (instr_cnt_t - 1.))
                omb_stat[var][instr]['spread_t'] = np.sqrt(instr_spread_t / (instr_cnt_t * self.exp.ens_size - 1.))
                omb_stat[var][instr]['cnt_t'] = instr_cnt_t.copy()

            # Finalise the variable statistics
            omb_stat[var]['mean'] = var_mean / var_cnt
            omb_stat[var]['rms'] = np.sqrt(var_rms / (var_cnt - 1.))
            omb_stat[var]['spread'] = np.sqrt(var_spread / (var_cnt * self.exp.ens_size - 1.))
            omb_stat[var]['cnt'] = var_cnt
            omb_stat[var]['timeline'] = var_tline.copy()
            omb_stat[var]['mean_t'] = var_mean_t / var_cnt_t
            omb_stat[var]['rms_t'] = np.sqrt(var_rms_t / (var_cnt_t - 1.))
            omb_stat[var]['spread_t'] = np.sqrt(var_spread_t / (var_cnt_t * self.exp.ens_size - 1.))
            omb_stat[var]['cnt_t'] = var_cnt_t.copy()

        # Save global stats in text file
        fname = '{}/data/omb_statistics_global.txt'.format(self.ppdir)
        with open(fname, 'w') as fout:
            fout.write('OmB statistics: mean / rms / spread / obs number \n')
            fout.write('----------------------------------------------\n\n')

            for var in omb_stat:
                fout.write('{}:\n'.format(var))
                if 'mean' in var or 'rms' in var or 'spread' in var or 'cnt' in var or var == 'timeline':
                    continue
                for instr in omb_stat[var]:
                    if 'mean' in instr or 'rms' in instr or 'spread' in instr or 'cnt' in instr or instr == 'timeline':
                        continue
                    instr_name = get_instrument_name(instr)
                    fout.write('   {}:\n'.format(instr_name))
                    for loc in omb_stat[var][instr]:
                        if 'mean' in loc or 'rms' in loc or 'spread' in loc or 'cnt' in loc or loc == 'timeline':
                            continue
                        fout.write('      {}:\n'.format(loc))
                        fout.write('{:+21.3f}'.format(omb_stat[var][instr][loc]['mean']))
                        fout.write('{:12.3f}'.format(omb_stat[var][instr][loc]['rms']))
                        fout.write('{:12.3f}'.format(omb_stat[var][instr][loc]['spread']))
                        fout.write('{:12.0f}\n'.format(omb_stat[var][instr][loc]['cnt']))
                    fout.write('      Total for {}:\n'.format(instr_name))
                    fout.write('{:+21.3f}'.format(omb_stat[var][instr]['mean']))
                    fout.write('{:12.3f}'.format(omb_stat[var][instr]['rms']))
                    fout.write('{:12.3f}'.format(omb_stat[var][instr]['spread']))
                    fout.write('{:12.0f}\n'.format(omb_stat[var][instr]['cnt']))
                fout.write('   Total for {}:\n'.format(var))
                fout.write('{:+18.3f}'.format(omb_stat[var]['mean']))
                fout.write('{:12.3f}'.format(omb_stat[var]['rms']))
                fout.write('{:12.3f}'.format(omb_stat[var]['spread']))
                fout.write('{:12.0f}\n'.format(omb_stat[var]['cnt']))

        # Save all stats in pickle file
        fname = '{}/data/omb_statistics_all.pic'.format(self.ppdir)
        pickle.dump(omb_stat, open(fname, 'wb'))

        return omb_stat

    def obs_rank(self, omb):
        """Calculate the rank diagram of the ensemble
            - omb: omb dictionary
        """

        obs_rank = {'cnt': 0, 'rank': np.zeros(self.exp.ens_size + 1)}

        # Loop on variables
        for var in omb:
            obs_rank[var] = {'cnt': 0, 'rank': np.zeros(self.exp.ens_size + 1)}
            # Loop on instrument:
            for instr in omb[var]:
                obs_rank[var][instr] = {'cnt': 0, 'rank': np.zeros(self.exp.ens_size + 1)}
                # Loop on location
                for loc in omb[var][instr]:
                    obs_rank[var][instr][loc] = {'cnt': 0, 'rank': np.zeros(self.exp.ens_size + 1)}

                    # Rank for this location
                    for obs in omb[var][instr][loc]['omb'].T:
                        obs = np.sort(-obs)
                        if np.all(obs > 0.):
                            obs_rank[var][instr][loc]['rank'][0] += 1
                        elif np.all(obs < 0.):
                            obs_rank[var][instr][loc]['rank'][-1] += 1
                        else:
                            obs_rank[var][instr][loc]['rank'][np.where(obs <= 0.)[0][-1] + 1] += 1
                        obs_rank[var][instr][loc]['cnt'] += 1

                    # Rank for instrument
                    obs_rank[var][instr]['cnt'] += obs_rank[var][instr][loc]['cnt']
                    obs_rank[var][instr]['rank'] += obs_rank[var][instr][loc]['rank']

                # Rank for the variable
                obs_rank[var]['cnt'] += obs_rank[var][instr]['cnt']
                obs_rank[var]['rank'] += obs_rank[var][instr]['rank']

            # Rank total
            obs_rank['cnt'] += obs_rank[var]['cnt']
            obs_rank['rank'] += obs_rank[var]['rank']

        # Save in pickle file
        fname = '{}/data/omb_rank.pic'.format(self.ppdir)
        pickle.dump(obs_rank, open(fname, 'wb'))

        return obs_rank

    # =================================== #
    #              Analyses               #
    # =================================== #

    def construct_observation(self, location, variable, std_var, shift_start=None, length=None,
                              frequency=None, location_name=None, write=True, svgname=None, overwrite=True,
                              instrument='Gauge'):
        """Construct observations from a free run chronicle.
            The observations correspond to the value + gaussian noise N(0,std_var)
            - location:    model-like coordinate (tuple), can be a list of locations
            - variable:    variable to extract, can be a list of variables
            - std_var:     standard deviation of the observation, if more than 1 variable and 1 location,
                           must be a list corresponding to the variables for each location
            - shift_start: shift the start of the post processing in format [x, unit]
            - length:      partial length in format [x, unit]
            - frequency:   frequency of retrieval in format [x, unit], or list of datetime
            - location_name: name of locations when writing file
            - write:       write the observations in ppdir/data
            - svgname:     if write = True, file name without extension
            - overwrite:   if write = True, overwrite the existing file name
            - instrument:  instrument from which the observations are coming
        """

        # Standard deviation
        if not isinstance(std_var, list):
            std_var = [[std_var]]
        elif not isinstance(std_var[0], list):
            std_var = [std_var]

        # Frequency
        if frequency is None:
            frequency = [1, 'hour']

        if 'all' in location:
            # Get cycling information
            _, tline = self.get_cycling_info(shift_start, length, [0, 'hour'], frequency=frequency)
            # Extract the fields
            dates = [self.exp.start0 + timedelta(seconds=t) for t in tline[0]]
            field = self.extract_field(variable, lead_time=[0, 'hour'], date=dates, write=False)
            chron = {}
            for var in field:
                chron[var] = {'all': {}}
                for d, tim in zip(dates, tline[0]):
                    chron[var]['all'][tim] = field[var][d][0]

        else:
            # Extract the chronicles
            chron, tline = self.extract_chronicle(location, variable, lead_time=[0, 'hour'], shift_start=shift_start,
                                                  length=length, frequency=frequency, write=False)
        timeline = tline[0]

        # Add the noise
        chronicle = copy.deepcopy(chron)
        # np.random.seed(0)
        for v, var in enumerate(chron):
            for l, loc in enumerate(chron[var]):
                for tim in chron[var][loc]:
                    shape = chron[var][loc][tim].shape
                    chronicle[var][loc][tim] += np.random.normal(0, std_var[l][v], shape)
                chronicle[var][loc]['sigma'] = std_var[l][v]

        # Location name
        if location_name is None:
            loc_name = [(l, '-') for l in location]
        else:
            loc_name = [(l, ln) for l, ln in zip(location, location_name)]

        # Construct the observation file
        if write:
            if svgname is None:
                fname = '{}/obs/observations'.format(self.ppdir)
            else:
                fname = '{}/obs/{}'.format(self.ppdir, svgname)
            if not overwrite:
                i = 0
                while os.path.exists(fname):
                    i += 1
                svgname_sp = svgname.split('.')
                fname = '{}/obs/{}_{}'.format(self.ppdir, svgname_sp[0], i)

            instr = instance_obs(instrument, {}, self.exp.model.parameter)
            instr.write_observations(fname, chronicle, self.exp.start0, timeline, loc_name)

    def field_statistics(self, reference, variable, lead_time=None, shift_start=None, length=None,
                         shift_base=None, write=True, svgname=None, overwrite=True):
        """Calculate the statistics for a variable
            - reference:   postprocessing instance for a free or dry run
            - variable:    variable to extract, can be a list of variables
            - lead_time:   lead time to extract, in format [x, unit], must be a list for forecast lead times,
                           default is [0, 'hour'],
            - shift_start: shift the start of the post processing in format [x, unit]
            - length:      partial length in format [x, unit]
            - shift_base:  shift the base time in the reanalysis window: time = base time - shift,
                           taken into account only if lead_time = [0, 'hour']
            - write:       write the extraction in ppdir/data
            - svgname:     if write = True, file name without extension, can be a list, 1 name per variable
            - overwrite:   if write = True, overwrite the existing file name
        """

        # Lead time
        if lead_time is None:
            lead_time = [0, 'hour']
        lds = format2sec(lead_time)

        # Get cycling information
        cycles, timeline = self.get_cycling_info(shift_start, length, lead_time, shift_base)
        timeline = [t[0] for t in timeline]
     
        # Initialisation
        if isinstance(variable, list):
            nbvar = len(variable)
        else:
            nbvar = 1
            variable = [variable]
        mean = [0.] * nbvar
        rms = [0.] * nbvar
        spread = [0.] * nbvar
        mean_sp = [np.empty(0, dtype=np.float32)] * nbvar
        rms_sp = [np.empty(0, dtype=np.float32)] * nbvar
        spread_sp = [np.empty(0, dtype=np.float32)] * nbvar
        mean_t = [np.empty(0, dtype=np.float32)] * nbvar
        rms_t = [np.empty(0, dtype=np.float32)] * nbvar
        spread_t = [np.empty(0, dtype=np.float32)] * nbvar

        # Loop on date
        for c, t in zip(cycles, timeline):
            date = self.exp.start0 + timedelta(seconds=int(t))
            # Reference extraction
            ref = reference.extract_field(variable, lead_time=lead_time, date=date, shift_base=shift_base, write=False)
            # Self extraction
            field = self.extract_field(variable, lead_time=lead_time, date=date, shift_base=shift_base, write=False)
            # Statistics
            for v, var in enumerate(variable):
                ens_mean = np.mean(field[var][date][lds] - ref[var][date][lds][0, :], axis=0)
                ens_anom = field[var][date][lds] - ref[var][date][lds][0, :] - ens_mean
                try:
                    mean_sp[v] += ens_mean
                    rms_sp[v] += ens_mean ** 2
                    spread_sp[v] += ens_anom ** 2
                except ValueError:
                    mean_sp[v] = ens_mean
                    rms_sp[v] = ens_mean ** 2
                    spread_sp[v] = ens_anom ** 2
                mean_t[v] = np.append(mean_t[v], np.mean(ens_mean))
                rms_t[v] = np.append(rms_t[v], np.sqrt(np.sum(ens_mean ** 2) / (ens_mean.size - 1.)))
                spread_t[v] = np.append(spread_t[v], np.std(ens_anom))

        # Finalise statistics
        stats = {}
        if len(cycles) == 1:
            dnm = 1
        else:
            dnm = len(cycles) - 1
        for v, var in enumerate(variable):
            mean[v] = np.mean(mean_sp[v]) / (1. * len(cycles))
            rms[v] = np.sqrt(np.sum(rms_sp[v]) / (len(cycles) * rms_sp[v].size - 1.))
            spread[v] = np.sqrt(np.sum(spread_sp[v]) / (len(cycles) * spread_sp[v].size - 1.))
            mean_sp[v] /= (1. * len(cycles))
            rms_sp[v] = np.sqrt(rms_sp[v] / dnm)
            spread_sp[v] = np.sqrt(spread_sp[v] / dnm)
            stats[var] = {'mean': mean[v], 'rms': rms[v], 'spread': spread[v],
                          'mean_sp': mean_sp[v], 'rms_sp': rms_sp[v], 'spread_sp': spread_sp[v],
                          'mean_t': mean_t[v], 'rms_t': rms_t[v], 'spread_t': spread_t[v], 'timeline': timeline}

        # Write the statistics
        if write:

            # File names
            if svgname is None:
                fnames = ['{}/data/field_statistics_{}.pic'.format(self.ppdir, var) for var in variable]
            elif isinstance(svgname, list):
                fnames = ['{}/data/{}.pic'.format(self.ppdir, fn) for fn in svgname]
            else:
                fnames = '{}/data/{}.pic'.format(self.ppdir, svgname)

            # Dump
            if isinstance(fnames, list):
                for fn, var in zip(fnames, variable):
                    if not overwrite:
                        fnsvg = fn[:-4]
                        i = 0
                        while os.path.exists(fn):
                            i += 1
                            fn = '{}_{}.pic'.format(fnsvg, i)
                    gherkins = [[reference.name, variable, lead_time, shift_start, length, shift_base], stats[var]]
                    pickle.dump(gherkins, open(fn, 'wb'))
            else:
                if not overwrite:
                    fnsvg = fnames[:-4]
                    i = 0
                    while os.path.exists(fnames):
                        i += 1
                        fnames = '{}_{}.pic'.format(fnsvg, i)
                gherkins = [[reference.name, variable, lead_time, shift_start, length, shift_base], stats]
                pickle.dump(gherkins, open(fnames, 'wb'))

        return stats

