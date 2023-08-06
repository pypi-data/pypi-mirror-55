"""
Experiment
==========

Possible experiments:
    - Free Run: run from start to stop without assimilation
    - Dry Run: run with reanalyses and forecasts but without data assimilation
    - Assim Run: run with reanalyses and forecasts with data assimilation

Possible models:
    - Mascaret

Possible assimilation scheme:
    - EKF: extended Kalman Filter
"""

import logging
import os
import sys
import shutil
import yaml
import ctypes
from pathos.multiprocessing import ProcessPool
from datetime import datetime, timedelta
from ..models.instanciate import instanciate as instance_model
from ..assim.instanciate import instanciate as instance_assim
from ..common.functions import sec2unit, format2sec
from ..common.errors import ExperimentError

# List of possibilities
available_exps = ['Free Run', 'Dry Run', 'Assim Run']
available_assims = ['EnKF']

# List of model instances
ens_model = []

# Log file
logpath = os.getcwd()                                      # Path of the logfile: directory from where it is launched
logname = 'smurf'                                          # basic name of the logfile without extension
logfile = '{}/{}.log'.format(logpath, logname)             # Whole logfile name
i0 = 1
while os.path.exists(logfile):
    logfile = '{}/{}_{}.log'.format(logpath, logname, i0)
    i0 += 1

# ======================================================


