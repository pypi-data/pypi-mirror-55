"""
EnsKalmanFilter
===============

Assimilation scheme

"""

import logging
import numpy as np
from datetime import datetime
import yaml
import ctypes
from pathos.multiprocessing import ProcessPool
from .assim import Assim
from .perturbation import Perturbation
from ..common.matrix import Vector, Matrix
from ..covariances.bkg_cov import BkgCov
from ..common.functions import sec2unit
from ..common.errors import EnKFError

# ======================================================


class EnsKalmanFilter(Assim):

    logger = logging.getLogger('Ensemble Kalman Filter')
    logging.Logger.setLevel(logger, logging.INFO)

    # Size of the ensemble
    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        try:
            self._size = int(value)
        except ValueError:
            msg = 'Incorrect size {} for the ensemble.'.format(value)
            self.logger.exception(msg)
            raise EnKFError(msg)
        else:
            if self._size < 2:
                msg = 'Cannot run an ensemble with {} member(s).'.format(value)
                self.logger.exception(msg)
                raise EnKFError(msg)

    # Seed the ensemble
    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        if value == 'once':
            # Seed only at start of the first cycle
            self._seed = 'once'
        elif not value:
            # Do not seed the ensemble (carry on)
            self._seed = False
        else:
            # Seed at the start of each cycle
            self._seed = True

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

        # General attributes
        self.scheme = 'EnKF'                    # Assimialtion scheme
        self.variant = 'stochastic'             # Variant of the scheme
        self.parallel = False                   # Run ensemble in parallel
        self.nbproc = 0                         # Numer of processors
        self.seed = 'any'                       # Seeding the ensemble:
        #                                         once: only at the start of the first cycle
        #                                         any: at the start of each cycle (default value)

        # Assimilation vectors and matrices
        self.ens_xb = None                     # Ensemble anomalies for the control vector
        self.ens_Hxb = None                    # Ensemble anomalies for the control vector in obs space
        self.ens_d = None                      # Ensemble innovation vector
        self.ens_dx = None                     # Ensemble increment vector
        self.xb_mean = None                    # Ensemble mean for the control vector
        self.Hxb_mean = None                   # Ensemble mean for the control vector in obs space
        self.xa_mean = None                    # Ensemble mean for the analysis vector

        # Perturbations
        self.conf_pert = {}
        self.perturbation = None               # Perturbations

        # Prepare configuration
        Assim.__init__(self, config, ens_model, window, overlap, wdir, archdir, step, nbstep,
                       parallel, nbproc, postproc)

        # Checks
        if self.parallel and self.subwindow < self.window:
            self.logger.warning('No parallelisation when the assimilation window is split')
            self.parallel = False
            self.nbproc = 0

        model = ctypes.cast(self.model, ctypes.py_object).value
        if self.postproc:

            # Instanciation for post processing only
            self.perturbation = Perturbation(None)

        else:

            # Instanciate the variant
            if self.variant == 'stochastic':
                pass
            else:
                msg = 'The variant {} is not available.'.format(self.variant)
                self.logger.error(msg)
                raise EnKFError(msg)

            # Prepare perturbations
            gps_axis = model.get_gps_axis()
            self.perturbation = Perturbation(self.conf_pert, self.control, self.parameter, gps_axis)
            model.keep_gps = self.perturbation.get_gpsampler_structure()

        # Update length of control vector
        model.control = self.control

        # Define background error covariance matrix
        self.B = BkgCov(model, self.conf_B)

    def read_config(self):
        """Read the configuration file"""

        # Read the yml file
        with open(self.config, 'r') as fin:
            data = yaml.safe_load(fin)

        # Update mandatory attributes
        try:
            self.control = data['control']
            self.spinup = data['spinup']
            self.subwindow = data['subwindow']
            self.conf_obs = data['observations']
            self.conf_R = data['R']
            self.conf_pert = data['pert_distrib']
        except (KeyError, TypeError) as err:
            msg = 'Some configuration is missing:\n{}'.format(err)
            self.logger.exception(msg)
            raise EnKFError(msg)
        self.conf_B = {'type': None}

        # Update optional attributes
        try:
            self.seed = data['seed']
        except (KeyError, TypeError):
            self.seed = 'any'
        try:
            self.variant = data['variant']
        except (KeyError, TypeError):
            self.variant = 'stochastic'
        try:
            self.smoother = data['smoother']
        except (KeyError, TypeError):
            self.smoother = False

    def apply_perturbation(self):
        """ Sample and apply perturbations"""

        # Design of experiment
        if self.seed:
            self.perturbation.generate_sample(self.size)

        # Loop on ensemble members
        for m, modid in enumerate(self.ens_model):
            self.model = modid
            # Update changes
            if self.seed:
                extra = []
                for ex in self.perturbation.extra:
                    if ex is None:
                        extra.append(0)
                    else:
                        extra.append(ex[m])
                model = ctypes.cast(modid, ctypes.py_object).value
                flags = model.set_changes(state=self.perturbation.configuration,
                                          values=self.perturbation.sample[m],
                                          extra=extra)
                for f in flags:
                    if isinstance(f, dict):
                        self.perturbation.change_gpsampler_sample(index=f['index'], member=m, value=f['value'])

    def calc_innovation(self, datestart, filename, dumplist, ist, iend):
        """Get the background state in obs space and
            calculate the innovation
            - datestart:   datetime of the start of the cycle
            - filename:    filename for the model log
            - dumplist:    list of time of observation
            - ist:         start index for obs vector
            - iend:        ending index for obs vector
        """

        # Apply perturbations
        self.apply_perturbation()

        if self.parallel:
            arg = [[i, datestart, filename, dumplist, ist, iend] for i in self.ens_model]
            pool = ProcessPool(self.nbproc)
            res = pool.map(self.calc_innovation_parallel, arg)
            pool.clear()

            # Construct the ensemble vectors xb, Hxb, d
            self.ens_xb = Matrix(dim=(self.size, res[0][0].dim))
            self.ens_xb.init = True
            self.ens_Hxb = Matrix(dim=(self.size, res[0][1].dim))
            self.ens_Hxb.init = True
            self.ens_d = Matrix(dim=(self.size, res[0][2].dim))
            self.ens_d.init = True

            # Store results
            for m in range(self.size):
                self.ens_xb[m, :] = res[m][0].array
                self.ens_Hxb[m, :] = res[m][1].array
                self.ens_d[m, :] = res[m][2].array

            # Reinitialise model
            if not self.smoother:
                for m, modid in enumerate(self.ens_model):
                    model = ctypes.cast(modid, ctypes.py_object).value
                    model.unpickle(res[m][3])

        else:
            # Loop on ensemble members
            for m, modid in enumerate(self.ens_model):

                # Calculate innovation
                self.model = modid
                Assim.calc_innovation(self, datestart, filename, dumplist, ist, iend)

                # Construct the ensemble vectors xb, Hxb, d
                if m == 0:
                    self.ens_xb = Matrix(dim=(self.size, self.xb.dim))
                    self.ens_xb.init = True
                    self.ens_Hxb = Matrix(dim=(self.size, self.Hxb.dim))
                    self.ens_Hxb.init = True
                    self.ens_d = Matrix(dim=(self.size, self.Hxb.dim))
                    self.ens_d.init = True

                # Store results
                self.ens_xb[m, :] = self.xb.array
                self.ens_Hxb[m, :] = self.Hxb.array
                self.ens_d[m, :] = self.d.array

        # Calculate mean of xb and Hxb
        self.xb_mean = self.ens_xb.mean(axis=0)
        self.Hxb_mean = self.ens_Hxb.mean(axis=0)

        # Calculate anomalies of xb and Hxb
        for m in range(self.size):
            self.ens_xb[m, :] -= self.xb_mean
            self.ens_Hxb[m, :] -= self.Hxb_mean

        # Simulate observation noise for the stochastic variant
        if self.variant == 'stochastic':
            epso = Matrix(dim=self.ens_d.shape)
            epso.init = True
            rsqrt = self.R[ist:iend, ist:iend] ** 0.5
            for m in range(self.size):
                epso[m, :] = rsqrt.dot(np.random.normal(loc=0., scale=1., size=self.ens_d.shape[1]))
            self.ens_d += epso

        # Update the seed
        if self.seed == 'once':
            self.seed = False

        self.logger.debug('yo: {}'.format(self.yo[ist:iend].array))
        self.logger.debug('xb: {}'.format(self.xb_mean.array))
        self.logger.debug('Hxb: {}'.format(self.Hxb_mean.array))
        self.logger.debug('d: {}'.format(self.ens_d.mean(axis=0).array))

    def calc_innovation_parallel(self, arg):
        """Get the background state in obs space and
            calculate the innovation in parallel
            - arg = [modid, datestart, filename, dumplist, ist, iend]
            - modid:       model id
            - datestart:   datetime of the start of the cycle
            - filename:    filename for the model log
            - dumplist:    list of time of observation
            - ist:         start index for obs vector
            - iend:        ending index for obs vector
        """

        # Get background vector
        model = ctypes.cast(arg[0], ctypes.py_object).value
        xb, Mxb, Hxb, gherkins = model.get_Mxb_Hxb(arg[1], self.subwindow, arg[2], arg[3],
                                                   self.smoother, self.yo.obs_info, not self.smoother)

        # Innovation
        d = self.yo[arg[4]:arg[5]] - Hxb

        return xb, Hxb, d, gherkins

    def calc_increment(self, ist, iend, cnt):
        """Calculate increment
            - ist:         observation starting index for the cycle
            - iend:        observation ending index for the cycle
            - cnt:         increment id
        """

        # Calculate precision matrix
        self.HBHt = self.ens_Hxb.covariance()
        R = self.R[ist:iend, ist:iend]
        S = (self.HBHt + R).invert()

        # Calculate gain matrix
        self.BHt = self.ens_xb.covariance(self.ens_Hxb)
        K = self.BHt.dot(S)

        # Calculate increment
        self.ens_dx = Matrix(dim=(self.size, self.xb_mean.dim))
        self.ens_dx.init = True
        for m in range(self.size):
            self.ens_dx[m, :] = K.dot(self.ens_d[m, :])
            # Check the increment
            model = ctypes.cast(self.ens_model[m], ctypes.py_object).value
            self.ens_dx[m, :] = model.check_increment(bkg=self.ens_xb[m, :] + self.xb_mean,
                                                      increment=self.ens_dx[m, :])
        # Update B
        self.B = self.ens_xb.covariance()

        # Calculate analysis 
        dx_mean = self.ens_dx.mean(axis=0)
        self.xa_mean = self.xb_mean + dx_mean
        ens_xa = self.ens_xb + self.ens_dx
        for m in range(self.size):
            ens_xa[m, :] -= dx_mean

        self.logger.debug('dx: {}'.format(dx_mean.array))
        self.logger.debug('xa: {}'.format(self.xa_mean.array))

        # Calculate analysis covariance matrix
        self.A = ens_xa.covariance()
        normb = self.B.norm()
        norma = self.A.norm()
        self.logger.info('||B|| = {:.03f} --> ||A|| = {:.03f} ({:.02f}%)'.
                         format(normb, norma, 100. * (norma - normb) / normb))

        # Store background and analysis error covariances
        self.store_cov(cnt)

    def use_increment(self, cnt):
        """Store the increment and take it into account
            - cnt:     increment id
        """

        # Resample perturbations from gp sampler
        if not self.seed or self.smoother:
            self.perturbation.take_inc_batman_gpsampler(self.size, self.ens_dx)

        # Loop on model
        for m, modid in enumerate(self.ens_model):
            # Take increment into account
            if not self.seed or self.smoother:
                extra = []
                if self.perturbation.extra is not None:
                    for ex in self.perturbation.extra:
                        extra.append(ex[m])
                model = ctypes.cast(self.ens_model[m], ctypes.py_object).value
                flags = model.set_changes(bkg=self.ens_xb[m, :] + self.xb_mean, increment=self.ens_dx[m, :],
                                          extra=extra)
                for f in flags:
                    if isinstance(f, dict):
                        self.perturbation.change_gpsampler_sample(index=f['index'], member=m, value=f['value'])

            # Store the increment
            name = '{}/increment_{:02d}_memb{}.txt'.format(self.wdir, cnt, m + 1)
            self.store_increment(name, m)

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
            fout.write('Member {:02d}\n'.format(member + 1).encode('utf-8'))
            fout.write('-----------------------------------------------------------------------\n'.encode('utf-8'))

            # Write increments
            for v, var in enumerate(self.control):
                ind0 = model.first_node[v]
                ind1 = model.first_node[v + 1]
                nbv = ind1 - ind0
                if nbv > 5:
                    nbcol = 5
                    nbend = ind0 + int(nbv / nbcol) * nbcol
                else:
                    nbcol = nbv
                    nbend = ind1
                nblin = int(nbv / nbcol)
                nbmod = int(nbv % nbcol)
                fout.write('{} {}\n'.format(var, self.control[var]).encode('utf-8'))

                # Write background
                if var in self.parameter['store_anl']:
                    fout.write('   background \n'.encode('utf-8'))
                    try:
                        np.savetxt(fout, (self.ens_xb[member, ind0:nbend] +
                                          self.xb_mean[ind0:nbend]).array.reshape(nblin, nbcol), fmt='%12.3f')
                    except ValueError:
                        pass
                    if nbmod > 0:
                        np.savetxt(fout, (self.ens_xb[member, nbend:ind1] +
                                          self.xb_mean[nbend:ind1]).array.reshape(nblin, nbmod), fmt='%12.3f')

                # Write increment
                fout.write('   increment \n'.encode('utf-8'))
                try:
                    np.savetxt(fout, self.ens_dx[member, ind0:nbend].array.reshape(nblin, nbcol), fmt='%12.3f')
                except ValueError:
                    pass
                if nbmod > 0:
                    np.savetxt(fout, self.ens_dx[member, nbend:ind1].array.reshape(nblin, nbmod), fmt='%12.3f')

                # Write analysis
                if var in self.parameter['store_anl']:
                    fout.write('   analysis \n'.encode('utf-8'))
                    try:
                        np.savetxt(fout, (self.ens_xb[member, ind0:nbend] + self.xb_mean[ind0:nbend] +
                                          self.ens_dx[member, ind0:nbend]).array.reshape(nblin, nbcol), fmt='%12.3f')
                    except ValueError:
                        pass
                    if nbmod > 0:
                        np.savetxt(fout, (self.ens_xb[member, nbend:ind1] + self.xb_mean[nbend:ind1] +
                                          self.ens_dx[member, nbend:ind1]).array.reshape(nblin, nbmod), fmt='%12.3f')

                fout.write('\n'.encode('utf-8'))

    def set_assim_results(self, ist, iend):
        """Set the assimilation results for the observations
            - ist:   starting index
            - iend:  ending endex
        """

        self.yo.set_omb(self.ens_d, ist, iend)

    def propagate(self, datestart, length, file='rean', directory=True, save_state=False,
                  restore_state=False, dump_state=False, time=True, overlap=0, init_now=False):
        """Propagation of the state by the model and next step"""

        if self.parallel and length > 0:
            arg = [[i, datestart, length, file, overlap] for i in self.ens_model]
            pool = ProcessPool(self.nbproc)
            res = pool.map(self.propagate_parallel, arg)
            pool.clear()

            # Reinitialise model
            for m, modid in enumerate(self.ens_model):
                model = ctypes.cast(modid, ctypes.py_object).value
                if res[m][1]:
                    model.unpickle(res[m][1], overlap=True)
                model.unpickle(res[m][0])
                model.prepare_next_run(directory=directory, save_state=save_state,
                                       restore_state=restore_state, dump_state=dump_state,
                                       time=time, init_now=init_now)

        else:
            for modid in self.ens_model:
                self.model = modid
                Assim.propagate(self, datestart, length, file=file, directory=directory,
                                save_state=save_state, restore_state=restore_state,
                                dump_state=dump_state, time=time, overlap=overlap, init_now=init_now)

    @staticmethod
    def propagate_parallel(arg):
        """Propagation of the state by the model in parallel"""

        model = ctypes.cast(arg[0], ctypes.py_object).value
        model(dateref=arg[1], length=arg[2], file=arg[3], overlap=arg[4])
        gherkins = [model.pickle()]
        if arg[4] > 0:
            gherkins.append(model.pickle(overlap=True))
        else:
            gherkins.append([])
 
        return gherkins

    def update(self):
        """Update perturbations if required"""

        # Update perturbations 
        if self.seed:
            model = ctypes.cast(self.model, ctypes.py_object).value
            self.perturbation.update(self.xa_mean, model)
            for modid in self.ens_model:
                model = ctypes.cast(modid, ctypes.py_object).value
                model.update_gps(self.perturbation.extra)

    def model_output_files(self, store):
        """Reconstruct the reanalysis file
            Move the outputs from model workdir,
            - store:   reconstruct and store reanalysis
        """

        # Loop on models
        for modid in self.ens_model:
            self.model = modid
            Assim.model_output_files(self, store)

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
            fout.write('#Analysis information for restart written on {}\n'
                       .format(datetime.now().strftime('%d/%m/%Y %H:%M')).encode('utf-8'))
            fout.write('#---------------------------------------------------------------\n\n'.encode('utf-8'))
            fout.write('#Ensemble members:\n'.encode('utf-8'))
            fout.write('#   {}\n\n'.format(self.size).encode('utf-8'))
            fout.write('#Analysis:\n'.encode('utf-8'))
            if self.yo.dim == 0:
                fout.write('#No observation assimilated'.encode('utf-8'))
                return
            xa = self.ens_xb + self.xb_mean + self.ens_dx
            np.savetxt(fout, xa.array, fmt='%12.3f')
            fout.write('\n#Perturbations:\n'.encode('utf-8'))
            fout.write('#Seed:\n#   {}\n'.format(self.seed).encode('utf-8'))

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
        xa = Matrix(np.genfromtxt(filename))

        # Seed of the ensemble
        if self.seed == 'once':
            self.seed = False

        # Take the analysis into account
        if not self.seed:
            for m, modid in enumerate(self.ens_model):
                model = ctypes.cast(modid, ctypes.py_object).value
                model.control = self.control
                model.set_changes(bkg=xa[m, :], increment=Vector(dim=xa.shape[1]))
        
        # Update the perturbations
        self.xa_mean = xa.mean(axis=0)
        self.update()

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
                raise EnKFError(msg)

        # Subwindow:
        subwindow = ['{:02d}'.format(w) for w in subwindow]

        # Loop on subwindow
        ressub = []
        for sub in subwindow:
            res = {}
            # Loop on members
            for m in range(1, self.size+1):
                filename = '{}/{}/step{}/assim/increment_{}_memb{}.txt'.format(self.archdir, datedir,
                                                                               self.step, sub, m)

                # Open the file
                with open(filename, 'r') as fin:
                    data = fin.readlines()

                # Variable indices:
                var_ind = [i for v in varbs for i in range(len(data)) if data[i].split() and data[i].split()[0] == v]

                # Loop on variables:
                for v, iv in enumerate(var_ind):
                    var = data[iv].split()[0]
                    varasked = variable[v]
                    if var == varasked:
                        cln_ind = None
                    else:
                        cln_ind = self.parameter['composite'][var][0].index(varasked)
                    indvar = data[iv][len(var):-1].strip()
                    if varasked not in res:
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
                                raise EnKFError(msg)
                            if ind not in res[varasked]:
                                res[varasked][ind] = {}
                            if assim_t not in res[varasked][ind]:
                                res[varasked][ind][assim_t] = np.empty(0, dtype=np.float32)
                            if cln_ind is None:
                                r = np.reshape(np.array(data_tmp[cln * nbv: (cln+1) * nbv]), (1, nbv))
                            else:
                                r = np.reshape(np.array(data_tmp[cln * nbv + cln_ind]), (1, 1))
                            try:
                                res[varasked][ind][assim_t] = np.concatenate((res[varasked][ind][assim_t], r), axis=0)
                            except ValueError:
                                res[varasked][ind][assim_t] = r

            ressub.append(res)

        return ressub

    def __repr__(self):
        """Information"""

        string = 'Step {}\n'.format(self.step)
        string += '   scheme                  : {}\n'.format(self.scheme)
        string += '   variant                 : {}\n'.format(self.variant)
        string += '   smoother                : {}\n'.format(self.smoother)
        string += '   ensemble size           : {}\n'.format(self.size)
        string += '   configuration           : {}\n'.format(self.config)
        val, unit = sec2unit(self.spinup)
        string += '   spinup                  : {} {}\n'.format(val, unit)
        val, unit = sec2unit(self.subwindow)
        string += '   assimilation subwindow  : {} {}\n'.format(val, unit)
        return string
