"""
Model
========

Mother class model

"""

import logging
import os
import shutil
import yaml
import numpy as np
from datetime import datetime, timedelta
from ..common.matrix import Matrix
from ..common.errors import ModelError

# ======================================================


class Model(object):

    logger = logging.getLogger('Model')
    logging.Logger.setLevel(logger, logging.INFO)

    # Control vector
    @property 
    def control(self):
        return self._control
    
    @control.setter 
    def control(self, value):
        """
        Dictionary describing the variables to control and their location
        Initialised by Model, updated by Assim.
        It defines the control vector length and the index of each control variables
        e.g. self.control = {'Ks': [1,2,3], 'h': 'all'}
             self.ctl_length = 466  for a mesh of 463 points
             self.first_node = [0, 1, 2, 3, 466]
        """
        if value == {}:
            self._control = None
            self.ctl_length = 0
            self.first_node = []
        else:
            self._control = value
            dim = 1
            for d in self.shape:
                dim *= d
            self.ctl_length = dim * len(value)
            self.first_node = range(0, self.ctl_length+1, dim)

    # =================================== #
    #               Methods               #
    # =================================== #

    def __init__(self, config, prm, statdir='.', wdir='Work', archdir='Archive', member=0,
                 start=None, start0=None, postproc=False):
        """Constructor
            config:       path and name of the file containing the configuration
            prm:          path and name of the file containing the parameters
            statdir:      path to the required files as enumerated in the item ['files'] of the configuration file
                          if None, files are expected to be in the launch directory
            wdir:         working directory
            archdir:      archiving directory
            member:       member id
            member:       member id: 0 if no ensemble,
                                     from 1 to Ne if there is an ensemble
            start:        datetime start to carry on the experiment
            start0:       datetime original start of the experiment
            postproc:     instanciation for post-processing purposes
        """
        # Public attributes, initialisation
        self.name = ''                  # Name of the model
        self.member = member            # Member id
        self.outdir = wdir              # Output files directory
        self.figdir = wdir              # Output figures directory
        self.datestart = datetime(2018, 4, 16)  # Starting date (datetime)
        if start is None or start0 is None:
            self.start = 0.             # Starting time (relative) in seconds (int)
        else:
            self.start = (start - start0).days * 86400 + (start - start0).seconds
        self.length = 0                 # Length of the run in seconds (int or float)
        self.step = 0.                  # Time step of the model (float)
        self.control = {}               # Control variables (dictionary) cf. decorator
        #                                 -> self.ctl_length = 0    Length of control vector
        #                                 -> self.first_node = []   Index of each control variable
        
        # Model-like attributes, initialisation   
        self.postproc = postproc        # Instanciation for post-processing purposes
        self.conf = None                # Configuration
        self.parameter = None           # Parameters
        self.files = {}                 # Dictionary of required files
        self.statdir = statdir          # Required files (restart, geometry, ...) directory
        self.wdir = wdir                # Working directory
        self.archdir = archdir          # Archiving directory
        if self.postproc:               # Path and name of the configuration and parameter files
            self.config = '{}/init/{}'.format(self.archdir, config.split('/')[-1])
            self.prm = '{}/init/{}'.format(self.archdir, prm.split('/')[-1])
        else:
            self.config = config
            self.prm = prm
        self.shape = (0,)               # Dimensions of the model (tuple)
        self.state_change = {}          # Dictionary of changes for next run
        self.interpol = {}              # Dictionary of spatial interpolation
        self.datestop = self.datestart  # Ending date (datetime)
        self.stop = 0.                  # Ending time (relative) in seconds (int or float)
        self.saved_time = {}            # Dictionary used in self.save_time() and self.restore_time()
        #                                {'date': datetime, 'start': int, 'length': int}
        self.keep_gps = []                # Variables to correct for the GP sampler
        #                                           Updated by the assimilation

        # Read the configuration file
        self.read_config()
        if not self.postproc:
            # Copy the configuration file in the archiving directory
            shutil.copyfile(self.config, os.path.join('{}/init'.format(self.archdir),
                                                      self.config.split('/')[-1]))                            
            # Copy the configuration file in the working directory 
            shutil.copyfile(self.config, os.path.join(self.wdir, self.config.split('/')[-1]))

        # Read the parameter file
        self.read_prm()
        if not self.postproc:
            # Copy the configuration file in the archiving directory
            shutil.copyfile(self.prm, os.path.join('{}/init'.format(self.archdir),
                                                   self.prm.split('/')[-1]))
            # Copy the configuration file in the working directory
            shutil.copyfile(self.config, os.path.join(self.wdir, self.config.split('/')[-1]))
        # Instance
        self.model = None               # Instance 

    def read_config(self):
        """Read the configuration file. By default a yaml file is expected"""
        
        with open(self.config, 'r') as fin:
            try:
                # yml file
                self.conf = yaml.safe_load(fin)
            except IOError as err:
                msg = 'The configuration file cannot be read:\n{}'.format(err)
                self.logger.error(msg)
                raise ModelError(msg)

            try:
                self.files = self.conf['files']
            except KeyError:
                pass

    def read_prm(self):
        """Read the parameter file."""

        with open(self.prm, 'r') as fin:
            try:
                # yml file
                self.parameter = yaml.safe_load(fin)
            except IOError as err:
                msg = 'The parameter file cannot be read:\n{}'.format(err)
                self.logger.error(msg)
                raise ModelError(msg)
            else:
                if self.parameter['composite'] is None:
                    self.parameter['composite'] = []
                if self.parameter['store_anl'] is None:
                    self.parameter['store_anl'] = []
                if self.parameter['balance_var'] is None:
                    self.parameter['balance_var'] = []


    def set_time(self, dateref, length, start):
        """Define time of the run
            - dateref: datetime of the start
            - length:  length of the run in seconds
            - start:   initial time
        """
        
        self.datestart = dateref
        self.length = length
        self.datestop = dateref + timedelta(seconds=length)
        self.start = start
        self.stop = start + length

    def copy(self, members=None):
        """Create new model instances with the same characteristics
            - members: list of member id
        """

        msg = 'The Model method copy is not implemented'
        raise NotImplementedError(msg)

    def get_gps_axis(self):
        """Return a dictionary with the axis for the GP sampler perturbations"""

        return {}
    
    def __call__(self, dateref=None, length=None, dumptime=None,
                 file=None, overlap=None):
        """Run the model
            - dateref:  datetime of the start
            - length:   length of the run in seconds
            - dumptime: list of time to output
            - file:     specific file name for logging
            - overlap:  time to output for overlapping windows
         """

        msg = 'The Model method __call__ is not implemented'
        raise NotImplementedError(msg)
        
    def convert_coord(self, coord, model_coord):
        """Convert observation coordinates into coordinates understandable by the model
           Define the interpolation parameters
            - coord:  dictionary { 'spatial': {coord_type1: [], coord_type2: []},
                                   'time': [datetime] }
                       eg. {'spatial': {('lat','lon'): [(45.,200.)],
                                        ('s',): [36500., 45000.]},
                            'time': [datetime(2018,4,16,0,0,0]}
            - model_coord: dictionary {'spatial': {},
                                       'time': [1800.]}
        """

        msg = 'The Model method convert_coord is not implemented'
        raise NotImplementedError(msg)
    
    def get_coord_limits(self):
        """Return the limits of the domain"""

        limits = []
        return limits

    def get_Mxb_Hxb(self, datestart, length, file, dumptime, xb_start, obsinfo, pickle=False):
        """Return the background state of the control variables
            at the different time following dumptime and its
            counterpart in observation space
            - datestart:   datetime of the start of the run
            - length:      length of the run
            - file:        logging results in a specific file
            - dumptime:    list of time to dump
            - xb_start:    get xb at the start (end) of the run (bool)
            - obsinfo:     dictionary of observation information
            - pickle:      save and return state at the end of the length
        """

        msg = 'The Model method get_Mxb_Hxb is not implemented'
        raise NotImplementedError(msg)

    def control_vector(self):
        """Construct the control vector"""

        msg = 'The Model method __call__ is not implemented'
        raise NotImplementedError(msg)

    def apply_Hnolin(self, coords, ist, iend):
        """Return the vector in observation space
            (Possibly) non-linear version of H
            - coords:      dictionary of coordinates after self.convert_coord()
            - ist:         first index to take into account
            - iend:        last index to take into account
        """

        msg = 'The Model method __call__ is not implemented'
        raise NotImplementedError(msg)

    def get_H(self, coords, ist, iend, xb=None, Hxb=None):
        """Return the (tangent) linear matrix H
            - coords:      dictionary of coordinates after self.convert_coord()
            - ist:         first index to take into account
            - iend:        last index to take into account
            - xb:          Vector of ensemble of xb anomalies in model space
            - Hxb:         Vector of ensemble of anomalies in observation space
                           It is assumed that both xb and Hxb have as many
                           members as parameters and CL in control vector
        """

        H = np.zeros((iend-ist, self.ctl_length))
        return Matrix(H)

    def check_increment(self, bkg, increment):
        """Check the correctness of the increment
            - bkg:       background state
            - increment: increment to be added to the background state
        """
        
        return increment

    def check_range(self, var, therange, index=None):
        """Check if a range of values is consistent for a variable
            - var:       name of variable
            - therange:     range to check [min,max]
            - index:     index of the variable for BC
        """
        
        return therange
    
    def set_changes(self, bkg=None, increment=None, state=None, values=None, extra=None):
        """Set the changes to take into account for the next run
            - bkg:       background state
            - increment: increment to be added to the background state
            - state:     list of dictionary of changes
            - values:    list of values for changes
            - extra:     list of extra values for changes
        """

        msg = 'The Model method set_changes is not implemented'
        raise NotImplementedError(msg)
        
    def update_gps(self, extra):
        """Update the GP sampler perturbation reference
            - extra:  increment to add
        """

        pass

    def prepare_next_run(self, directory=True, save_state=False, restartdir=None,  
                         restore_state=False, dump_state=False, state=False,  
                         persist=False, time=True, shift=0, init_now=False):
        """Prepare next run
            - directory:   prepare directories
            - save_state:  save current state
            - restartdir:  directory containing the restart file
            - restore_state: restore state saved previously
            - dump_state:  dump state saved previously
            - state:       initialise from a particular state
            - persist:     persist boundary conditions for forecast
            - time:        set time of the run
            - shift:       shift of the time in seconds
            - init_now:    initialise the changes now
        """

        msg = 'The Model method prepare_next_run is not implemented'
        raise NotImplementedError(msg)

    def move_outputs(self, paths):
        """Move outputs into archiving directory
           - paths: dictionary with the paths for archiving
        """

        msg = 'The Model method move_outputs is not implemented'
        raise NotImplementedError(msg)

    def dump_restart(self, restartdir):
        """Dump restart files
            - restartdir:  directory containing the restart files
        """

        pass

    def dump_assim_restart(self, restartdir):
        """Dump restart information for assimilation
            - restartdir:  directory containing the restart files
        """

        pass

    def pickle(self, time_only=False, overlap=False):
        """Pickle for parallelisation
            - time_only: pickle the time only
            - overlap:   True for pickling state for sliding window
        """

        return [self.datestart, self.length, self.start]

    def unpickle(self, gherkins, time_only=False, overlap=False):
        """Unpickle for parallelisation
            - gherkins:  Saved information
            - time_only: Unpickle the time only
            - overlap:   True for pickling state for sliding window
        """

        self.set_time(gherkins[0], gherkins[1], gherkins[2])

    def reconstruct_output_file(self, filelist):
        """ Reconstruct output files by keeping the last state for each time step
            - filelist:    list of files for the reconstruction
        """
        
        pass
    
    def extract_info(self, location, variable, datedir, times, size_ensemble, fname=None):
        """Find the indices for output file extraction
            - location:       list of model-like coordinates (tuple),
                              or 'all' for all locations. If tuple, take the closest location.
            - variable:       list of variables to extract
            - datedir:        cycling directory
            - times:          list of time to extract in seconds. Take the closest time.
            - size_ensemble:  size of the ensemble
            - fname:          name of file, default given by the instance configuration
        """

        pass

    def extract_from_file(self, location, variable, datedir, times, size_ensemble):
        """Extract a variable at a particular location for post processing
            - location:       list of model-like coordinates (tuple),
                              or 'all' for all locations
            - variable:       list of variables to extract
            - datedir:        cycling directory
            - times:          list of time to extract in seconds
            - size_ensemble:  size of the ensemble
        """

        msg = 'The Model method extract_from_file is not implemented'
        raise NotImplementedError(msg)

    def __repr__(self):
        """Information"""
        
        string = 'Model \n'
        string += '   configuration       : {}\n'.format(self.config)
        string += '   static directory    : {}\n'.format(self.statdir)
        string += '   working directory   : {}\n'.format(self.wdir)
        string += '   archiving directory : {}\n'.format(self.archdir)
        return string
