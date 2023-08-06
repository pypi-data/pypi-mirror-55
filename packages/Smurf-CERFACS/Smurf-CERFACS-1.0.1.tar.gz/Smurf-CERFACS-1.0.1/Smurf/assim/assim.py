"""
Assim model
============

assimilation scheme:
    - KF
    - EnKF: stochastic
"""

import logging
import os
import shutil
from datetime import datetime, timedelta
import numpy as np
import itertools as it
import pickle
import ctypes
from ..observations.instanciate import instanciate as instance_obs
from ..observations.obs_vector import ObsVector
from ..covariances.obs_cov import ObsCov
from ..common.vector import Vector
from ..common.functions import sec2unit, format2sec
from ..common.errors import AssimError, PPError

# Dictionary of observation instrument instances
observation = {}


# ======================================================


class Assim(object):

    logger = logging.getLogger('Assimilation')
    logging.Logger.setLevel(logger, logging.INFO)

    # Assimilation window
    @property
    def window(self):
        return self._window
    
    @window.setter
    def window(self, value):
        try:
            if isinstance(value, list):
                self._window = format2sec(value)
            else:
                self._window = value
        except ValueError:
            msg = 'Incorrect window {}.'.format(value)
            self.logger.error(msg)
            raise AssimError(msg)
        
    # Spinup before assimilation
    @property
    def spinup(self):
        return self._spinup
    
    @spinup.setter
    def spinup(self, value):
        if value == 0:
            self._spinup = 0
            return 
        try:
            if isinstance(value, list):
                self._spinup = format2sec(value)
            else:
                self._spinup = value
        except ValueError:
            msg = 'Incorrect spinup {}.'.format(value)
            self.logger.error(msg)
            raise AssimError(msg)
        else:
            # Multiple of model time step
            try:
                model = ctypes.cast(self.model, ctypes.py_object).value
                self._spinup = self._spinup / int(model.step) * int(model.step)
            except ZeroDivisionError:
                pass
            if self._spinup >= self.window:
                msg = 'Spinup greater than window.'
                self.logger.error(msg)
                raise AssimError(msg)

    # subwindow within the reanalysis
    @property
    def subwindow(self):
        return self._subwindow
    
    @subwindow.setter
    def subwindow(self, value):
        if value == 0:
            self._subwindow = 0
            return 
        try:            
            if isinstance(value, list):
                self._subwindow = format2sec(value)
            else:
                self._subwindow = value
        except ValueError:
            msg = 'Incorrect subwindow {}.'.format(value)
            self.logger.error(msg)
            raise AssimError(msg)
        else:
            if self._subwindow == 0:
                model = ctypes.cast(self.model, ctypes.py_object).value
                self._subwindow = int(model.step)
            if (self.window - self.spinup) % self._subwindow != 0:
                    msg = 'Subwindow not consistent with spinup and window.'.format(value)
                    self.logger.error(msg)
                    raise AssimError(msg)
            if self.step < self.nbstep and self.window != self._subwindow + self.spinup:
                msg = 'For step {}/{}, the subwindow should correspond to the window.'.format(self.step, self.nbstep)
                self.logger.error(msg)
                raise AssimError(msg)

    # =================================== #
    #               Methods               #
    # =================================== #

    def __init__(self, config, ens_model, window, overlap=0, wdir='Work', archdir='Archive',
                 step=1, nbstep=1, parallel=False, nbproc=0, postproc=False):
        """Constructor
            config:       path and name of the config.yml
            ens_model:    ens_model id for propagation
            window:       assimilation window
            overlap:      overlap of windows
            wdir:         working directory
            archdir:      archiving directory
            step:         step number
            parallel:     parallelisation of the ensemble
            nbproc:       number of processors for the parallelisation
            postproc:     instanciation for post-processing purposes
        """

        global observation

        # General attributes
        self.postproc = postproc               # Instanciation for post processing
        self.step = step                       # Assimilation step for this instance
        self.nbstep = nbstep                   # Number of assimilation steps for the experiment
        self.parallel = parallel               # Parallelisation of the ensemble
        self.nbproc = nbproc                   # Number of processors for the parallelisation
        if self.nbproc < 2:
            self.parallel = False
        self.size = len(ens_model)             # Size of the ensemble
        self.control = {}                      # Dictionary of control variables
        self.start0 = None                     # Start of the window before spinup (datetime)
        self.start = None                      # Start of the window after spinup (datetime)
        self.stop = None                       # End of the experiment (datetime)
        self.smoother = False                  # Rerun the assimilation window with the analysis values
        self.window = window                   # Assimilation window
        self.spinup = 0                        # Spinup in the assimilation window
        self.subwindow = 0                     # Length of a subwindow within the assimilation window
        self.overlap = overlap                 # Overlap of the windows between two assimilation cycles:
        #                                        start cycle2 = stop cycle1 - overlap

        # Path and name of the configuration file
        if self.postproc:
            config_split = config.split('/')[-1].split('.')
            self.config = '{}/init/{}_step{}.{}'.format(archdir, config_split[0],
                                                        step, config_split[-1])
        else:
            self.config = config

        # Model(s)
        self.model = ens_model[0]
        if self.size > 1:
            self.ens_model = ens_model
        else:
            self.ens_model = []
        model = ctypes.cast(self.model, ctypes.py_object).value
        self.parameter = model.parameter

        # Observations
        observation = {'keep': None,                   # Observations keep: observation read once for the experiment
                       'cycle': None}                  # cycle: observations read at each cycle

        # Assimilation vectors and matrices
        self.yo = None                         # Observation vector
        self.xb = None                         # Control vector
        self.Hxb = None                        # Control vector in observation space
        self.d = None                          # Innovation vector
        self.dx = None                         # Increment vector
        self.xa = None                         # Analysis vector
        self.B = None                          # Background error covariance matrix
        self.R = None                          # Observation error covariance matrix
        self.A = None                          # Analysis error covariance matrix
        self.HBHt = None                       # B matrix in observation space
        self.BHt = None                        # B matrix between model and observation space

        # Other assimilation attributes
        self.runlist = []                      # List of innovation times

        # Configuration elements
        self.conf_B = {}                      # Dictionary for the configuration of B
        self.conf_R = {}                      # Dictionary for the configuration of R
        self.conf_obs = {}                    # Dictionary for the observations
        self.write_format = 'txt'             # Format for output files

        # Directories
        self.wdir = '{}/assim_step{}'.format(wdir, self.step)  # Working directory
        self.archdir = archdir                 # Archiving directory

        # Read the config.yml file
        self.read_config()
           
        if self.postproc:
            self.yo = ObsVector([])
        else:

            # Check the compatibility with sliding windows
            if self.overlap > 0 and not self.smoother:
                msg = 'No sliding windows allowed if no smoother.'
                self.logger.error(msg)
                raise AssimError(msg)

            # Copy the file in the archiving directory
            name = self.config.split('/')[-1]
            name = '{}_step{}.yml'.format(name[:-4], self.step)
            shutil.copyfile(self.config, os.path.join('{}/init'.format(self.archdir), name))           
                    
            # Check control variables
            bal = [v for v in self.control if v in self.parameter['balance_var']]
            for var in bal:
                for varbal in self.parameter['balance_var'][var]:
                    if varbal not in self.control:
                        msg = '{} is balanced with {} and must be in the control vector.'.format(varbal, var)
                        self.logger.error(msg)
                        raise AssimError(msg)

            # Prepare observations that will be kept for the whole experiment
            for conf in self.conf_obs:
                if conf['keep']:
                    if observation['keep'] is None:
                        observation['keep'] = [instance_obs(conf['instrument'], conf,
                                                            self.parameter, size=self.size)]
                    else:
                        observation['keep'].append(instance_obs(conf['instrument'], conf,
                                                                self.parameter, size=self.size))

    def read_config(self):
        """Read the configuration file"""

        msg = 'The Assim method read_config is not implemented'
        raise NotImplementedError(msg)

    def __call__(self, datestart, paths, store):
        """Calculate an analysis and propagate it
            - datestart:    datetime of the start
            - paths:        archiving paths
            - store:        store propagation of analysis
        """

        # Update control vector information
        for modid in self.ens_model:
            model = ctypes.cast(modid, ctypes.py_object).value
            model.control = self.control

        # Prepare working directory
        if os.path.exists(self.wdir):
            shutil.rmtree(self.wdir)
        os.makedirs(self.wdir)

        # Prepare yo and cycles to run
        flag = self.get_obs(datestart, paths)
        
        if flag:
            # Assimilation for the cycle
            # ---------------------------
                
            # Define observation error covariance matrix
            self.R = ObsCov(self.yo, self.conf_R)
        
            # Run the spinup
            if self.spinup > 0:
                self.propagate(datestart=self.start0, length=self.spinup, file='rean_0',
                               directory=False, time=True, overlap=0)
        
            # Save first state
            if self.smoother:
                self.propagate(datestart=self.start0, length=0, directory=False,
                               save_state=True, time=False)
            
            # Loop on cycles
            datestart = self.start
            indst = 0
            cnt = 1
            if self.smoother:
                log = 'bkg'
            else:
                log = 'rean'

            model = ctypes.cast(self.model, ctypes.py_object).value
            while datestart < self.stop:
                # Analysis step
                dumplist = [t for t in self.runlist if model.start < t <= model.start + self.subwindow]
                if not dumplist == []:
                    # Define observation slice
                    i = indst + 1
                    while i < len(self.yo.obs_info['time']) and self.yo.obs_info['time'][i] <= dumplist[-1]:
                        i += 1
                    indend = i
                    # Calculate innovation
                    self.logger.info('Calculate innovations')
                    self.calc_innovation(datestart, '{}_{:02d}'.format(log, cnt), dumplist, indst, indend)
                    # Calculate increment
                    self.logger.info('Calculate increment')
                    self.calc_increment(indst, indend, cnt)
                    # Store the increment and take it into account
                    self.use_increment(cnt)   
                    # Set assimilation information
                    self.set_assim_results(indst, indend)
                    # Update observation slice
                    indst = indend 
            
                # Prepare analysis propagation
                self.logger.info('Propagation')
                time = True
                if datestart + timedelta(seconds=self.subwindow) == self.stop:
                    time = False   
                if not dumplist:
                    self.propagate(datestart=self.start0, length=0, directory=False,
                                   dump_state=self.smoother, time=False)
                elif self.smoother:
                    self.propagate(datestart=self.start0, length=0, directory=False,
                                   restore_state=True, time=False, init_now=True)
                else:
                    self.propagate(datestart=self.start0, length=0, directory=False, time=time)

                # Propagation
                overlap = self.overlap
                overlap_time = self.stop - timedelta(seconds=self.overlap)
                if overlap_time < datestart or overlap_time > datestart + timedelta(seconds=self.subwindow):
                    overlap = 0
                if self.smoother:
                    if dumplist or self.step == self.nbstep:
                        self.propagate(datestart, length=self.subwindow, file='rean_{:02d}'.format(cnt),
                                       directory=False, time=time, overlap=overlap) 
                else: 
                    if not dumplist:
                        self.propagate(datestart, length=self.subwindow, file='rean_{:02d}'.format(cnt),
                                       directory=False, time=time, overlap=overlap)
                                                                                    
                # Update
                self.update()
                cnt += 1
            
                # Next cycle             
                datestart += timedelta(seconds=self.subwindow)
                    
            # Finish
            self.model_output_files(store)
            self.write_assim_output_files()
        
        else:
            # Propagation only for the cycle
            # --------------------------------
            self.logger.info('Propagation only')
            self.propagate(datestart=self.start0, length=self.window, file=None,
                           directory=False, time=False, overlap=self.overlap)

        # Reset time window rejection
        self.yo.reset_time_out()

    def get_obs(self, datestart, paths):
        """Get observation information
            - datestart:    datetime of the start
            - paths:      archiving paths
        """

        global observation

        # Reinitialisation of obs vector
        if self.yo is not None:
            self.yo = None
            
        # Start and stop time
        self.start0 = datestart
        self.stop = datestart + timedelta(seconds=self.window)
        
        # Taking into account the spinup
        self.start = self.start0 + timedelta(seconds=self.spinup)
        
        self.logger.info('Preparing observations from {} to {}.'.
                         format(self.start.strftime('%d/%m/%Y %H:%M'), self.stop.strftime('%d/%m/%Y %H:%M')))
        
        # Preparing observations for the cycle
        for conf in self.conf_obs:
            if not conf['keep']:
                if observation['cycle'] is None:
                    observation['cycle'] = [instance_obs(conf['instrument'], conf, self.start, self.size)]
                else:
                    observation['cycle'].append(instance_obs(conf['instrument'], conf, self.start, self.size))

        # Instanciate observation vector
        obs_list = [o for obs in observation.values() if obs is not None for o in obs]
        self.yo = ObsVector(obs_list, self.start, self.stop)

        # Defining coordinates understandable by the model
        tsec = [(t-self.start0).days * 86400 + (t-self.start0).seconds
                + (t-self.start0).microseconds * 1.e-6 for t in self.yo.coord['time']]
        self.yo.model_coord['time'] = tsec
        model = ctypes.cast(self.model, ctypes.py_object).value
        model.convert_coord(self.yo.coord, self.yo.model_coord)

        # Reject observations out of domain
        self.yo.reject_domain_out(model.get_coord_limits())

        # QC check
        self.yo.qc_check()

        # Write report on observations
        self.yo.report('{}/report.txt'.format(paths['obs']))

        # Get observations
        self.runlist = self.yo.get_observations()

        # Check number of observations
        if self.yo.dim == 0:
            self.logger.info('No observation files. Skip the assimilation for this step.')
            return False
            
        # Return True to carry on the assimilation step
        return True

    def apply_perturbation(self):
        """ Sample and apply perturbations"""

        pass

    def calc_innovation(self, datestart, filename, dumplist, ist, iend):
        """Get the background state in obs space and
            calculate the innovation
            - datestart:   datetime of the start of the cycle
            - filename:    filename for the model log
            - dumplist:    list of time of observation
            - ist:         start index for obs vector
            - iend:        ending index for obs vector
        """

        # Get background vector
        model = ctypes.cast(self.model, ctypes.py_object).value
        self.xb, Mxb, self.Hxb, _ = model.get_Mxb_Hxb(datestart, self.subwindow, filename,
                                                      dumplist, self.smoother, self.yo.obs_info)

        # Innovation
        self.d = self.yo[ist:iend] - self.Hxb

    def calc_increment(self, ist, iend, cnt):
        """Calculate increment
            - ist:         starting index for the cycle
            - iend:        ending index for the cycle
            - cnt:         increment id
        """
        
        msg = 'The Assim method calc_increment is not implemented'
        raise NotImplementedError(msg)

    def use_increment(self, cnt):
        """Store the increment and take it into account
            - cnt:     increment id
        """
        model = ctypes.cast(self.model, ctypes.py_object).value
        
        # Check increment
        self.dx = model.check_increment(bkg=self.xb, increment=self.dx)
        
        # Take increment into account
        model.set_changes(bkg=self.xb, increment=self.dx)
        
        # Store the increment        
        name = '{}/increment_{:02d}.txt'.format(self.wdir, cnt)
        self.store_increment(name)

    def store_increment(self, name, member=0):
        """Launch the increment storage depending on the format
            - name:     increment name
            - member:   ensemble member id
        """

        if self.write_format == 'txt':
            # Text file format
            self.store_increment_txt(name, member)

    def store_increment_txt(self, name, member=0):
        """Store the increment
            - name:     increment name
            - member:   ensemble member id
        """

        model = ctypes.cast(self.model, ctypes.py_object).value
        with open(name, 'wb') as fout:
            
            # Write header
            fout.write('Increments calculated on: {}\n'.format(datetime.now().strftime('%d/%m/%Y %H:%M'))
                       .encode('utf-8'))
            fout.write('for the model {}\n'.format(model.name).encode('utf-8'))
            fout.write('-----------------------------------------------------------------------\n'.encode('utf-8'))
            
            # Write increments
            for v, var in enumerate(self.control):
                ind0 = model.first_node[v]
                ind1 = model.first_node[v+1]  
                nbv = ind1 - ind0
                if nbv > 5:
                    nbcol = 5
                    nbend = ind0 + int(nbv / nbcol) * nbcol
                else:
                    nbcol = nbv
                    nbend = ind0
                nblin = int(nbv / nbcol)
                nbmod = int(nbv % 5)
                fout.write('{} {}\n'.format(var, self.control[var]).encode('utf-8'))

                # Write background
                if var in self.parameter['store_anl']:
                    fout.write('   background \n'.encode('utf-8'))
                    try:
                        np.savetxt(fout, self.xb[ind0:nbend].array.reshape(nblin, nbcol), fmt='%12.3f')
                    except ValueError:
                        pass
                    if nbmod > 0:
                        np.savetxt(fout, self.xb[nbend:ind1].array.reshape(nblin, nbmod), fmt='%12.3f')

                # Write increment
                fout.write('   increment \n'.encode('utf-8'))
                try:
                    np.savetxt(fout, self.dx[ind0:nbend].array.reshape(nblin, nbcol), fmt='%12.3f')
                except ValueError:
                    pass
                if nbmod > 0:
                    np.savetxt(fout, self.dx[nbend:ind1].array.reshape(nblin, nbmod), fmt='%12.3f')

                # Write analysis
                if var in self.parameter['store_anl']:
                    fout.write('   analysis \n'.encode('utf-8'))
                    try:
                        np.savetxt(fout, self.xa[ind0:nbend].array.reshape(nblin, nbcol), fmt='%12.3f')
                    except ValueError:
                        pass
                    if nbmod > 0:
                        np.savetxt(fout, self.xa[nbend:ind1].array.reshape(nblin, nbmod), fmt='%12.3f')

                fout.write('\n'.encode('utf-8'))

    def store_cov(self, cnt):
        """Store background and analysis error covariance matrices"""
        
        name = '{}/covariance_{:02d}.pic'.format(self.wdir, cnt)
        control = []
        model = ctypes.cast(self.model, ctypes.py_object).value
        for v, var in enumerate(self.control):
            if var in self.parameter['composite']:
                control.extend([(varcomp, ind, 0) for varcomp, ind in
                                it.product(self.parameter['composite'][var][0], self.control[var])])
            else:
                nb = int((model.first_node[v+1] - model.first_node[v]) / len(self.control[var]))
                control.extend([(var, ind, i) for ind, i in it.product(self.control[var], range(nb))])
        pickle.dump([self.B.array, self.A.array, self.HBHt.array, self.BHt.array, control], open(name, 'wb'))

    def read_cov(self, cov_list, datedir, subwindow):
        """Read background and analysis error covariance matrices
            - cov_list:   list of covariance to read 'B', 'A', 'HBHt', 'BHt'
            - datedir:   cycling directory
            - subwindow: subwindow to read
        """

        covs = ['B', 'A', 'HBHt', 'BHt']
        name = '{}/{}/step{}/assim/covariance_{:02d}.pic'.format(self.archdir, datedir, self.step, subwindow)
        tmp = pickle.load(open(name, 'rb'))
        cov = []
        for c in cov_list:
            cov.append(tmp[covs.index(c)])

        return cov, tmp[-1]

    def set_assim_results(self, ist, iend):
        """Set the assimilation results for the observations
            - ist:   starting index
            - iend:  ending endex
        """
        
        self.yo.set_omb(self.d, ist, iend)

    def propagate(self, datestart, length, file=None, directory=True, save_state=False,
                  restore_state=False, dump_state=False, time=True, overlap=0, init_now=False):
        """Propagation of the state by the model and next step"""

        model = ctypes.cast(self.model, ctypes.py_object).value
        if length > 0:
            model(dateref=datestart, length=length, file=file, overlap=overlap) 
        model.prepare_next_run(directory=directory, save_state=save_state,
                               restore_state=restore_state, dump_state=dump_state,
                               time=time, init_now=init_now)               

    def update(self):
        """Update perturbations if required"""

        # Required only for ensemble schemes
        pass
        
    def model_output_files(self, store):
        """Reconstruct the reanalysis file
            Move the outputs from model workdir,
            - store:   reconstruct and store reanalysis
        """

        model = ctypes.cast(self.model, ctypes.py_object).value
        
        # Move bkg files
        listfile = os.listdir(model.outdir)
        bkglist = [f for f in listfile if f[:3] == 'bkg']
        for bkgfile in bkglist:
            if self.size > 1 and model.member >= 1:
                outname = bkgfile.split('.')
                outfile = '{}/{}_memb{}.{}'.format(self.wdir, outname[0], model.member, outname[1])
            else:
                outfile = '{}/{}'.format(self.wdir, bkgfile)
            shutil.move(os.path.join(model.outdir, bkgfile), outfile)
            
        if store:
            # Reconstruct reanalysis file
            reanlist = [f for f in listfile if f[:4] == 'rean']
            model.reconstruct_output_file(reanlist)
            for file in reanlist:
                os.remove(os.path.join(model.outdir, file))
        else:
            # Move rean files
            reanlist = [f for f in listfile if f[:4] == 'rean']
            for reanfile in reanlist:
                if self.size > 1 and model.member >= 1:
                    outname = reanfile.split('.')
                    outfile = '{}/{}_memb{}.{}'.format(self.wdir, outname[0], model.member, outname[1])
                else:
                    outfile = '{}/{}'.format(self.wdir, reanfile)
                shutil.move(os.path.join(model.outdir, reanfile), outfile)
    
    def write_assim_output_files(self):
        """Write assimilation information"""

        name = '{}/obs_assimilated.txt'.format(self.wdir)
        self.yo.write_omb(name)

    def read_assim_output_files(self, datedir):
        """Read assimiation information"""

        name = '{}/{}/step{}/obs/obs_assimilated.txt'.format(self.archdir, datedir, self.step)
        return self.yo.read_omb(name)

    def move_outputs(self, paths):
        """Move outputs into archiving directory
           - paths:       dictionary with the paths for archiving assimilation f
        """
    
        # Move assimilation files
        try:
            if os.path.exists(os.path.join(self.wdir, 'obs_assimilated.txt')):
                shutil.move(os.path.join(self.wdir, 'obs_assimilated.txt'),
                            os.path.join(paths['obs'], 'obs_assimilated.txt'))
            listfile = os.listdir(self.wdir)
            for file in listfile:
                shutil.move(os.path.join(self.wdir, file), os.path.join(paths['assim'], file))
        except IOError as err:
            msg = 'Cannot move assimilation files: \n{}'.format(err)
            self.logger.error(msg)
            raise AssimError(msg)

    def dump_restart(self, restartdir, dateref):
        """Dump restart files
            - restartdir:  directory containing the restart files
            - dateref:     datetime of the restart
        """

        model = ctypes.cast(self.model, ctypes.py_object).value
        model.control = self.control

        # Filename
        thedate = dateref.strftime('%Y%m%d-%H%M')
        filename = '{}/{}_assim_step{}.txt'.format(restartdir, thedate, self.step)

        # Write file
        with open(filename, 'wb') as fout:
            fout.write('#Assimilation information for restart written on {}\n'
                       .format(datetime.now().strftime('%d/%m/%Y %H:%M')).encode('utf-8'))
            fout.write('#---------------------------------------------------------------\n\n'.encode('utf-8'))
            fout.write('#Analysis:\n'.encode('utf-8'))
            if self.yo.dim == 0:
                fout.write('#No observation assimilated'.encode('utf-8'))
                return
            np.savetxt(fout, self.xa.array, fmt='%12.3f')

        # Write model information
        model.dump_assim_restart(restartdir)

    def carry_on(self, restartdir, dateref):
        """Take into account the previous analysis if carrying on the experiment
            - restartdir:  directory containing the restart files
            - dateref:     datetime of the restart
        """

        # Filename
        thedate = dateref.strftime('%Y%m%d-%H%M')
        filename = '{}/{}_assim_step{}.txt'.format(restartdir, thedate, self.step)

        # Read file
        self.xa = Vector(np.genfromtxt(filename))
        if self.xa.dim == 0:
            return

        # Take the analysis into account
        model = ctypes.cast(self.model, ctypes.py_object).value
        model.control = self.control
        model.set_changes(bkg=self.xa, increment=Vector(dim=self.xa.dim))

    def extract_increment(self, variable, index, assim_type, datedir, subwindow):
        """Extract assimilation information from increment file
            - variable:       list of control variables to extract, can be a composite element
            - index:          list of indices (list) for each variable
            - assim_type:     list of type: 'bkg', 'anl', 'inc'
            - datedir:        cycling directory
            - subwindow:      subwindow to extract
        """

        # Sort assimilation type
        ast_dic = {'bkg': 'background',
                   'inc': 'increment',
                   'anl': 'analysis'}
        ast = [ast_dic[a] for a in ast_dic if a in assim_type]

        # Control variable
        varbs = []
        for v in variable:
            if v in self.control:
                varbs.append(v)
            elif v in [vv for comp in list(self.parameter['composite'].values()) for vv in comp[0]]:
                varbs.append(list(filter(lambda d: (v in d[1][0]), self.parameter['composite'].items()))[0][0])
            else:
                msg = 'There is no {} in control vector'.format(v)
                self.logger.error(msg)
                raise PPError(msg)

        # Subwindow:
        subwindow = ['{:02d}'.format(w) for w in subwindow]

        # Loop on subwindow
        ressub = []
        for sub in subwindow:
            filename = '{}/{}/step{}/assim/increment_{}.txt'.format(self.archdir, datedir,
                                                                    self.step, sub)

            # Open the file
            with open(filename, 'r') as fin:
                data = fin.readlines()

            # Variable indices:
            var_ind = [i for v in varbs for i in range(len(data)) if data[i].split() and data[i].split()[0] == v]

            res = {}
            # Loop on variables:
            for v, iv in enumerate(var_ind):
                var = data[iv].split()[0]
                varasked = variable[v]
                if var == varasked:
                    cln_ind = None
                else:
                    cln_ind = self.parameter['composite'][var][0].index(varasked)
                indvar = data[iv][len(var):-1].strip()
                res[varasked] = {}

                # Find indices
                try:
                    ind_read = [int(i) for i in indvar[1:-1].split(',')]
                except ValueError:
                    ind_read = [s.strip()[1:-1] for s in indvar[1:-1].split(',')]

                # loop on assim_type
                assim_ind = iv + 1
                for assim in ast:
                    assim_t = list(filter(lambda d: (d[1] == assim), ast_dic.items()))[0][0]
                    while assim_ind < len(data) and data[assim_ind].strip() != assim:
                        assim_ind += 1
                    assim_ind += 1

                    # Retrieve data
                    data_tmp = []
                    while assim_ind < len(data):
                        try:
                            data_tmp.extend([float(d) for d in data[assim_ind].strip().split()])
                            assim_ind += 1
                        except ValueError:
                            break
                    nbv = int(len(data_tmp) / len(ind_read))

                    # Loop on index
                    for ind in index[v]:
                        try:
                            cln = ind_read.index(ind)
                        except ValueError:
                            msg = 'There is no index {} in control variable {}'.format(ind, varasked)
                            self.logger.error(msg)
                            raise PPError(msg)
                        if ind not in res[varasked]:
                            res[varasked][ind] = {}
                        if cln_ind is None:
                            r = np.reshape(np.array(data_tmp[cln * nbv: (cln+1) * nbv]), (1, nbv))
                        else:
                            r = np.reshape(np.array(data_tmp[cln * nbv + cln_ind]), (1, 1))
                        res[varasked][ind][assim_t] = r

            ressub.append(res)

        return ressub

    def __repr__(self):
        """Information"""
        
        string = 'Step {}\n'.format(self.step)
        if self.size > 1:
            string += '   ensemble size       : {}\n'.format(self.size)
        string += '   configuration       : {}\n'.format(self.config)
        val, unit = sec2unit(self.spinup)
        string += '   spinup              : {} {}\n'.format(val, unit)
        val, unit = sec2unit(self.subwindow)
        string += '   assimilation cycle  : {} {}\n'.format(val, unit)
        return string
