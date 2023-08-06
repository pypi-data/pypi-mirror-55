"""
Barbatruc
=========

"""


import logging
import shutil
import os
import numpy as np
from datetime import timedelta
from .model import Model
from ..common.vector import Vector
from ..common.errors import BarbatrucError
from examples import smurf_test

# ======================================================


class Barbatruc(Model):

    logger = logging.getLogger('Barbatruc')
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

        self.ctl_length = 0
        self.first_node = [0]

        if value == {} or self.postproc:
            self._control = None
        else:
            self._control = value
            for var in self._control:
                if var == 'sloc':
                    self.ctl_length += 2
                else:
                    self.ctl_length += 1
                self.first_node.append(self.ctl_length)
        
    # Dictionary of parameters
    @property
    def params(self):

        params = {"nx": self.nx,
                  "ny": self.ny,
                  "dx": self.dx,
                  "rho": self.rho,
                  "nu": self.nu,
                  "u_west": self.u_west,
                  "tend": self.t_end,
                  "source": self.source}
        return params

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
        self.name = 'Barbatruc'
        
        # Initialisation of specific attributes
        self.nx = self.conf['nx']          # x-axis domain
        self.ny = self.conf['ny']          # y-axis domain
        self.dx = self.conf['dx']          # spatial step
        self.rho = self.conf['rho']        # density
        self.nu = self.conf['nu']          # kinematic viscosity
        self.u_west = self.conf['u_west']  # western boundary condition for u-velocity
        self.t_end = self.conf['t_end']    # final time
        self.u = None                      # u-velocity
        self.v = None                      # v-velocity
        self.p = None                      # pressure
        self.ps = None                     # passive scalar
        self.time = None                   # model time

        self.source = {'location': tuple(self.conf['source']['location']),    # Source
                       'value': self.conf['source']['value'],
                       'blur_it': self.conf['source']['blur_it']}

        if not self.postproc:

            # Directories
            self.outdir = '{}/{}'.format(self.wdir, self.member)
            self.figdir = self.outdir
            try:
                if os.path.exists(self.outdir):
                    shutil.rmtree(self.outdir)
                os.makedirs(self.outdir)
            except IOError as err:
                msg1 = 'Cannot create output directory:\n{}'.format(err)
                self.logger.error(msg1)
                raise BarbatrucError(msg1)

    def set_time(self, dateref=None, length=None, start=None):
        """Define time of the run
            - dateref: datetime of the start
            - length:  length of the run in seconds
            - start:   initial time
        """

        if dateref is None:
            dateref = self.datestart
        if start is None:
            start = 0
        if length is None:
            length = 0

        Model.set_time(self, dateref, length, start)

    def copy(self, members=None):
        """Create new model instances with the same characteristics
            - members: list of member id
        """

        if members is None:
            members = [1]

        listmodels = []                # list of model instances

        # Loop on models
        for m in members:
            self.logger.info('Instanciate member {}'.format(m))

            # Instanciate new member
            new_instance = Barbatruc(self.config, self.prm, self.statdir, self.wdir, self.archdir, m)

            # control and interpol must have the same id for both models
            new_instance.control = self.control

            # Set time
            new_instance.set_time(self.datestart, self.length, self.start)

            # Append the new instance
            listmodels.append(new_instance)
    
        return listmodels

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
        
        # Take into account possible changes from assimilation
        self.init_changes()

        # Run the model
        if length > 0:

            rec_field, self.time = smurf_test(self.params, 10)
            self.u = rec_field['vel_u']
            self.v = rec_field['vel_v']
            self.ps = rec_field['scal']
            self.p = rec_field['press']
            self.time *= 1000

            # Write the inputs and the results
            if file is not None and file[:3] == 'bkg':
                basename = '{}_'.format(file)
            else:
                basename = ''

            fname = '{}/{}input.txt'.format(self.outdir, basename)
            with open(fname, 'w') as fout:
                fout.write('rho: {}\n'.format(self.rho))
                fout.write('nu: {}\n'.format(self.nu))
                fout.write('u_west: {}\n'.format(self.u_west))

            for field, name in zip([self.u, self.v, self.p, self.ps, self.time],
                                   ['u-velocity', 'v-velocity', 'pressure', 'passive_scalar', 'time']):
                filename = '{}/{}{}.npy'.format(self.outdir, basename, name)
                np.save(filename, field)

    def init_changes(self):
        """Initialise the changes"""

        if self.state_change is not None:

            for var in self.state_change:
                val = self.state_change[var]['value']
                if var == 'rho':
                    if self.state_change[var]['inc']:
                        val += self.rho
                    self.rho = val
                elif var == 'nu':
                    if self.state_change[var]['inc']:
                        val += self.nu
                    self.nu = val
                elif var == 'u_west':
                    if self.state_change[var]['inc']:
                        val += self.u_west
                    self.u_west = val
                elif var == 'source':
                    if self.state_change[var]['inc']:
                        val += self.source['value']
                    self.source['value'] = val
                elif var == 'sloc':
                    if self.state_change[var]['inc']:
                        val[0] += self.source['location'][0]
                        val[1] += self.source['location'][1]
                    self.source['location'] = (int(round(val[0])), int(round(val[1])))

            self.state_change = None

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

        # Loop on coordinate type
        for ctype in coord['spatial']:

            if ctype not in model_coord['spatial']:
                model_coord['spatial'][ctype] = []

            if ctype == ('y', 'x'):
                model_coord['spatial'][('y', 'x')] = coord['spatial'][('y', 'x')]

    def get_coord_limits(self):
        """Return the limits of the domain"""

        return [[0, self.ny - 1], [0, self.nx - 1]]

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
        Mxb = []
        Hxb = []

        # Get xb
        self.init_changes()
        xb = self.control_vector()

        self(dateref=datestart, length=length, dumptime=dumptime, file=file)

        # Start and stop indices for observations
        obslist = [i for i in range(len(obsinfo['time'])) if obsinfo['time'][i] in dumptime]

        # Control vector
        Mxb.append(self.control_vector())

        # Apply H
        Hxb.extend(self.apply_Hnolin(obsinfo, obslist[0], obslist[-1] + 1).array)

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
            if v == 'rho':
                ctl[ind0] = self.rho
            elif v == 'nu':
                ctl[ind0] = self.nu
            elif v == 'u_west':
                ctl[ind0] = self.u_west
            elif v == 'source':
                ctl[ind0] = self.source['value']
            elif v == 'sloc':
                ctl[ind0] = self.source['location'][0]
                ctl[ind0 + 1] = self.source['location'][1]

        return ctl

    def apply_Hnolin(self, coords, ist, iend):
        """Return the vector in observation space
            Non-linear version of H
            - coords:      dictionary of coordinates after self.convert_coord()
            - ist:         first index to take into account
            - iend:        last index to take into account
        """

        # Initialisation
        Hv = np.zeros(iend - ist)

        # Loop on observation type
        listtype = set(coords['obs_type'])
        for obs in listtype:

            # Define observation elements for this variable
            tlist = [np.argmin(np.abs(self.time - t)) for t in coords['time'][ist:iend]]
            indlist = [int(tlist[i] * self.ny * self.nx + coords['scoord'][i][0] * self.nx +
                       coords['scoord'][i][1]) for i in range(ist, iend) if coords['obs_type'][i] == obs]
            hvlist = [i - ist for i in range(ist, iend) if coords['obs_type'][i] == obs]

            if obs == 'u':

                Hv[hvlist] = self.u.ravel()[indlist]

            elif obs == 'v':
                Hv[hvlist] = self.v.ravel()[indlist]

            elif obs == 'p':
                Hv[hvlist] = self.p.ravel()[indlist]

            elif obs == 'ps':
                Hv[hvlist] = self.ps.ravel()[indlist]

            else:
                msg1 = 'Non-linear H cannot be applied for observation type {}'.format(obs)
                self.logger.error(msg1)
                raise BarbatrucError(msg1)

        return Vector(Hv)

    def check_increment(self, bkg, increment):
        """Check the correctness of the increment
            - bkg:       background state
            - increment: increment to be added to the background state
        """

        # Initialisation
        analysis = bkg + increment
        new_increment = Vector(increment.array)
        flag = False

        for v, var in enumerate(self.control):
            ind0 = self.first_node[v]

            if var in ['rho', 'nu', 'u_west', 'source']:
                # Check min
                mini = [self.parameter['limitations']['rho_mini'], self.parameter['limitations']['nu_mini'],
                        self.parameter['limitations']['u_west_mini'], self.parameter['limitations']['source_mini']
                        ][['rho', 'nu', 'u_west', 'source'].index(var)]
                if analysis[ind0] < mini:
                    new_increment[ind0] = mini - bkg[ind0]
                    flag = True
                # Check max
                maxi = [self.parameter['limitations']['rho_maxi'], self.parameter['limitations']['nu_maxi'],
                        self.parameter['limitations']['u_west_maxi'], self.parameter['limitations']['source_maxi']
                        ][['rho', 'nu', 'u_west', 'source'].index(var)]
                if analysis[ind0] > maxi:
                    new_increment[ind0] = maxi - bkg[ind0]
                    flag = True

            elif var == 'sloc':
                new_increment[ind0] = np.round(increment[ind0].array)
                new_increment[ind0+1] = np.round(increment[ind0+1].array)
                # Check mini
                if analysis[ind0] < 0:
                    new_increment[ind0] = -bkg[ind0]
                    flag = True
                if analysis[ind0+1] < 0:
                    new_increment[ind0 + 1] = -bkg[ind0 + 1]
                    flag = True
                # Check maxi
                if analysis[ind0] >= self.ny:
                    new_increment[ind0] = self.ny - 1 - bkg[ind0]
                    flag = True
                if analysis[ind0+1] >= self.nx:
                    new_increment[ind0+1] = self.nx - 1 - bkg[ind0 + 1]
                    flag = True

        if flag:
            self.logger.warning('check increment: the increment has been modified.')

        return new_increment

    def check_range(self, var, therange, index=None):
        """Check if a range of values is consistent for a variable
            - var:       name of variable
            - therange:     range to check [min,max]
            - index:     index of the variable for BC
        """
        
        vmin = therange[0]
        vmax = therange[1]
        rg = vmax - vmin

        if var in ['rho', 'nu', 'u_west', 'source']:
            mini = [self.parameter['limitations']['rho_mini'], self.parameter['limitations']['nu_mini'],
                    self.parameter['limitations']['u_west_mini'], self.parameter['limitations']['source_mini']
                    ][['rho', 'nu', 'u_west', 'source'].index(var)]
            maxi = [self.parameter['limitations']['rho_maxi'], self.parameter['limitations']['nu_maxi'],
                    self.parameter['limitations']['u_west_maxi'], self.parameter['limitations']['source_maxi']
                    ][['rho', 'nu', 'u_west', 'source'].index(var)]
            if vmin < mini:
                vmin = mini
                vmax = mini + rg
            elif vmax > maxi:
                vmax = maxi
                vmin = maxi - rg

        elif var == 'sloc_y':
            if vmin < 0.:
                vmin = 0.
                vmax = rg
            elif vmax >= self.ny:
                vmax = self.ny - 1.
                vmin = vmax - rg

        elif var == 'sloc_x':
            if vmin < 0.:
                vmin = 0.
                vmax = rg
            elif vmax >= self.nx:
                vmax = self.nx - 1.
                vmin = vmax - rg

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

                if var in ['rho', 'nu', 'u_west', 'source']:
                    if bkg is None:
                        self.state_change[var] = {'index': 0, 'inc': True, 'value': increment[ind0].array[0]}
                    else:
                        self.state_change[var] = {'index': 0, 'inc': False,
                                                  'value': (bkg[ind0] + increment[ind0]).array[0]}

                elif var == 'sloc':
                    if bkg is None:
                        self.state_change[var] = {'index': 0, 'inc': True, 'value': increment[ind0:ind1].array}
                    else:
                        self.state_change[var] = {'index': 0, 'inc': False,
                                                  'value': (bkg[ind0:ind1] + increment[ind0:ind1]).array}

        if state is not None and values is not None:
            if self.state_change is None:
                self.state_change = {}
            for v, dico in enumerate(state):

                if dico['variable'] in ['rho', 'nu', 'u_west', 'source']:
                    if dico['variable'] not in self.state_change:
                        self.state_change[dico['variable']] = []
                    val = values[v]
                    mini = [self.parameter['limitations']['rho_mini'], self.parameter['limitations']['nu_mini'],
                            self.parameter['limitations']['u_west_mini'], self.parameter['limitations']['source_mini']
                            ][['rho', 'nu', 'u_west', 'source'].index(dico['variable'])]
                    if val < mini:
                        val = mini
                    maxi = [self.parameter['limitations']['rho_maxi'], self.parameter['limitations']['nu_maxi'],
                            self.parameter['limitations']['u_west_maxi'], self.parameter['limitations']['source_maxi']
                            ][['rho', 'nu', 'u_west', 'source'].index(dico['variable'])]
                    if val > maxi:
                        val = maxi
                    self.state_change[dico['variable']] = {'index': 0, 'value': val, 'inc': False}

                elif dico['variable'] in ['sloc_y', 'sloc_x']:
                    if 'sloc' not in self.state_change:
                        self.state_change['sloc'] = {'index': 0, 'value': [10, 10], 'inc': False}
                    if dico['variable'] == 'sloc_y':
                        val = int(round(values[v]))
                        if val < 0:
                            val = 0
                        elif val >= self.ny:
                            val = self.ny - 1
                        self.state_change['sloc']['value'][0] = val
                    elif dico['variable'] == 'sloc_x':
                        val = int(round(values[v]))
                        if val < 0:
                            val = 0
                        elif val >= self.nx:
                            val = self.nx - 1
                        self.state_change['sloc']['value'][1] = val

        return flags

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
            os.makedirs(self.outdir)

        # Model times
        if time:
            self.set_time(dateref=self.datestop + timedelta(seconds=shift), start=self.stop + shift)

        # Initialise now
        if init_now:
            self(dateref=self.datestart, length=0)

    def move_outputs(self, paths):
        """Move outputs into archiving directory
           - paths:     dictionary with the paths for archiving
        """

        namein = '{}/input.txt'.format(self.outdir)
        if self.member > 0:
            nameout = '{}/input_memb{}.txt'.format(paths['run'], self.member)
        else:
            nameout = '{}/input.txt'.format(paths['run'])
        try:
            shutil.move(namein, nameout)
        except IOError as err:
            msg1 = 'Cannot move the input file:\n{}'.format(err)
            self.logger.error(msg1)
            raise BarbatrucError(msg1)

        # Move outputs
        for name in ['u-velocity', 'v-velocity', 'pressure', 'passive_scalar', 'time']:
            namein = '{}/{}.npy'.format(self.outdir, name)
            if self.member > 0:
                nameout = '{}/{}_memb{}.npy'.format(paths['run'], name, self.member)
            else:
                nameout = '{}/{}.npy'.format(paths['run'], name)
            try:
                shutil.move(namein, nameout)
            except IOError as err:
                msg1 = 'Cannot move the output files:\n{}'.format(err)
                self.logger.error(msg1)
                raise BarbatrucError(msg1)
        
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

        # Initialisation
        res = {}

        # Time names
        if size_ensemble == 1:
            if fname is None:
                timenames = ['{}/{}/time.npy'.format(self.archdir, datedir)]
            else:
                timenames = ['{}/{}/{}_time.npy'.format(self.archdir, datedir, fname)]
        else:
            if fname is None:
                timenames = ['{}/{}/time_memb{}.npy'.format(self.archdir, datedir, m)
                             for m in range(1, size_ensemble + 1)]
            else:
                timenames = ['{}/{}/{}_time_memb{}.npy'.format(self.archdir, datedir, fname, m)
                             for m in range(1, size_ensemble + 1)]

        # Load times and find indices for interpolation
        timelist = []
        indlist1 = []
        indlist2 = []
        for file in timenames:
            timelist.append(np.load(file))
            indlist1.append([np.where(timelist[-1] <= t)[0][-1] for t in times])
            indlist2.append([i + 1 if i + 1 < len(timelist[-1]) else i for i in indlist1[-1]])

        # Loop on variables
        for var in variable:
            res[var] = {}

            # List of file names
            name = self.parameter['variables'][var][0].replace(' ', '_')
            if size_ensemble == 1:
                if fname is None:
                    filenames = ['{}/{}/{}.npy'.format(self.archdir, datedir, name)]
                else:
                    filenames = ['{}/{}/{}_{}.npy'.format(self.archdir, datedir, fname, name)]
            else:
                if fname is None:
                    filenames = ['{}/{}/{}_memb{}.npy'.format(self.archdir, datedir, name, m)
                                 for m in range(1, size_ensemble + 1)]
                else:
                    filenames = ['{}/{}/{}_{}_memb{}.npy'.format(self.archdir, datedir, fname, name, m)
                                 for m in range(1, size_ensemble + 1)]

            # Loop on filenames
            for f, file in enumerate(filenames):

                # Times of the file
                times_real = [t for t in times if t <= timelist[f][-1]]

                # Log the res
                datavar = np.load(file)
                if 'all' in location:
                    if 'all' not in res[var]:
                        res[var]['all'] = {}
                    for t, tim in enumerate(times_real):
                        if tim not in res[var]['all']:
                            res[var]['all'][tim] = np.zeros((size_ensemble, self.ny, self.nx))
                        tmp1 = datavar[indlist1[f][t], :, :]
                        tmp2 = datavar[indlist2[f][t], :, :]
                        slope = (tmp2 - tmp1) / (timelist[f][indlist2[f][t]] - timelist[f][indlist1[f][t]])
                        res[var]['all'][tim][f, :, :] = tmp1 + (tim - timelist[f][indlist1[f][t]]) * slope
                    for tim in times[len(times_real):]:
                        if tim not in res[var]['all']:
                            res[var]['all'][tim] = np.zeros((size_ensemble, self.ny, self.nx))
                        res[var]['all'][tim][f, :, :] = datavar[-1, :, :]
                else:
                    for loc in location:
                        if loc not in res[var]:
                            res[var][loc] = {}
                            for t, tim in enumerate(times_real):
                                if tim not in res[var][loc]:
                                    res[var][loc][tim] = np.zeros(size_ensemble)
                                tmp1 = datavar[indlist1[f][t], loc[0], loc[1]]
                                tmp2 = datavar[indlist2[f][t], loc[0], loc[1]]
                                slope = (tmp2 - tmp1) / (timelist[f][indlist2[f][t]] - timelist[f][indlist1[f][t]])
                                res[var][loc][tim][f] = tmp1 + (tim - timelist[f][indlist1[f][t]]) * slope
                            for tim in times[len(times_real):]:
                                if tim not in res[var][loc]:
                                    res[var][loc][tim] = np.zeros(size_ensemble)
                                res[var][loc][tim][f] = datavar[-1, loc[0], loc[1]]

        return res

    def __repr__(self):
        """Information"""
        
        string = 'Barbatruc \n'
        string += '   configuration       : {}\n'.format(self.config)
        string += '   static directory    : {}\n'.format(self.statdir)
        string += '   working directory   : {}\n'.format(self.wdir)
        string += '   archiving directory : {}\n'.format(self.archdir)
        string += '   domain dimension    : ({}, {})\n'.format(self.ny, self.nx)
        string += '   spatial step        : {}\n'.format(self.dx)
        string += '   final time          : {}\n'.format(self.t_end)
        return string