class Experiment(object):

    # logging.basicConfig(filename=logfile)
    logging.basicConfig(stream=sys.stdout)
    logger = logging.getLogger('Experiment')
    logging.Logger.setLevel(logger, logging.INFO)

    # Configuration for the run
    @property
    def conf_exp(self):
        return self._conf_exp
    
    @conf_exp.setter 
    def conf_exp(self, dico):
        try:
            self._conf_exp = dico['experiment']
            # Basic settings
            self.name = self._conf_exp['name']
            self.exp_type = self._conf_exp['type']
            if self.exp_type not in available_exps:
                msg = 'Unknown experiment type {}.'.format(self.exp_type)
                self.logger.error(msg)
                raise ExperimentError(msg)
            self.model_type = self._conf_exp['model']
            if self.exp_type == 'Assim Run':
                self.assim = []
                self.assim_nbsteps = self._conf_exp['assimsteps']
                if self.assim_nbsteps == 0:
                    msg = 'At least 1 step must be defined.'
                    self.logger.error(msg)
                    raise ExperimentError(msg)
                try:
                    self.ens_size = self._conf_exp['ens_size']
                except (KeyError, TypeError):
                    self.ens_size = 1
                if self.ens_size > 1:
                    try:
                        self.parallel = self._conf_exp['parallel']
                    except (KeyError, TypeError):
                        self.parallel = False
                    if self.parallel:
                        try:
                            self.nbproc = self._conf_exp['nbproc']
                        except (KeyError, TypeError):
                            self.nbproc = 0
                    else:
                        self.nbproc = 0
                else:
                    self.parallel = False
                    self.nbproc = 0
            else:
                self.assim = None
                self.ens_size = 1
                self.parallel = False
                self.nbproc = 0
        except (KeyError, TypeError) as err:
            msg = 'Experiment information incomplete:\n{}'.format(err)
            self.logger.error(msg)
            raise ExperimentError(msg)

    # Configuration for the model
    @property
    def conf_model(self):
        return self._conf_model
    
    @conf_model.setter 
    def conf_model(self, dico):
        try: 
            self._conf_model = dico['model']['config']
            if self._conf_model[0] != '/':
                self._conf_model = '{}/{}'.format(os.getcwd(), self._conf_model)
            self.prm_model = dico['model']['parameter']
            if self.prm_model[0] != '/':
                self.prm_model = '{}/{}'.format(os.getcwd(), self.prm_model)
        except (KeyError, TypeError) as err:
            msg = 'Model information incomplete:\n{}'.format(err)
            self.logger.error(msg)
            raise ExperimentError(msg)

    # Configuration for the assimilation
    @property
    def conf_assim(self):
        return self._conf_assim
    
    @conf_assim.setter 
    def conf_assim(self, dico):
        if self.exp_type != 'Assim Run':
            self._conf_assim = None
        else:
            self._conf_assim = {}
            for i in range(1, self.assim_nbsteps+1):
                key = 'step{}'.format(i)
                try:
                    self._conf_assim[i] = dico['assim'][key]
                    if dico['assim'][key]['scheme'] not in available_assims:
                        msg = 'Unknown assimilation type {}.'.format(dico['assim'][key]['scheme'])
                        self.logger.error(msg)
                        raise ExperimentError(msg)
                    if dico['assim'][key]['config'][0] != '/':
                        self._conf_assim[i]['config'] = '{}/{}'.format(os.getcwd(), dico['assim'][key]['config'])
                    if dico['assim'][key]['scheme'] == 'KF':
                        self.ens_size = 1
                except (KeyError, TypeError) as err:
                    msg = 'Assimilation information incomplete for step {}:\n{}'.format(i, err)
                    self.logger.error(msg)
                    raise ExperimentError(msg)

    # Working directory
    @property
    def wdir(self):
        return self._wdir
    
    @wdir.setter 
    def wdir(self, directory):
        if directory[0] != '/':
            directory = '{}/{}'.format(os.getcwd(), directory)
        self._wdir = directory
        if not self.postproc:
            try:
                if os.path.exists(directory):
                    shutil.rmtree(directory)
                os.makedirs(directory)
            except IOError as err:
                msg = 'Cannot create working directory:\n{}'.format(err)
                self.logger.error(msg)
                raise ExperimentError(msg)

    # Archiving directory
    @property
    def archdir(self):
        return self._archdir
    
    @archdir.setter 
    def archdir(self, directory):
        if directory[0] != '/':
            directory = '{}/{}'.format(os.getcwd(), directory)
        self._archdir = directory
        if not self.postproc:
            try:
                if os.path.exists(directory):
                    self.logger.warning('Archiving directory exists. Data will be overwritten')
                    listdir = os.listdir(directory)
                    for d in listdir:
                        if os.path.isdir('{}/{}'.format(directory, d)):
                            if d[:8].isdigit():
                                if datetime.strptime(d, "%Y%m%d-%H%M") >= self.start0:
                                    shutil.rmtree('{}/{}'.format(directory, d))
                            elif d == 'init' or d == 'diags':
                                shutil.rmtree('{}/{}'.format(directory, d))
                            elif d == 'restart':
                                listfile = os.listdir('{}/restart'.format(directory))
                                for file in listfile:
                                    dd = file.split('_')[0]
                                    if datetime.strptime(dd, "%Y%m%d-%H%M") > self.start0:
                                        os.remove('{}/restart/{}'.format(directory, file))
                        elif os.path.isfile(d):
                            os.remove('{}/{}'.format(directory, d))
                os.makedirs('{}/init'.format(directory))
                os.makedirs('{}/diags'.format(directory))
                if not os.path.exists('{}/restart'.format(directory)):
                    os.makedirs('{}/restart'.format(directory))
            except IOError as err:
                msg = 'Cannot create archiving directory:\n{}'.format(err)
                self.logger.error(msg)
                raise ExperimentError(msg)

    # Static directory
    @property
    def statdir(self):
        return self._statdir
    
    @statdir.setter 
    def statdir(self, directory):
        if directory[0] != '/':
            directory = '{}/{}'.format(os.getcwd(), directory)
        self._statdir = directory
        if not self.postproc and not os.path.exists(directory):
            msg = 'Static directory does not exists\n{}'.format(directory)
            self.logger.error(msg)
            raise ExperimentError(msg)

    # Start time
    @property
    def start0(self):
        return self._start0
    
    @start0.setter
    def start0(self, value):
        try:
            self._start0 = datetime.strptime(value, "%d/%m/%Y %H:%M")
        except ValueError:
            msg = 'The start time must have the format as dd/mm/yyyy hh:mm'
            self.logger.error(msg)
            raise ExperimentError(msg)
        
    # Length of the experiment
    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, value):
        try:
            self._length = format2sec(value)
        except ValueError or self._length <= 0:
            msg = 'Incorrect length time {}.'.format(value)
            self.logger.error(msg)
            raise ExperimentError(msg)

    # Spinup of the experiment
    @property
    def spinup(self):
        return self._spinup
    
    @spinup.setter
    def spinup(self, value):
        try:
            self._spinup = format2sec(value)
        except ValueError or self._spinup < 0:
            self.logger.warning('Experiment spinup set to 0')
            self._spinup = 0

    # Length of the reanalysis step
    @property
    def reanalysis(self):
        return self._reanalysis
    
    @reanalysis.setter
    def reanalysis(self, value):
        try:
            self._reanalysis = format2sec(value)
        except ValueError or self._reanalysis == 0:
            msg = 'Incorrect reanalysis time {}\n'.format(value)
            self.logger.error(msg)
            raise ExperimentError(msg)

    # Length of the forecast step
    @property
    def forecast(self):
        return self._forecast
    
    @forecast.setter
    def forecast(self, value):
        try:
            self._forecast = format2sec(value)
        except ValueError or self._forecast < 0:
            self.logger.warning('Forecast time set to 0')
            self._forecast = 0

    # Sliding window
    @property
    def overlap(self):
        return self._overlap
    
    @overlap.setter
    def overlap(self, value):
        try:
            self._overlap = format2sec(value)
        except ValueError:
            self.logger.warning('Sliding window set to 0')
            self._overlap = 0
        else:
            if self._overlap > 0:
                self._overlap = self.reanalysis - self._overlap

    # Frequency for dumping restart files
    @property
    def restart(self):
        return self._restart
    
    @restart.setter
    def restart(self, value):
        try:
            self._restart = format2sec(value)
        except ValueError or self._restart < self.reanalysis:
            self.logger.warning('Reset restart dumping frequency to reanalysis window')
            self._restart = self.reanalysis

    # =================================== #
    #               Methods               #
    # =================================== #

    def __init__(self, configrun=None, archivepath=None):
        """Constructor
            - configrun:    path and name of the yml configuration file
                            for running an experiment. If None, post processing
            - archivepath:  path to the archived experiment
                            for post-processing purposes
        """

        global ens_model

        if configrun is None:
            # Instanciate for postprocessing
            self.postproc = True                                   # Instanciation for off-line post processing
            self.conf_path = '{}/init/configrun.yml'.format(archivepath)  # Configuration file
        else:
            # Instanciate for running experiment
            self.postproc = False
            self.conf_path = configrun
        
        # Read the config.yml file
        with open(self.conf_path, 'r') as fin:
            data = yaml.safe_load(fin)

        # Set configurations
        self.conf_exp = data                                       # Experiment configuration
        self.conf_model = data                                     # Model configuration
        self.conf_assim = data                                     # Assimilation configuration

        # Handle times
        self.start0 = self.conf_exp['time']['start']               # Start of the experiment before spinup
        self.start = self.start0                                   # Start of the experiment after spinup
        self.length = self.conf_exp['time']['length']              # Length of the experiment without spinup (sec)
        self.spinup = self.conf_exp['time']['spinup']              # Length of spinup (sec)
        self.start += timedelta(seconds=self.spinup)
        if self.exp_type == 'Dry Run' or self.exp_type == 'Assim Run':
            self.reanalysis = self.conf_exp['time']['reanalysis']  # Length of a reanalysis window (sec)
            self.forecast = self.conf_exp['time']['forecast']      # Length of a forecast (sec)
            self.overlap = self.conf_exp['time']['sliding_window']  # Overlapping time between windows (sec)
        else:
            self.reanalysis = self.length
            self.forecast = 0
            self.overlap = 0
        self.stop = self.start + timedelta(seconds=self.length)    # Stop of the experiment cycling
        
        # Restart dumping frequency
        self.restart = self.conf_exp['restart']                    # Frequency of dumping restart files

        # Carry on previous experiment
        try:
            self.carry_on = self.conf_exp['time']['carry_on']      # Carry on the experiment ?
        except (KeyError, TypeError):
            self.carry_on = False
        else:
            if self.postproc:
                self.carry_on = False
        self.start_origin = self.start0                            # Original starting time of the experiment
        if self.carry_on:
            # Check available restart files
            restdir = '{}/{}/restart'.format(self.conf_exp['directory']['archive'], self.name)
            restdate = datetime.strptime(list(sorted(set([d.split('_')[0] for d in os.listdir(restdir)])))[-1],
                                         '%Y%m%d-%H%M')
            if restdate > self.start:
                # Take into account the restart file available
                self.spinup = [0, 'hour']
                self.start0 = restdate.strftime('%d/%m/%Y %H:%M')
                self.start = restdate

        # Check and create the directories
        if not self.postproc:
            self.logger.info('Check and create directories for the experiment.')
        self.wdir = self.conf_exp['directory']['work']             # Working directory
        self.archdir = '{}/{}'.format(self.conf_exp['directory']['archive'],  # Archiving directory
                                      self.name)
        self.statdir = self.conf_exp['directory']['static']        # Static directory
        self.arch_paths = {'spinup': {},                           # Archiving paths
                           'reanalysis': {},
                           'forecast': {},
                           'restart': '{}/restart'.format(self.archdir)}

        # Copy the parameters of the experiment
        if not self.postproc:
            shutil.copyfile(self.conf_path, '{}/init/configrun.yml'.format(self.archdir))
            # Move to working directory
            os.chdir(self.wdir)
        
        # Starting dates
        if self.carry_on:
            start = self.start
            start0 = self.start_origin
        else:
            start = None
            start0 = None
        if self.ens_size > 1 or self.postproc:
            member = 1
        else:
            member = 0

        # Create the model instance
        self.logger.info('Create the model instance.')
        model = instance_model(self.model_type, self.conf_model, self.prm_model, self.statdir,
                               self.wdir, self.archdir, member, start, start0, self.postproc)
        self.model = id(model)                                    # Model instance

        ens_model = [model]
        self.ens_model = [self.model]                             # List of model instances
        for _ in range(1, self.ens_size):
            ens_model.append(model)
            self.ens_model.append(self.model)

        if self.postproc:
            self.model = model    # No parallelism in postprocessing

        # Create the assimilation instances
        if self.exp_type == 'Assim Run':
            self.assim = [0]                                      # List of assimilation instances
            for i in range(1, self.assim_nbsteps+1):
                self.logger.info('Create the assimilation instance for step {}.'.format(i))
                self.assim.append(instance_assim(self.conf_assim[i]['scheme'], self.conf_assim[i]['config'],
                                                 self.ens_model, self.reanalysis, self.overlap, self.wdir,
                                                 self.archdir, i, self.assim_nbsteps, self.parallel,
                                                 self.nbproc, self.postproc))

    def __call__(self):
        """Run the experiment
           Post process the run
           Move the outputs in the archiving directory
           Prepare restart files
        """
                
        global ens_model

        self.logger.info('Starting experiment.')
        self.logger.info('\n{}'.format(self.__repr__()))
        
        # ---------------------------------
        #  Running the spinup if required
        # ---------------------------------
        if self.spinup > 0:
            self.logger.info('Running the spinup.')
            self.run_base(spinup=True)
            self.dump_restart()

        # Instanciate ensemble if required
        if self.ens_size > 1:
            self.logger.info('Instanciate {} other models for the ensemble.'.format(self.ens_size-1))
            model = ctypes.cast(self.model, ctypes.py_object).value
            ens_model[1:] = model.copy(range(2, self.ens_size+1))
            self.ens_model[1:] = [id(m) for m in ens_model[1:]]
            for i in range(1, self.assim_nbsteps+1):
                self.assim[i].ens_model = self.ens_model
            # Sample perturbations
            if not self.carry_on:
                for i in range(1, self.assim_nbsteps+1):
                    self.assim[i].apply_perturbation()

        # Take into account the previous analysis if carrying on the experiment
        if self.carry_on:
            for assim in self.assim[1:]:
                assim.carry_on(self.arch_paths['restart'], self.start)

        # ---------------------------
        #  Running the experiment
        # ---------------------------
        self.logger.info('Running a {} experiment.'.format(self.exp_type))
        # Restart dumping
        rstart = self.start
        
        # Cycling the run
        while self.start + timedelta(seconds=self.reanalysis) <= self.stop:                
        
            # Flag for dumping restart files
            rlength = self.start - rstart
            if rlength.days*86400 + rlength.seconds >= self.restart:
                self.dump_restart()
                rstart = self.start
            
            if self.assim is not None:
                # Assimilation step
                # ------------------
                # Loop on assimilation steps
                for i in range(1, self.assim_nbsteps+1):
                    self.logger.info('Calculating analysis for step {}.'.format(self.assim[i].step))
                    # Save the current time
                    if i < self.assim_nbsteps:
                        self.save_time('save')
                    # Run the assimilation
                    self.run_base(assim=i)
                    # Restore the time
                    if i < self.assim_nbsteps:
                        self.save_time('restore')
            
            else:
                # Reanalysis step
                # ------------------
                self.logger.info('Running reanalysis from {}.'.format(self.start.strftime('%d/%m/%Y %H:%M')))
                self.run_base()
                
            # Moving starting time
            self.start += timedelta(seconds=self.reanalysis) 
            if self.forecast == 0:
                self.start -= timedelta(seconds=self.overlap)
            
            # Forecast step
            # ----------------
            if self.forecast > 0:
                self.logger.info('Running forecast from {}.'.format(self.start.strftime('%d/%m/%Y %H:%M')))
                self.run_base(forecast=True) 
                if self.overlap != 0:
                    self.start -= timedelta(seconds=self.overlap)  
                        
        # Dump final restart
        self.dump_restart()

        # Reinitialise starting time
        self.start = self.stop - timedelta(seconds=self.length)            
                                
        self.logger.info('-------------------------------------')
        self.logger.info('Experiment finished running correctly')
        self.logger.info('-------------------------------------')

    def run_base(self, spinup=False, forecast=False, assim=0):
        """Basic sequence of a run
            - spinup:   Running a spinup?
            - forecast: Running a forecast?
            - assim:    Running assim? Which step?
        """

        # Preparing archive
        if not forecast:
            self.prepare_archive(spinup)
        
        # Running
        if spinup:
            model = ctypes.cast(self.model, ctypes.py_object).value
            model(dateref=self.start0, length=self.spinup)
        elif forecast:
            length = self.forecast
            if self.parallel:
                arg = [[i, length] for i in self.ens_model]
                pool = ProcessPool(self.nbproc)
                res = pool.map(self.forecast_parallel, arg)
                pool.clear()
                # Reinitialise model
                for m, modid in enumerate(self.ens_model):
                    model = ctypes.cast(modid, ctypes.py_object).value
                    model.unpickle(res[m])
            else:
                for modid in self.ens_model:
                    model = ctypes.cast(modid, ctypes.py_object).value
                    model(dateref=self.start, length=length)
        elif assim > 0:
            self.assim[assim](self.start, self.arch_paths['step{}'.format(assim)], store=assim == self.assim_nbsteps)
        else:
            for modid in self.ens_model:
                model = ctypes.cast(modid, ctypes.py_object).value
                model(dateref=self.start, length=self.reanalysis, overlap=self.overlap)
        
        # Archiving
        self.archiving(spinup=spinup, forecast=forecast, assim=assim)
                    
        # Prepare next cycle
        self.logger.info('Prepare next cycle')
        if spinup:
            model = ctypes.cast(self.model, ctypes.py_object).value
            model.prepare_next_run()

        elif forecast:
            for modid in self.ens_model:
                model = ctypes.cast(modid, ctypes.py_object).value
                model.prepare_next_run(restore_state=self.overlap == 0, init_now=True,
                                       shift=-self.forecast-self.overlap)
        else:
            if assim == 0 or assim == self.assim_nbsteps:
                if self.forecast == 0:
                    for modid in self.ens_model:
                        model = ctypes.cast(modid, ctypes.py_object).value
                        model.prepare_next_run(time=True, shift=-self.overlap, init_now=True)
                else:
                    for modid in self.ens_model:
                        model = ctypes.cast(modid, ctypes.py_object).value
                        model.prepare_next_run(save_state=self.overlap == 0, persist=True, shift=0)

    def forecast_parallel(self, arg):
        """Run forecast in parallel"""

        model = ctypes.cast(arg[0], ctypes.py_object).value
        model(dateref=self.start, length=arg[1])
        gherkins = model.pickle()
        return gherkins

    def save_time(self, mode):
        """ Save or restore model parameters
            - mode:  'save' or 'restore'
        """
        
        if mode == 'save':
            for modid in self.ens_model:
                model = ctypes.cast(modid, ctypes.py_object).value
                model.pickle(time_only=True)
        elif mode == 'restore':
            for m, modid in enumerate(self.ens_model):
                model = ctypes.cast(modid, ctypes.py_object).value
                model.unpickle(time_only=True)

    def prepare_archive(self, spinup=False):
        """Prepare archiving idrectories
            - spinup:  prepare for spinup only
        """
    
        try:
            if spinup:
                # Create the directories for the spinup
                dirname = '{}/{}'.format(self.archdir, self.start0.strftime('%Y%m%d-%H%M'))
                res = '{}/spinup'.format(dirname)
                if not os.path.exists(res):
                    os.makedirs(res)
                self.arch_paths['spinup']['run'] = res
            
            else:
                # Create the directories of the reanalysis
                dirname = '{}/{}'.format(self.archdir, self.start.strftime('%Y%m%d-%H%M'))
                res = '{}/reanalysis'.format(dirname)
                if not os.path.exists(res):
                    os.makedirs(res)
                self.arch_paths['reanalysis']['run'] = res

                # Create the directories of assimilation
                if self.assim is not None:
                    for i in range(1, self.assim_nbsteps+1):
                        step = 'step{}'.format(i)
                        self.arch_paths[step] = {}
                        res = '{}/{}/assim'.format(dirname, step)
                        if not os.path.exists(res):
                            os.makedirs(res)
                        self.arch_paths[step]['assim'] = res
                        res = '{}/{}/obs'.format(dirname, step)
                        if not os.path.exists(res):
                            os.makedirs(res)
                        self.arch_paths[step]['obs'] = res
                                    
                # Create the directories of the forecast
                if self.forecast > 0:
                    datefct = self.start + timedelta(seconds=self.reanalysis)
                    dirname = '{}/{}'.format(self.archdir, datefct.strftime('%Y%m%d-%H%M'))
                    res = '{}/forecast'.format(dirname)
                    if not os.path.exists(res):
                        os.makedirs(res)
                    self.arch_paths['forecast']['run'] = res

        except IOError as err:
            msg = 'Cannot create archiving directory:\n{}'.format(err)
            self.logger.error(msg)
            raise ExperimentError(msg)

    def archiving(self, spinup=False, forecast=False, assim=0):
        """Archive the experiment outputs
            - spinup: archiving spinup?
            - assim: archiving assimilation? Which step
            - forecast: archiving forecast?
        """
        
        self.logger.info('Archiving.')
        
        if spinup:
            model = ctypes.cast(self.model, ctypes.py_object).value
            model.move_outputs(self.arch_paths['spinup'])
            model.dump_restart(self.arch_paths['restart'])
        elif assim > 0:
            self.assim[assim].move_outputs(self.arch_paths['step{}'.format(assim)])
            if assim == self.assim_nbsteps:
                for modid in self.ens_model:
                    model = ctypes.cast(modid, ctypes.py_object).value
                    model.move_outputs(self.arch_paths['reanalysis'])
        elif forecast:
            for modid in self.ens_model:
                model = ctypes.cast(modid, ctypes.py_object).value
                model.move_outputs(self.arch_paths['forecast'])
        else:
            for modid in self.ens_model:
                model = ctypes.cast(modid, ctypes.py_object).value
                model.move_outputs(self.arch_paths['reanalysis'])

    def dump_restart(self):
        """Dump restart files"""

        # Dump the model restart file
        for modid in self.ens_model:
            model = ctypes.cast(modid, ctypes.py_object).value
            model.dump_restart(self.arch_paths['restart'])

        # Dump the assimilation information
        if self.exp_type == "Assim Run" and self.start > self.start0 + timedelta(seconds=self.spinup):
            for assim in self.assim[1:]:
                assim.dump_restart(self.arch_paths['restart'], self.start)

    def __repr__(self):
        """Information"""
        
        string = 'Experiment \n'
        string += '   name:               {}\n'.format(self.name)
        string += '   type:               {}\n'.format(self.exp_type)
        string += '   carry on:           {}\n'.format(self.carry_on)
        string += '   model:              {}\n'.format(self.model_type)
        if self.spinup == 0:
            string += '   spinup:             None\n'
        else:
            string += '   spinup:             {:%d/%m/%Y %H:%M} - {:%d/%m/%Y %H:%M}\n'\
                .format(self.start0, self.start0 + timedelta(seconds=self.spinup))
        string += '   reanalysis:         {:%d/%m/%Y %H:%M} - {:%d/%m/%Y %H:%M}\n'\
            .format(self.start, self.stop)
        if self.exp_type == 'Dry Run' or self.exp_type == 'Assim Run':
            val, unit = sec2unit(self.reanalysis)
            string += '   reanalysis window:  {} {}\n'.format(val, unit)
            val, unit = sec2unit(self.reanalysis-self.overlap)
            string += '   overlap:            {} {}\n'.format(val, unit)
            val, unit = sec2unit(self.forecast)
            string += '   forecast window:    {} {}\n'.format(val, unit)
        if self.exp_type == 'Assim Run':
            string += '   Assimilation steps: {}\n'.format(self.assim_nbsteps)
            for i in range(1, self.assim_nbsteps+1):
                string += self.assim[i].__repr__()
        return string
