"""
Mascaret
========

Hydraulic code 1.5D

"""

import logging
import json
from datetime import datetime, timedelta
import os
import shutil
import numpy as np
from copy import deepcopy
from .model import Model
from ..common.vector import Vector
from ..common.matrix import Matrix
from ..common.errors import MascaretError
from telapy.tools.studyMASC_UQ import MascaretStudy

# ======================================================


class Mascaret(Model):

    logger = logging.getLogger('Mascaret')
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
        It initialises the parametres a, b and c saving list
        e.g. self.control = {'Ks': [1,2,3], 'h': 'all', 'bc_abc': ['debit_tonneins','level_Adour']}
             self.ctl_length = 472  for a mesh of 463 points
             self.first_node = [0, 1, 2, 3, 466, 469, 472]
             self.bc_a = [1., 1.]
             self.bc_b = [0., 0.]
             self.bc_c = [0., 0.]
        """
        self.ctl_length = 0
        self.first_node = [0]

        if value == {} or self.postproc:
            self._control = None
        else:
            self._control = value
            dim = int(np.prod(self.shape))

            for var in self._control:
                if var in ['h', 'z', 'zb', 'q']:
                    self.ctl_length += dim                
                
                elif var == 'bc_abc':
                    for bc in self._control[var]:
                        typecode = self.model.bc_keep[bc].typecode
                        if not (typecode == 1 or typecode == 2):
                            msg1 = 'BC of type {} cannot be corrected'. \
                                format(self.model.self.model.bc_keep[bc].typeBC)
                            self.logger.error(msg1)
                            raise MascaretError(msg1)
                    self.ctl_length += 3 * len(self._control[var])
                    if len(self.bc_a) != len(self._control[var]):
                        self.bc_a = [1.] * len(self._control[var])
                        self.bc_b = [0.] * len(self._control[var])
                        self.bc_c = [0] * len(self._control[var])
                
                elif var == 'bc_gps':
                    for i, bc in enumerate(self._control[var]):
                        typecode = self.model.bc_keep[bc].typecode
                        if not (typecode == 1 or typecode == 2):
                            msg1 = 'BC of type {} cannot be corrected'.\
                                format(self.model.self.model.bc_keep[bc].typeBC)
                            self.logger.error(msg1)
                            raise MascaretError(msg1)
                        self.ctl_length += len(self.keep_gps[i])
                else:
                    self.ctl_length += len(self._control[var])
                self.first_node.append(self.ctl_length)

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
            member:       member id: 0 if no ensemble,
                                     from 1 to Ne if there is an ensemble
            start:        datetime start to carry on the experiment
            start0:       datetime original start of the experiment
            postproc:     instanciation for post-processing purposes
        """

        # Basic initialisation
        Model.__init__(self, config, prm, statdir, wdir, archdir, member, start, start0, postproc)
        self.name = 'Mascaret'              # Name of the model
        
        # Initialisation of specific attributes
        self.interpol = {}                  # Dictionary of interpolation information
        #                                     {model_coord_1: { 'ind1': (index, weight),
        #                                     'ind2': (index, weight)}}
        self.state0 = None                  # Dictionary of specific configuration for the run
        self.persist = False                # Persistence for forecast on going (bool)
        self.saved_state = None             # Id of the saved state
        self.saved_overlap = None           # Id of the saved state for overlapping windows
                
        # Post processing attributes
        if self.postproc:
            self.start_line = 0        # Starting line for extraction
            self.var_ind = None        # Indices for extracting variables from output file
            self.tim_ind = None        # Indices for extracting time steps from output file
            self.loc_ind = None        # Indices for extracting location from output file

        # No post processing
        else:

            # Carry on experiment
            if start is not None and start0 is not None:
                otherfiles = ['xcas', 'loi', 'geo']
                if self.member == 0:
                    filename = '{}/restart/{}_{}'.format(self.archdir, start.strftime("%Y%m%d-%H%M"),
                                                         self.files['lig'])
                    if not os.path.exists(filename):
                        filename = '{}/restart/{}_{}_memb1.lig'.format(self.archdir, start.strftime("%Y%m%d-%H%M"),
                                                                       self.files['lig'].split('.')[0])
                else:
                    filename = '{}/restart/{}_{}_memb{}.lig'.format(self.archdir, start.strftime("%Y%m%d-%H%M"),
                                                                    self.files['lig'].split('.')[0], self.member)
                try:
                    shutil.copyfile(filename, os.path.join(self.wdir, self.files['lig']))
                except IOError as err:
                    msg1 = 'Cannot copy file:\n{}'.format(err)
                    self.logger.error(msg1)
                    raise MascaretError(msg1)
            else:
                otherfiles = ['lig', 'xcas', 'loi', 'geo']

            # Copy required files in the working directory and archiving directory
            dirname = '{}/init'.format(self.archdir)
            for typ in otherfiles:
                if isinstance(self.files[typ], list):
                    for file in self.files[typ]:
                        try:
                            shutil.copyfile(os.path.join(self.statdir, file),
                                            os.path.join(self.wdir, file))
                            shutil.copyfile(os.path.join(self.statdir, file),
                                            os.path.join(dirname, file))
                        except IOError as err:
                            msg1 = 'Cannot copy file:\n{}'.format(err)
                            self.logger.error(msg1)
                            raise MascaretError(msg1)
    
                else:
                    try:
                        shutil.copyfile(os.path.join(self.statdir, self.files[typ]),
                                        os.path.join(self.wdir, self.files[typ]))
                        shutil.copyfile(os.path.join(self.statdir, self.files[typ]),
                                        os.path.join(dirname, self.files[typ]))
                    except IOError as err:
                        msg1 = 'Cannot copy file:\n{}'.format(err)
                        self.logger.error(msg1)
                        raise MascaretError(msg1)

            # Copy damocle file if it exists
            try:
                shutil.copyfile(os.path.join(self.statdir, self.files['damocle']),
                                os.path.join(self.wdir, self.files['damocle']))
                shutil.copyfile(os.path.join(self.statdir, self.files['damocle']),
                                os.path.join(dirname, self.files['damocle']))
            except IOError:
                self.logger.warning('No file damocle.')
                del(self.files['damocle'])
        
            # Instanciate Mascaret
            if self.member > 0:
                memb = '_memb{}'.format(self.member)
            else:
                memb = ''        
            workdir = 'study{}'.format(memb)
            self.model = MascaretStudy(self.config, log_lvl='INFO', iprint=1, working_directory=workdir)
            
            # Update public and model-like attributes
            self.shape = (self.model.model_size,)   # Dimensions of the model (tuple)
            self.set_time(start=self.start)         # Date attributes
            self.step = self.model.time_step        # Time step of the model (float)
            self.outdir = '{}/study{}/output'.format(self.wdir, memb)    # Output files directory
            self.figdir = '{}/study{}/figures'.format(self.wdir, memb)   # Output figures directory
    
            # Initialisation of specific attributes            
            self.bc_chronicle_svg = {}                # Dictionary containing the saved chronicles  
            #                                           for the boundary conditions. Updated before persistence
            self.bc_a = [1.]                          # homothetic vertical transformation of the boundary 
            #                                           chronicle. Updated in self.control
            self.bc_b = [0.]                          # amplitude shift of the boundary chronicle
            #                                           Updated in self.control
            self.bc_c = [0]                           # time shift in seconds of the forcing chronicle
            #                                           Updated in self.control
            # If carry on experiment, update boundaries if required
            try:
                filename = '{}/restart/{}_assim_model.txt'.format(self.archdir, start.strftime("%Y%m%d-%H%M"))
                with open(filename, 'r') as fin:
                    data = fin.readlines()
                    for i, d in enumerate(data):
                        if d[:6] == 'bc_gps':
                            bclist = [s[1:-1] for s in d[9:-2].split(',')]
                            for j, bc_id in enumerate(bclist):
                                chronicle = [float(s) for s in data[i + 1 + j].split()[1:] if s != '']
                                if len(chronicle) == self.model.bc_keep[bc_id].size_bc:
                                    self.model.bc_keep[bc_id].value = chronicle
                                else:
                                    shift = chronicle[-1] - self.model.bc_keep[bc_id].value[len(chronicle) - 1]
                                    self.model.bc_keep[bc_id].value[:len(chronicle)] = chronicle
                                    self.model.bc_keep[bc_id].value[len(chronicle):] += shift
                                self.model.change_boundary_condition({'name': bc_id, 'multcoeff': 1.})
            except (AttributeError, IOError):
                pass

    def read_config(self):
        """Read the configuration file"""

        with open(self.config, 'r') as fin:
            try:
                # json file
                data = json.load(fin, encoding='utf-8')
                self.conf = data
                self.files = data['files']
            except IOError as err:
                msgs = 'The configuration file cannot be read:\n{}'.format(err)
                self.logger.error(msgs)
                raise MascaretError(msgs)

    def set_time(self, dateref=None, length=None, start=None):
        """Define time of the run
            - dateref: datetime of the start
            - length:  length of the run in seconds
            - start:   initial time
        """
        
        if dateref is None:
            dateref = self.datestart
        if start is None:
            start = self.model.initial_time
        if length is None:
            length = self.model.final_time - start
        
        Model.set_time(self, dateref, length, start)

    def copy(self, members=None):
        """Create new model instances with the same characteristics
            - members: list of member id
        """

        if members is None:
            members = [1]

        listmodels = []                # list of model instances
        
        # Save the current state
        state = self.model.masc.save_state()

        # Loop on models
        for m in members:
            self.logger.info('Instanciate member {}'.format(m))
            # instanciate new member
            new_instance = Mascaret(self.config, self.prm, self.statdir, self.wdir, self.archdir, m)
            # Copy the state
            new_instance.model.masc.set_state(state, 0, new_instance.model.masc.id_masc)   
            new_instance.state0 = {}     
            # keep_gps must be copied
            new_instance.keep_gps = deepcopy(self.keep_gps)
            # control and interpol must have the same id for both models
            new_instance.control = self.control
            new_instance.interpol = self.interpol
            # Set time
            new_instance.set_time(self.datestart, self.length, self.start)
            # Append the new instance
            listmodels.append(new_instance)
            
        # Delete the saved state
        self.model.masc.free_saved_state(state)
        
        return listmodels

    def get_gps_axis(self):
        """Return a dictionary with the axis for the GP sampler perturbations"""
        
        boundary = {}
        for bc in self.model.bc_keep:
            boundary[bc] = self.model.bc_keep[bc].taxis
        return boundary

    def __call__(self, dateref=None, length=None, dumptime=None,
                 file=None, overlap=0):
        """Run the model
            - dateref:  datetime of the start
            - start:       start in seconds of the cycle
            - length:   length of the run in seconds
            - dumptime: list of time to output
            - file:     specific file name for logging
            - overlap:  time to output for overlapping windows
         """
        
        # Set the times for the run
        self.set_time(dateref, length, self.start)
        
        # Reinitialisation flag
        flag = True

        # Initialise state 
        if self.state0 is not None:
            if 'saved_state' in self.state0:
                self.logger.debug('Initialisation from saved state {} for model {}.'
                                  .format(self.state0['saved_state'], self.member))
                self.model.masc.set_state(self.state0['saved_state'], 1)
                del self.state0['saved_state']
            elif 'initial_conditions' in self.state0:
                if 'q' in self.state0['initial_conditions'] and \
                   'z' in self.state0['initial_conditions']:
                    self.logger.debug('Initialisation from given z and q.')
                    self.model.initialize_model(self.state0['initial_conditions']['z'],
                                                self.state0['initial_conditions']['q'])
                del self.state0['initial_conditions']
            else:
                self.logger.debug('No initialisation, carry on for model {}.'.format(self.member))
        else:
            self.logger.debug('Initialisation from restart file for model {}.'.format(self.member))
            self.model.initialize_model()
            # No need to reinitialise SimulPhase, it is done in initialize_model()
            flag = False
        
        # Reset the Simulation Phase to INITIALISATION
        if flag:
            self.model.masc.set('State.SimulPhase', 1)
        
        # Take into account possible changes from assimilation
        self.init_changes()

        # Run the model
        if length > 0:
            # Take into account possible overlap
            if overlap != 0:
                if dumptime is None:
                    dumptime = [self.stop-overlap]
                else:
                    dumptime.append(self.stop-overlap)
                    dumptime.sort()

            # Handle the output files
            if file is not None:
                if os.path.exists('{}/{}.lis'.format(self.outdir, file)):
                    os.symlink('{}/{}.lis'.format(self.outdir, file),
                               os.path.join(self.outdir, self.files['listing']))
                if os.path.exists('{}/{}.opt'.format(self.outdir, file)):
                    os.symlink('{}/{}.opt'.format(self.outdir, file),
                               os.path.join(self.outdir, self.files['res']))

            # Run the model
            self.logger.debug('Running from {} to {}.'.format(self.start, self.stop))
            if self.state0 is None or self.state0 == {}:
                self.model(dump_state=dumptime, tstart=self.start, tend=self.stop, flag=None)
            else:
                self.model(x=self.state0, dump_state=dumptime, tstart=self.start, 
                           tend=self.stop, flag=None)
            self.state0 = {}
            
            # Store the possible overlap
            if overlap != 0:
                self.saved_overlap = self.model.dump_index[dumptime.index(self.stop-overlap)]
                self.model.dump_index.remove(self.saved_overlap)
                self.logger.debug('State (sliding windows) saved as {} for model {}.'.
                                  format(self.saved_overlap, self.member))

            # Handle the output files
            if file is not None:
                if not os.path.exists('{}/{}.lis'.format(self.outdir, file)):
                    shutil.copyfile(os.path.join(self.outdir, self.files['listing']),
                                    '{}/{}.lis'.format(self.outdir, file))
                os.remove(os.path.join(self.outdir, self.files['listing']))
                if not os.path.exists('{}/{}.opt'.format(self.outdir, file)):
                    shutil.copyfile(os.path.join(self.outdir, self.files['res']),
                                    '{}/{}.opt'.format(self.outdir, file))
                os.remove(os.path.join(self.outdir, self.files['res']))

    def init_changes(self):
        """Initialise the changes"""
        
        if self.state_change is not None:

            if 'h' in self.state_change or 'z' in self.state_change or 'q' in self.state_change:
                # State variable
                if 'h' in self.state_change:
                    z = self.state_change['h']['value']
                    if self.state_change['h']['inc']:
                        z += np.array(self.model.global_elevation)
                    else:
                        z += np.array(self.model.global_bathymetry)
                elif 'z' in self.state_change:
                    z = self.state_change['z']['value']
                    if self.state_change['z']['inc']:
                        z += np.array(self.model.global_elevation)
                else:
                    z = np.array(self.model.global_elevation)
                if 'q' in self.state_change:
                    q = self.state_change['q']['value']
                    if self.state_change['q']['inc']:
                        q += np.array(self.model.global_discharge)
                else:
                    q = np.array(self.model.global_discharge)
                self.model.initialize_model(z, q)

            for var in self.state_change:
                if var in ['h', 'z', 'q']:
                    continue
                
                elif var == 'Ksmin':
                    # Friction coefficient for minor
                    for change in self.state_change['Ksmin']:
                        if change['inc']:
                            change['value'] += self.model.get_zone_friction_minor(change['index'])[0]
                        self.model.set_zone_friction_minor(change)
                
                elif var == 'Ksmaj':
                    # Friction coefficient for major
                    for change in self.state_change['Ksmaj']:
                        if change['inc']:
                            change['value'] += self.model.get_zone_friction_major(change['index'])[0]
                        self.model.set_zone_friction_major(change)
                
                elif var == 'bc_cst':
                    # Constant boundary condition
                    for change in self.state_change['bc_cst']:
                        if change['inc']:
                            change['value'] += self.model.bc_keep[change['index']].value[0]
                        bc = {'name': change['index'], 'value': change['value']}
                        self.model.change_boundary_condition(bc)
                        
                elif var == 'bc_abc':
                    # Boundary chronicle with a, b, c
                    for change in self.state_change[var]:
                        bc = {'name': change['index']}
                        if change['index'] in self.control[var]:
                            i = self.control[var].index(change['index'])
                            if change['inc']:
                                self.bc_a[i] += change['value'][0]
                                self.bc_b[i] += change['value'][1]
                                self.bc_c[i] += change['value'][2]
                            else:
                                self.bc_a[i] = change['value'][0]
                                self.bc_b[i] = change['value'][1]
                                self.bc_c[i] = change['value'][2]
                            if self.bc_a[i] != 1.:
                                bc['multcoeff'] = self.bc_a[i]
                            if self.bc_b[i] != 0.:
                                try:
                                    # Python 2.7
                                    bc['addperturb'] = [self.bc_b[i]]*self.model.bc_keep[change['index']].sizeBC
                                except AttributeError:
                                    # Python 3
                                    bc['addperturb'] = [self.bc_b[i]]*self.model.bc_keep[change['index']].size_bc
                            if self.bc_c[i] != 0.:
                                bc['shift_chronicle'] = self.bc_c[i]
                        else:
                            if change['value'][0] != 1.:
                                bc['multcoeff'] = change['value'][0]
                            if change['value'][1] != 0.:
                                try:
                                    # Python 2.7
                                    bc['addperturb'] = [change['value'][1]] * \
                                                       self.model.bc_keep[change['index']].sizeBC
                                except AttributeError:
                                    # Python 3
                                    bc['addperturb'] = [change['value'][1]] * \
                                                       self.model.bc_keep[change['index']].size_bc
                            if change['value'][2] != 0:
                                bc['shift_chronicle'] = change['value'][2]
                        self.model.change_boundary_condition(bc)                 

                elif var == 'bc_gps':
                    # Boundary chronicle with gaussian process perturbations
                    for change in self.state_change[var]:
                        try:
                            i = self.control[var].index(change['index'])
                        except KeyError:
                            pass
                        else:
                            if change['inc']:
                                for j in range(len(self.keep_gps[i])):
                                    self.keep_gps[i][j] += change['control'][j]
                            else:
                                self.keep_gps[i] = change['control']
                        bc = {'name': change['index'], 'addperturb': change['value']}
                        self.model.change_boundary_condition(bc)

            self.state_change = None
               
    def convert_coord(self, coord, model_coord):
        """Convert observtion coordinates into coordinates understandable by the model
           Define the interpolation parameters
            - coord:  dictionary { 'spatial': {coord_type1: [], coord_type2: []},
                                   'time': [datetime] }
                       eg. {'spatial': {('lat','lon'): [(45.,200.)],
                                        ('s',): [36500., 45000.]},
                            'time': [datetime(2018,4,16,0,0,0]}
            - model_coord: dictionary {'spatial': {},
                                       'time': [1800.]}
        """
        
        # Loop on coordinate type
        for ctype in coord['spatial']:
            
            if ctype not in model_coord['spatial']:
                model_coord['spatial'][ctype] = []

            if ctype == ('s',):
                # Curvilinear abscissa
                model_coord['spatial'][('s',)] = coord['spatial'][('s',)]
            
            elif ctype == ('lat', 'lon'):
                # Latitude, Longitude
                latlon = np.genfromtxt('{}/conv_latlon.out'.format(self.statdir))
                dim = latlon.shape[0]
                for c in coord['spatial'][('lat', 'lon')]:
                    lono = c[1]
                    if lono > 180.:
                        lono -= 360.
                    ind0 = ((latlon[:, 1] - lono) ** 2 + (latlon[:, 2] - c[0]) ** 2).argmin()
                    latlon2 = np.zeros((dim - 1, 3))
                    latlon2[:ind0, :] = latlon[:ind0, :]
                    if ind0 < dim - 1:
                        latlon2[ind0:, :] = latlon[ind0+1:, :]
                    ind1 = ((latlon2[:, 1] - lono) ** 2 + (latlon2[:, 2] - c[0]) ** 2).argmin()
                    if ind1 >= ind0:
                        ind1 += 1
                    if np.sign(latlon[ind0, 1] - lono) == np.sign(latlon[ind1, 1] - lono) and \
                            np.sign(latlon[ind0, 2] - c[0]) == np.sign(latlon[ind1, 2] - c[0]):
                        cm = latlon[ind0, 0] + np.sign(ind1 - ind0)
                        model_coord['spatial'][('lat', 'lon')].append((cm,))
                    else:
                        d0 = np.sqrt((latlon[ind0, 1] - lono) ** 2 + (latlon[ind0, 2] - c[0]) ** 2)
                        d1 = np.sqrt((latlon[ind1, 1] - lono) ** 2 + (latlon[ind1, 2] - c[0]) ** 2)
                        cm = latlon[ind0, 0] + d0 * (latlon[ind1, 0] - latlon[ind0, 0]) / (d0 + d1)
                        model_coord['spatial'][('lat', 'lon')].append((cm,))

            elif ctype == ('other',):
                # Other type should be converted into curvilinear abscissa
                pass
            
            else:
                msg1 = 'Coordinate {} not yet taken into account'.format(ctype)
                self.logger.error(msg1)
                raise MascaretError(msg1)

        # Find the indices and weight for interpolation
        # Beware self.interpol must not change id for ensemble assimilation
        list_curv = [v[0] for val in model_coord['spatial'].values() for v in val]
        interpol = self.model.local_interpolation(list_curv)
        for key in interpol:
            self.interpol[key] = interpol[key]

        # Define time at the next multiple of model time step
        for t, tsec in enumerate(model_coord['time']):
            # Multiple of model time step
            tts = int(tsec / int(self.step)) * int(self.step)
            if tsec % int(self.step) > 0:
                tts += int(self.step)
            tts += self.start
            model_coord['time'][t] = tts
    
    def get_coord_limits(self):
        """Return the limits of the domain"""

        return [(self.model.curvilinear_abscissa[0],), (self.model.curvilinear_abscissa[-1],)]

    def get_Mxb_Hxb(self, datestart, length, file, dumptime, xb_start, obsinfo, pickle=False):
        """Return the background state of the control variables
            at the different time following dumptime and its
            counterpart in observation space
            - datestart:   datetime of the start of the run
            - start:       start in seconds of the cycle
            - length:      length of the run
            - file:        logging results in a specific file
            - dumptime:    list of time to dump
            - xb_start:    get xb at the start (end) of the run (bool)
            - obsinfo:     dictionary of observation information
            - pickle:      save and return state at the end of the length
        """

        # Initialisation
        xb = None
        Mxb = []
        Hxb = []

        # Get xb at the start of the run
        if xb_start:
            self.init_changes()
            xb = self.control_vector()

        # Run the model
        self(dateref=datestart, length=length, dumptime=dumptime, file=file)

        # Get xb at the end of the run
        if not xb_start and dumptime[-1] < self.stop:
            xb = self.control_vector()

        # Start and stop indices for observations
        obslist = [i for i in range(len(obsinfo['time'])) if obsinfo['time'][i] in dumptime]
        
        # Loop on time
        for cnt, t in enumerate(dumptime):

            # Restore the state
            self.model.masc.set_state(self.model.dump_index[cnt], 1)
            
            # Control vector
            Mxb.append(self.control_vector())
            
            # Apply H
            indlist = [i for i in obslist if obsinfo['time'][i] == t]
            Hxb.extend(self.apply_Hnolin(obsinfo, indlist[0], indlist[-1]+1).array)
                                                               
        # Get xb at the end of the run
        if not xb_start and dumptime[-1] == self.stop:
            xb = Mxb[-1]

        # Save the state at the end of the window
        if pickle:
            gherkins = self.pickle()
        else:
            gherkins = []

        return Vector(xb), Vector(Mxb), Vector(Hxb), gherkins

    def control_vector(self):
        """Construct the control vector"""
        
        ctl = np.zeros(self.ctl_length)
        for i, v in enumerate(self.control):
            ind0 = self.first_node[i]
            ind1 = self.first_node[i+1]
            if v == 'h':
                ctl[ind0:ind1] = self.model.global_height
            elif v == 'z':
                ctl[ind0:ind1] = self.model.global_elevation
            elif v == 'q':
                ctl[ind0:ind1] = self.model.global_discharge
            elif v == 'zb':
                ctl[ind0:ind1] = self.model.global_bathymetry
            elif v == 'Ksmin':
                for j, zone in enumerate(self.control['Ksmin']):
                    ctl[ind0+j] = self.model.get_zone_friction_minor(zone-1)[0]
            elif v == 'Ksmaj':
                for j, zone in enumerate(self.control['Ksmaj']):
                    ctl[ind0+j] = self.model.get_zone_friction_major(zone-1)[0]
            elif v == 'bc_cst':
                for j, name in enumerate(self.control[v]):
                    ctl[ind0+j] = self.model.bc[name].value[0]
            elif v == 'bc_abc':
                for j in range(len(self.control[v])):
                    ctl[ind0+3*j] = self.bc_a[j]
                    ctl[ind0+3*j+1] = self.bc_b[j]
                    ctl[ind0+3*j+2] = self.bc_c[j]
            elif v == 'bc_gps':
                ctl[ind0:ind1] = [x for sublist in self.keep_gps for x in sublist]
        return ctl

    def interpolate(self, vectm, coordlist):
        """Interpolate vector in other space
            - vectm:     vector or list of values in model space
            - coordlist:  List of coordinates
        """

        vecto = np.zeros(len(coordlist))
        
        # Loop on list
        for i, c in enumerate(coordlist):
            inda = self.interpol[c]['ind1'][0]
            indb = self.interpol[c]['ind2'][0]
            hia = self.interpol[c]['ind1'][1]
            hib = self.interpol[c]['ind2'][1]
            vecto[i] = vectm[inda] * hia + vectm[indb] * hib            
            
        return vecto

    def apply_Hnolin(self, coords, ist, iend):
        """Return the vector in observation space
            Non-linear version of H
            - coords:      dictionary of coordinates after self.convert_coord()
            - ist:         first index to take into account
            - iend:        last index to take into account
        """
                        
        # Initialisation
        Hv = np.zeros(iend - ist)
        scoord = np.array(coords['scoord'])[:, 0]
                
        # Loop on observation type
        listtype = set(coords['obs_type'])
        for obs in listtype:
            
            # Define observation elements for this variable
            indlist = [i for i in range(ist, iend) if coords['obs_type'][i] == obs]
            hvlist = list(np.array(indlist)-ist)
            
            if obs == 'h':
                # Observation of water height                
                v = self.model.global_height
                Hv[hvlist] = self.interpolate(v, scoord[indlist])
                        
            elif obs == 'z':
                # Observation of water elevation
                v = self.model.global_elevation
                Hv[hvlist] = self.interpolate(v, scoord[indlist])
            
            elif obs == 'zb':
                # Observation of bathymetry
                v = self.model.bathymetry
                Hv[hvlist] = self.interpolate(v, scoord[indlist])
        
            elif obs == 'q':
                # Observation of discharge
                v = self.model.global_discharge
                Hv[hvlist] = self.interpolate(v, scoord[indlist])
            
            else:
                msg1 = 'Non-linear H cannot be applied for observation type {}'.format(obs)
                self.logger.error(msg1)
                raise MascaretError(msg1)
                
        return Vector(Hv)

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
                        
        # Initialisation
        H = np.zeros((iend-ist, self.ctl_length))
        scoord = np.array(coords['scoord'])[:, 0]

        # Simple interpolation   
        ind = []       
        for v, var in enumerate(self.control):
            ind0 = self.first_node[v]
            ind1 = self.first_node[v+1]
            if var in ['h', 'z', 'zb', 'q']:
                for j in range(iend-ist):
                    inda = self.interpol[scoord[j+ist]]['ind1'][0]
                    indb = self.interpol[scoord[j+ist]]['ind2'][0]
                    hia = self.interpol[scoord[j+ist]]['ind1'][1]
                    hib = self.interpol[scoord[j+ist]]['ind2'][1]
                    for _ in range(ist, iend):
                        H[j, inda+ind0] = hia
                        H[j, indb+ind0] = hib
            else:
                ind.extend(range(ind0, ind1))
        
        # Surrogate H
        if xb is not None and Hxb is not None:
            for j in range(iend-ist):
                try:
                    H[j, ind] = np.linalg.solve(xb[:len(ind), ind].array, Hxb[:len(ind), j].array)
                except np.linalg.LinAlgError:
                    self.logger.warning('Surrogate H cannot be computed.')
                    continue
                   
        return Matrix(H)

    def check_increment(self, bkg, increment):
        """Check the correctness of the increment
            - bkg:       background state
            - increment: increment to be added to the background state
        """
        
        # Initialisation
        analysis = bkg + increment
        new_increment = Vector(increment.array)
        
        for v, var in enumerate(self.control):
            ind0 = self.first_node[v]
            ind1 = self.first_node[v+1]
                        
            if var == 'Ksmin' or var == 'Ksmaj':
                # Friction coefficient
                for i, anl in enumerate(analysis[ind0:ind1].array):
                    # Check min Ks
                    if anl < self.parameter['limitations']['Ks_mini'][i]:
                        new_increment[ind0+i] = self.parameter['limitations']['Ks_mini'][i] - bkg[ind0+i]
                    # Check max Ks
                    elif anl > self.parameter['limitations']['Ks_maxi'][i]:
                        new_increment[ind0+i] = self.parameter['limitations']['Ks_maxi'][i] - bkg[ind0+i]
            
            elif var == 'bc_cst':
                # Constant boundary condition
                for i, anl in enumerate(analysis[ind0:ind1].array):
                    typecode = self.model.bc_keep[self.control[var][i]].typecode
                    if typecode == 1:
                        # Check min discharge
                        if anl < self.parameter['limitations']['bc_Q_mini']:
                            new_increment[ind0+i] = self.parameter['limitations']['bc_Q_mini'] - bkg[ind0+i]
                        # Check max_discharge
                        elif anl > self.parameter['limitations']['bc_Q_maxi']:
                            new_increment[ind0+i] = self.parameter['limitations']['bc_Q_maxi'] - bkg[ind0+i]
                    elif typecode == 2:
                        # Check min level
                        if anl < self.parameter['limitations']['bc_H_mini']:
                            new_increment[ind0+i] = self.parameter['limitations']['bc_H_mini'] - bkg[ind0+i]
                        # Check max level
                        elif anl > self.parameter['limitations']['bc_H_maxi']:
                            new_increment[ind0+i] = self.parameter['limitations']['bc_H_maxi'] - bkg[ind0+i]
            
            elif var == 'bc_abc':
                # Boundary chronicle
                for i, anl in enumerate([analysis[j:j+3].array for j in range(ind0, ind1, 3)]):
                    # Check min homothetic transformation
                    if anl[0] < self.parameter['limitations']['bc_a_mini']:
                        new_increment[ind0+3*i] = self.parameter['limitations']['bc_a_mini'] - bkg[ind0+3*i]
                        anl = (bkg[ind0+3*i:ind0+3*i+3] + new_increment[ind0+3*i:ind0+3*i+3]).array
                    chronicle = self.model.bc_keep[self.control[var][i]]
                    bc_org = chronicle.value  
                    bc = anl[0] * bc_org
                    if chronicle.typecode == 1:
                        # Check min discharge
                        if np.min(bc) < self.parameter['limitations']['bc_Q_mini']:
                            new_increment[ind0+3*i] = self.parameter['limitations']['bc_Q_mini']\
                                                      - increment[ind0+3*i]*np.min(bc)
                            anl[0] = (bkg[ind0+3*i] * new_increment[ind0+3*i]).array
                        # Check max discharge
                        if np.max(bc) > self.parameter['limitations']['bc_Q_maxi']:
                            new_increment[ind0+3*i] = self.parameter['limitations']['bc_Q_maxi'] \
                                                      - increment[ind0+3*i]*np.max(bc)
                            anl[0] = (bkg[ind0+3*i] * new_increment[ind0+3*i]).array  
                        bc = anl[0] * bc_org + anl[1]
                        # Check min discharge
                        if np.min(bc) < self.parameter['limitations']['bc_Q_mini']:
                            new_increment[ind0+3*i+1] = self.parameter['limitations']['bc_Q_mini'] - np.min(bc)
                        # Check max discharge
                        if np.max(bc) > self.parameter['limitations']['bc_Q_maxi']:
                            new_increment[ind0+3*i+1] = self.parameter['limitations']['bc_Q_maxi'] - np.max(bc)
                    elif chronicle.typecode == 2:
                        # Check min level
                        if np.min(bc) < self.parameter['limitations']['bc_H_mini']:
                            new_increment[ind0+3*i] = self.parameter['limitations']['bc_H_mini'] \
                                                      - increment[ind0+3*i]*np.min(bc)
                            anl[0] = (bkg[ind0+3*i] * new_increment[ind0+3*i]).array
                        # Check max level
                        if np.max(bc) > self.parameter['limitations']['bc_H_maxi']:
                            new_increment[ind0+3*i] = self.parameter['limitations']['bc_H_maxi'] \
                                                      - increment[ind0+3*i]*np.max(bc)
                            anl[0] = (bkg[ind0+3*i] * new_increment[ind0+3*i]).array                        
                        bc = anl[0] * bc_org + anl[1]
                        # Check min level
                        if np.min(bc) < self.parameter['limitations']['bc_H_mini']:
                            new_increment[ind0+3*i+1] = self.parameter['limitations']['bc_Q_mini'] - np.min(bc)
                        # Check max level
                        if np.max(bc) > self.parameter['limitations']['bc_H_maxi']:
                            new_increment[ind0+3*i+1] = self.parameter['limitations']['bc_Q_maxi'] - np.max(bc)
        
        if not np.all(new_increment == increment):
            self.logger.warning('check increment: the increment has been modified.')
        
        return new_increment        
        
    def check_range(self, var, therange, index=None):
        """Check if a range of values is consistent for a variable
            - var:       name of variable
            - therange:  range to check [min,max]
            - index:     index of the variable for BC
        """
        
        vmin = therange[0]
        vmax = therange[1]
        rg = vmax - vmin
        
        if var == 'Ksmin' or var == 'Ksmaj':
            if vmin < self.parameter['limitations']['Ks_mini'][index]:
                vmin = self.parameter['limitations']['Ks_mini'][index]
                vmax = vmin + rg
            elif vmax > self.parameter['limitations']['Ks_maxi'][index]:
                vmax = self.parameter['limitations']['Ks_maxi'][index]
                vmin = vmax - rg
        
        elif var == 'bc_cst':
            typecode = self.model.bc_keep[index].typecode
            if typecode == 1:
                if vmin < self.parameter['limitations']['bc_Q_mini']:
                    vmin = self.parameter['limitations']['bc_Q_mini']
                    vmax = vmin + rg
                elif vmax > self.parameter['limitations']['bc_Q_maxi']:
                    vmax = self.parameter['limitations']['bc_Q_maxi']
                    vmin = vmax - rg
            elif typecode == 2:
                if vmin < self.parameter['limitations']['bc_H_mini']:
                    vmin = self.parameter['limitations']['bc_H_mini']
                    vmax = vmin + rg
                elif vmax > self.parameter['limitations']['bc_H_maxi']:
                    vmax = self.parameter['limitations']['bc_H_maxi']
                    vmin = vmax - rg
        
        elif var == 'bc_a':
            if vmin < self.parameter['limitations']['bc_a_mini']:
                vmin = self.parameter['limitations']['bc_a_mini']
                vmax = vmin + rg
            
        return [vmin, vmax]

    def set_changes(self, bkg=None, increment=None, state=None, values=None, extra=None):
        """Set the changes to take into account for the next run
            - bkg:       background state
            - increment: increment to be added to the background state
            - state:     list of dictionary of changes
            - values:    list of values for changes
            - extra:     list of extra values for changes
        """

        flags = []

        # Take corrections from increment
        if increment is not None:
            self.state_change = {}
            for v, var in enumerate(self.control):
                ind0 = self.first_node[v]
                ind1 = self.first_node[v+1]
                
                if var in ['h', 'z', 'q']:
                    # State variable
                    if bkg is None:
                        self.state_change[var] = {'value': increment[ind0:ind1].array, 'inc': True}
                    else:
                        self.state_change[var] = {'value': (bkg[ind0:ind1]+increment[ind0:ind1]).array, 'inc': False}           
                
                elif var == 'Ksmin' or var == 'Ksmaj':
                    # Friction coefficient
                    self.state_change[var] = []
                    if bkg is None:
                        for i, zone in enumerate(self.control[var]):
                            self.state_change[var].append({'index': zone-1, 'inc': True,
                                                           'value': increment[ind0 + i].array, })
                    else:
                        for i, zone in enumerate(self.control[var]):
                            self.state_change[var].append({'index': zone-1, 'inc': False,
                                                           'value': (bkg[ind0+i]+increment[ind0+i]).array})
                elif var == 'bc_cst':
                    # Constant boundary condition
                    self.state_change[var] = []
                    if bkg is None:
                        for i, index in enumerate(self.control[var]):
                            self.state_change[var].append({'index': index, 'inc': True, 
                                                           'value': increment[ind0+i].array})
                    else:
                        for i, index in enumerate(self.control[var]):
                            self.state_change[var].append({'index': index, 'inc': False,
                                                           'value': (increment[ind0+i]+bkg[ind0+i]).array})
                elif var == 'bc_abc':
                    # Boundary condition chronicle moved with a, b, c 
                    self.state_change[var] = []
                    if bkg is None:
                        for i, index in enumerate(self.control[var]):
                            self.state_change[var].append({'index': index, 'inc': True,
                                                           'value': [increment[ind0+3*i].array,
                                                                     increment[ind0+3*i+1].array,
                                                                     increment[ind0+3*i+2].array]})
                    else:
                        for i, index in enumerate(self.control[var]):
                            self.state_change[var].append({'index': index, 'inc': False,
                                                           'value': [(increment[ind0+3*i]+bkg[ind0+3*i]).array,
                                                                     (increment[ind0+3*i+1]+bkg[ind0+3*i+1]).array,
                                                                     (increment[ind0+3*i+2]+bkg[ind0+3*i+2]).array]})
                
                elif var == 'bc_gps':
                    # Boundary chronicle with gaussian process perturbation
                    self.state_change[var] = []
                    st = ind0
                    end = ind0
                    if bkg is None:
                        for i, index in enumerate(self.control[var]):
                            end += len(self.keep_gps[i])
                            self.state_change[var].append({'index': index, 'value': extra[v], 
                                                           'inc': True, 'control': increment[st:end].array})
                            st = end
                    else:
                        for i, index in enumerate(self.control[var]):
                            end += len(self.keep_gps[i])
                            self.state_change[var].append({'index': index, 'value': extra[i], 'inc': False,
                                                           'control': (increment[st:end]+bkg[st:end]).array})
                            st = end
                        
        # Take corrections from state
        if state is not None and values is not None:    
            if self.state_change is None:
                self.state_change = {}
            for v, dico in enumerate(state):
                
                if dico['variable'] in ['h', 'z', 'q']:
                    if list(set(values[v])) != [0.]:
                        self.state_change[dico['variable']] = values[v]                         
                         
                elif dico['variable'] == 'Ksmin' or dico['variable'] == 'Ksmaj':  
                    # Friction coefficient
                    if dico['variable'] not in self.state_change:
                        self.state_change[dico['variable']] = []   
                    val = values[v]
                    if val < self.parameter['limitations']['Ks_mini'][dico['zone']-1]:
                        val = self.parameter['limitations']['Ks_mini'][dico['zone']-1]
                    elif val > self.parameter['limitations']['Ks_maxi'][dico['zone']-1]:
                        val = self.parameter['limitations']['Ks_maxi'][dico['zone']-1]
                    self.state_change[dico['variable']].append({'index': dico['zone']-1, 'value': val, 'inc': False})                                                                        
                
                elif dico['variable'] == 'bc_cst':
                    # Constant boundary condition
                    if 'bc_cst' not in self.state_change:
                        self.state_change['bc_cst'] = [] 
                    val = values[v]
                    typecode = self.model.bc_keep[dico['index']].typecode 
                    if typecode == 1:
                        # Check discharge
                        if val < self.parameter['limitations']['bc_Q_mini']:
                            val = self.parameter['limitations']['bc_Q_mini']
                        elif val > self.parameter['limitations']['bc_Q_maxi']:
                            val = self.parameter['limitations']['bc_Q_maxi']
                    elif typecode == 2:
                        # Check level
                        if val < self.parameter['limitations']['bc_H_mini']:
                            val = self.parameter['limitations']['bc_H_mini']
                        elif val > self.parameter['limitations']['bc_H_maxi']:
                            val = self.parameter['limitations']['bc_H_maxi']
                    self.state_change['bc_cst'].append({'index': dico['index'], 'value': val, 'inc': False})
                
                elif dico['variable'] == 'bc_a' or dico['variable'] == 'bc_b' or dico['variable'] == 'bc_c':  
                    # Boundary chronicle moved with a, b, c 
                    if 'bc_abc' not in self.state_change:
                        self.state_change['bc_abc'] = [{'index': dico['index'],  
                                                        'value': [1., 0., 0], 'inc': False}]
                        ind = 0                            
                    else:
                        ind = len(self.state_change['bc_abc'])
                        for i, change in enumerate(self.state_change['bc_abc']):
                            if change['index'] == dico['index']:
                                ind = i
                                break
                        if ind == len(self.state_change['bc_abc']):
                            self.state_change['bc_abc'].append({'index': dico['index'],  
                                                                'value': [1., 0., 0], 'inc': False})
                    if dico['variable'] == 'bc_a':
                        val = values[v]
                        if val < self.parameter['limitations']['bc_a_mini']:
                            val = self.parameter['limitations']['bc_a_mini']
                        self.state_change['bc_abc'][ind]['value'][0] = val                    
                    elif dico['variable'] == 'bc_b':
                        self.state_change['bc_abc'][ind]['value'][1] = values[v] 
                    elif dico['variable'] == 'bc_c':
                        self.state_change['bc_abc'][ind]['value'][2] = values[v]

                elif dico['variable'] == 'bc_gps':
                    # Boundary chronicle with gaussian process perturbation
                    if 'bc_gps' not in self.state_change:
                        self.state_change['bc_gps'] = [] 
                    self.state_change['bc_gps'].append({'index': dico['index'], 'value': extra[v], 
                                                        'inc': False, 'control': values[v]})                                        
                
                else:
                    msg1 = 'No change possible for {}'.format(dico['variable'])
                    self.logger.error(msg1)
                    raise MascaretError(msg1)
            
            # Check boundary conditions for bc_abc if changes from state
            try:
                for i, change in enumerate(self.state_change['bc_abc']):
                    chronicle = self.model.bc_keep[change['index']]
                    bc_org = chronicle.value
                    a = change['value'][0]
                    b = change['value'][1]
                    bc = a * bc_org + b
                    if chronicle.typecode == 1:
                        # Check min discharge
                        if np.min(bc) < self.parameter['limitations']['bc_Q_mini']:
                            b = self.parameter['limitations']['bc_Q_mini'] - np.min(bc)
                            bc = a * bc_org + b
                            # Check max discharge
                        if np.max(bc) > self.parameter['limitations']['bc_Q_maxi']:
                            b = self.parameter['limitations']['bc_Q_maxi'] - np.max(bc)
                    elif chronicle.typecode == 2:
                        # Check min level
                        if np.min(bc) < self.parameter['limitations']['bc_H_mini']:
                            b = self.parameter['limitations']['bc_H_mini'] - np.min(bc)
                            bc = a * bc_org + b
                        # Check max level
                        if np.max(bc) > self.parameter['limitations']['bc_H_maxi']:
                            b = self.parameter['limitations']['bc_Q_maxi'] - np.max(bc)
                    self.state_change['bc_abc'][i]['value'][1] = b
            except KeyError:
                pass

        # Check boundary conditions for bc_gps if changes from state or increment
        try:
            for i, change in enumerate(self.state_change['bc_gps']):
                flags.append(None)
                chronicle = self.model.bc_keep[change['index']]
                bc_chg = chronicle.value + change['value']
                if chronicle.typecode == 1:
                    # Check min discharge
                    ind = np.where(bc_chg < self.parameter['limitations']['bc_Q_mini'])[0]
                    if len(ind) > 0:
                        bc_chg[ind] = self.parameter['limitations']['bc_Q_mini']
                        flags[-1] = True
                    # Check max discharge
                    ind = np.where(bc_chg > self.parameter['limitations']['bc_Q_maxi'])[0]
                    if len(ind) > 0:
                        bc_chg[ind] = self.parameter['limitations']['bc_Q_maxi']
                        flags[-1] = True
                elif chronicle.typecode == 2:
                    # Check min level
                    ind = np.where(bc_chg < self.parameter['limitations']['bc_H_mini'])[0]
                    if len(ind) > 0:
                        bc_chg[ind] = self.parameter['limitations']['bc_H_mini']
                        flags[-1] = True
                    # Check max level
                    ind = np.where(bc_chg > self.parameter['limitations']['bc_H_maxi'])[0]
                    if len(ind) > 0:
                        bc_chg[ind] = self.parameter['limitations']['bc_H_maxi']
                        flags[-1] = True
                if flags[-1]:
                    self.state_change['bc_gps'][i]['value'] = bc_chg - chronicle.value
                    flags[-1] = {'index': change['index'], 'value': self.state_change['bc_gps'][i]['value']}
        except KeyError:
            pass

        return flags

    def update_gps(self, extra):
        """Update the GP sampler perturbation reference
            - extra:  increment to add
        """
        
        if 'bc_gps' in self.control:
            for i, index in enumerate(self.control['bc_gps']):
                if extra[i] is not None:
                    self.model.bc_keep[index].value += extra[i]

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
        
        # Empty output and figures directories
        if directory:
            shutil.rmtree(self.outdir)
            shutil.rmtree(self.figdir)
            os.makedirs(self.outdir)
            os.makedirs(self.figdir)
            
        # Save current state
        if save_state:
            self.saved_state = self.model.masc.save_state()
            self.logger.debug('State saved as {} for model {}.'.format(self.saved_state, self.member))
        
        # Dump state previously stored
        if dump_state:
            self.model.masc.free_saved_state(self.saved_state)
        
        # Initial condition
        if restartdir is not None:
            # Copy restart file
            self.state0 = None
            shutil.copyfile(os.path.join(restartdir, self.files['lig']),
                            os.path.join(self.wdir, self.files['lig']))
        else:
            if self.state0 is None:
                self.state0 = {}
            # Restore state
            if restore_state:
                if self.saved_state is not None:
                    self.state0['saved_state'] = self.saved_state
                    self.saved_state = None
                else:
                    msg1 = 'No saved state available.'
                    self.logger.error(msg1)
                    raise MascaretError(msg1)
            elif time and shift != 0:
                if self.saved_overlap is not None:
                    self.state0['saved_state'] = self.saved_overlap
                    self.saved_overlap = None
                    if self.saved_state is not None:
                        self.model.masc.free_saved_state(self.saved_state)
                        self.saved_state = None
                else:
                    msg1 = 'No saved state available for sliding windows.'
                    self.logger.error(msg1)
                    raise MascaretError(msg1)
            elif state:
                self.state0['initial_conditions'] = {}
                self.state0['initial_conditions']['z'] = self.model.global_elevation
                self.state0['initial_conditions']['q'] = self.model.global_discharge

        # Model times
        if time:
            self.set_time(dateref=self.datestop+timedelta(seconds=shift), start=self.stop+shift)
                
        # Boundary conditions
        if persist:
            # Save the current boundary conditions
            for bc in self.model.bc:
                self.bc_chronicle_svg[bc] = self.model.bc[bc].copy()
            # Persist the boundary conditions
            if self.state0 is None:
                self.state0 = {}
            self.state0['boundary_conditions'] = []
            for bc in self.model.bc:
                chronicle = self.model.bc[bc]
                if chronicle.typecode == 1 or chronicle.typecode == 2:
                    size_bc = chronicle.size_bc
                    taxis = [i for i in range(size_bc) if chronicle.taxis[i] <= self.start]
                    if not taxis:
                        val = chronicle.value[0]
                    elif len(taxis) == size_bc:
                        val = chronicle.value[-1]
                    else:
                        i = taxis[-1]
                        val = chronicle.value[i] + (self.start-chronicle.taxis[i]) \
                            * (chronicle.value[i+1]-chronicle.value[i]) \
                            / (chronicle.taxis[i+1]-chronicle.taxis[i])
                    self.state0['boundary_conditions'].append({'name': bc, 'value': val})
            self.persist = True
        elif self.persist:
            # Renitialise the boundary conditions
            for bc in self.bc_chronicle_svg:
                chronicle = self.bc_chronicle_svg[bc]
                if chronicle.typecode == 1 or chronicle.typecode == 2:
                    self.model.change_boundary_condition({'name': bc, 'value': chronicle.value})
            self.persist = False

        # Initialise now
        if init_now:
            self(dateref=self.datestart, length=0)

    def move_outputs(self, paths):
        """Move outputs into archiving directory
           - paths:     dictionary with the paths for archiving
        """
                
        # Move outputs
        try:
            # Move file .lis            
            namein = '{}/{}'.format(self.outdir, self.files['listing'])
            if self.member > 0:
                namefile = self.files['listing'].split('.')
                nameout = '{}/{}_memb{}.{}'.format(paths['run'], namefile[0], self.member, namefile[1])
            else:
                nameout = '{}/{}'.format(paths['run'], self.files['listing'])
            shutil.move(namein, nameout)
            
            # Move file .opt            
            namein = '{}/{}'.format(self.outdir, self.files['res'])
            if self.member > 0:
                namefile = self.files['res'].split('.')
                nameout = '{}/{}_memb{}.{}'.format(paths['run'], namefile[0], self.member, namefile[1])
            else:
                nameout = '{}/{}'.format(paths['run'], self.files['res'])
            shutil.move(namein, nameout)
            
            # Move post-processing files
            if 'postproc' in paths:
                # Move figures
                if 'plot' in paths['postproc']:
                    for file in os.listdir(self.figdir):
                        shutil.move('{}/{}'.format(self.figdir, file), paths['postproc']['plot'])
            
        except IOError as err:
            msg1 = 'Cannot move the output files:\n{}'.format(err)
            self.logger.error(msg1)
            raise MascaretError(msg1)

    def dump_restart(self, restartdir):
        """Dump restart files
            - restartdir:  directory containing the restart files
        """

        # Filename
        thedate = self.datestart.strftime('%Y%m%d-%H%M')
        if self.member > 0:
            filename = '{}/{}_{}_memb{}.lig'.format(restartdir, thedate, 
                                                    self.files['lig'].split('.')[0], self.member)
        else:
            filename = '{}/{}_{}'.format(restartdir, thedate, self.files['lig'])

        # Write file
        self.model.save_lig_restart(out_file=filename, ks=True)

    def dump_assim_restart(self, restartdir):
        """Dump restart information for assimilation
            - restartdir:  directory containing the restart files
        """

        # Filename
        thedate = self.datestart.strftime('%Y%m%d-%H%M')
        filename = '{}/{}_assim_model.txt'.format(restartdir, thedate)

        # Write file
        with open(filename, 'wb') as fout:
            fout.write('Assimilation information for restart written on {}\n.'
                       .format(datetime.now().strftime('%d/%m/%Y %H:%M')).encode('utf-8'))
            fout.write('---------------------------------------------------------------\n\n'.encode('utf-8'))
            if 'bc_gps' in self.control:
                fout.write('bc_gps: {}\n'.format(self.control['bc_gps']).encode('utf-8'))
                for bc_id in self.control['bc_gps']:
                    bc = self.model.bc_keep[bc_id]
                    fout.write('   {}: '.format(bc_id).encode('utf-8'))
                    np.savetxt(fout, bc.value.reshape((1, bc.size_bc)), fmt=(bc.size_bc * '%10.3f'))

    def pickle(self, time_only=False, overlap=False):
        """Pickle for parallelisation
            - time_only: pickle the time only
            - overlap:   True for pickling state for sliding window
        """

        if overlap:
            if self.saved_overlap is not None:
                self.model.masc.set_state(self.saved_overlap, 1)
            else:
                self.model.masc.set_state(self.state0['saved_state'], 1)

        if time_only:
            return [self.datestart, self.length, self.start]
        else:
            return [self.datestart, self.length, self.start, self.model.global_elevation, self.model.global_discharge]

    def unpickle(self, gherkins, time_only=False, overlap=False):
        """Unpickle for parallelisation
            - gherkins:  Saved information
            - time_only: Unpickle the time only
            - overlap:   True for pickling state for sliding window
        """

        self.set_time(gherkins[0], gherkins[1], gherkins[2])
        if time_only:
            self.model.masc.set('State.SimulPhase', 1)
        else:
            self.model.initialize_model(gherkins[3], gherkins[4])
            if overlap:
                self.saved_overlap = self.model.masc.save_state()

    def reconstruct_output_file(self, filelist):
        """ Reconstruct output files by keeping the last state for each time step
            - filelist:    list of files for the reconstruction
        """
        
        # Prepare the file list
        optlist = [f for f in filelist if f.split('.')[-1] == 'opt']
        optlist.sort()
        lislist = [f for f in filelist if f.split('.')[-1] == 'lis']
        lislist.sort()
        
        # Process .opt
        fileout = '{}/{}'.format(self.outdir, self.files['res'])
        with open(fileout, 'w') as fout:
            for file in optlist:
                with open('{}/{}'.format(self.outdir, file), 'r') as fin:
                    data = fin.read().split('\n')
                    i = 0
                    while data[i] != '[resultats]':
                        i += 1
                    if len(optlist) == 1:
                        datatowrite = data[:]
                    elif file == optlist[0]:
                        datatowrite = data[:len(data)-self.shape[0]-1]
                    elif file == optlist[-1]:
                        datatowrite = data[i+1:]
                    else:
                        datatowrite = data[i+1:len(data)-self.shape[0]-1]
                for dataw in datatowrite:
                    fout.write('{} \n'.format(dataw))
                  
        # Process .lis
        fileout = '{}/{}'.format(self.outdir, self.files['listing'])
        with open(fileout, 'w') as fout:
            for file in lislist:
                with open('{}/{}'.format(self.outdir, file), 'r') as fin:
                    data = fin.read().split('\n')
                for dataw in data:
                    fout.write('{} \n'.format(dataw))
                               
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

        # File name to open
        if size_ensemble == 1:
            if fname is None:
                filename = '{}/{}/{}'.format(self.archdir, datedir, self.files['res'])
            else:
                ext = self.files['res'].split('.')[-1]
                filename = '{}/{}/{}.{}'.format(self.archdir, datedir, fname, ext)
        else:
            if fname is None:
                name = self.files['res'].split('.')
                filename = '{}/{}/{}_memb1.{}'.format(self.archdir, datedir, name[0], name[1])
            else:
                ext = self.files['res'].split('.')[-1]
                filename = '{}/{}/{}_memb1.{}'.format(self.archdir, datedir, fname, ext)

        # Open file
        with open(filename, 'r') as fin:
            data = fin.readlines()
            data = [d.strip() for d in data]

        # Find the column of the variables
        i = data.index('[variables]') + 1
        varbs = []
        while data[i] != '[resultats]':
            varbs.append(data[i].split(';')[1][1:-1])
            i += 1
        self.var_ind = []
        for var in variable:
            if var == 's':
                self.var_ind.append(3)
            if var == 'h':
                self.var_ind.append(varbs.index('Y') + 4)
            elif var == 'z':
                self.var_ind.append(varbs.index('Z') + 4)
            elif var == 'zb':
                self.var_ind.append(varbs.index('ZREF') + 4)
            elif var == 'q':
                self.var_ind.append(varbs.index('Q') + 4)
            elif var == 'Ksmin':
                self.var_ind.append(varbs.index('KMIN') + 4)
            elif var == 'Ksmaj':
                self.var_ind.append(varbs.index('KMAJ') + 4)
        i += 1
        self.start_line = i

        # Find time indices
        tmp = [float(line.split(';')[0]) for line in data[i:] if line]
        nbx = tmp.count(tmp[0])
        tmp = list(set(tmp))
        tmp.sort()
        self.tim_ind = [(np.abs(t - np.array(tmp))).argmin() * nbx for t in times]

        # Find location indices
        if 'all' in location:
            self.loc_ind = nbx
        else:
            tmp = [float(line.split(';')[3]) for line in data[i:i+nbx]]
            tmp = list(set(tmp))
            tmp.sort()
            self.loc_ind = [(np.abs(s[0] - np.array(tmp))).argmin() for s in location]

    def extract_from_file(self, location, variable, datedir, times, size_ensemble, fname=None):
        """Extract a variable at a particular location for post processing
            - location:       list of model-like coordinates (tuple),
                              or 'all' for all locations
            - variable:       list of variables to extract
            - datedir:        cycling directory
            - times:          list of time to extract in seconds
            - size_ensemble:  size of the ensemble
            - fname:          name of file, default given by the instance configuration
        """

        # List of filenames to open
        if size_ensemble == 1:
            if fname is None:
                filenames = ['{}/{}/{}'.format(self.archdir, datedir, self.files['res'])]
            else:
                ext = self.files['res'].split('.')[-1]
                filenames = ['{}/{}/{}.{}'.format(self.archdir, datedir, fname, ext)]
        else:
            if fname is None:
                name = self.files['res'].split('.')
                filenames = ['{}/{}/{}_memb{}.{}'.format(self.archdir, datedir, name[0], m, name[1])
                             for m in range(1, size_ensemble + 1)]
            else:
                ext = self.files['res'].split('.')[-1]
                filenames = ['{}/{}/{}_memb{}.{}'.format(self.archdir, datedir, fname, m, ext)
                             for m in range(1, size_ensemble + 1)]

        # Loop on files
        res = {}
        for m, f in enumerate(filenames):
            
            # Open the file
            with open(f, 'r') as fin:
                data = fin.readlines()
                data = [d.strip() for d in data]

            # Extraction
            for cv, var in enumerate(variable):
                if var not in res:
                    res[var] = {}
                if 'all' in location:
                    if 'all' not in res[var]:
                        res[var]['all'] = {}
                    for ct, t in enumerate(self.tim_ind):
                        if times[ct] not in res[var]['all']:
                            res[var]['all'][times[ct]] = np.zeros((size_ensemble, self.loc_ind))
                        line = data[self.start_line + t: self.start_line + t + self.loc_ind]
                        field = [float(v.split(';')[self.var_ind[cv]]) for v in line]
                        res[var]['all'][times[ct]][m, :] = field
                else:
                    for cc, c in enumerate(self.loc_ind):
                        if location[cc] not in res[var]:
                            res[var][location[cc]] = {}
                        for ct, t in enumerate(self.tim_ind):
                            if times[ct] not in res[var][location[cc]]:
                                res[var][location[cc]][times[ct]] = np.zeros(size_ensemble)
                            line = data[self.start_line + t + c]
                            line = line.split(';')
                            res[var][location[cc]][times[ct]][m] = float(line[self.var_ind[cv]])

        return res

    def __repr__(self):
        """Information"""
        
        string = 'Model {} \n'.format(self.name)
        string += '   configuration       : {}\n'.format(self.config)
        string += '   static directory    : {}\n'.format(self.statdir)
        string += '   working directory   : {}\n'.format(self.wdir)
        string += '   archiving directory : {}\n'.format(self.archdir)
        string += '   run time            : {} - {}\n'.format(self.start, self.stop)
        string += '   timestep            : {}\n'.format(self.step)
        return string
