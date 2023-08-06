"""
Perturbation
============

Initialise and sample perturbations

Methods:
    - batman_law:         sample wrt a law using batman
    - batman_gpsampler:   uses the gp sampler from batman

"""

import logging
import numpy as np
from batman.space import Space
from batman.space.gp_sampler import GpSampler
from ..common.errors import PertError

# List of possibilities
available_pert = ['batman_law', 'batman_gpsampler']

# ======================================================


class Perturbation(object):

    logger = logging.getLogger('Perturbation')
    logging.Logger.setLevel(logger, logging.INFO)

    # =================================== #
    #               Methods               #
    # =================================== #

    def __init__(self, config=None, control=None, prm=None, boundary_axis=None):
        """Constructor
            - config:          dictionary containing the perturbation configuration
            - control:         control variables
            - prm:             model parameters
            - boundary_axis:   dictionnary of boundary axis
        """

        self.control = control                 # Dictionary of control variables
        #                                        {'Ksmin': [1, 2, 3], 'bc_gps': ['debit_tonneins']}
        self.boundary = boundary_axis          # Dictionary of boundary axis
        #                                        {'debit_tonneins': array([0, 3600, ..., 741600])}
        self.configuration = []                # List of the perturbation configurations
        #                                        [{'variable': 'Ksmin', 'zone': 1, 'method': 'batman_law', 
        #                                          'update': True, 'config': {...}}, 
        #                                         ...
        #                                         {'variable': 'bc_gps', 'index': 'debit_tonneins', 
        #                                          'method': 'batman_gpsampler', 'update': True, 'config': {...}}]
        self.perturb = {}                      # Dictionary of the perturbations
        #                                        {'batman_law': {'id': [0, 1, 2], 'corners': [...], 
        #                                                        'distrib': ['Uniform(25.0,35.0)', ...], 
        #                                                        'plabel': ['Ksmin@1', ...],
        #                                                        'psize': [1, 1, 1],
        #                                                        'sample': array(size, nb ids)}
        #                                         'batman_gpsampler': {'id': [3], 'gpsampler': [...], 
        #                                                              'plabel': [['a0@debit_tonneins', ...]], 
        #                                                              'psize': [6], 'coeff': [], 'sample': []}}
        self.npert = 0                         # Number of perturbation configurations
        self.pert_size = []                    # List of the perturbation coefficient size
        self.space = None                      # Batman space instance
        self.sample = []                       # List of perturbation samples
        self.extra = []                        # List of actual perturbations when sample are coefficients

        # Initialisation for no perturbation
        if config is None:
            return

        # Initialisation of the perturbation configuration
        self.init_configuration(config, control, prm)

        # Initialise the perturbation sampling depending on the method
        self.init_perturbation()

        # Define the size of the perturbation coefficients
        for c, config in enumerate(self.configuration):
            if config['method'] == 'batman_law':
                if 'vector' in config and config['vector'] > 1:
                    self.pert_size.append(config['vector'])
                else:
                    self.pert_size.append(1)
            elif config['method'] == 'batman_gpsampler':
                i = self.perturb['batman_gpsampler']['id'].index(c)
                nb = self.perturb['batman_gpsampler']['psize'][i]
                if config['config']['kernel_update']:
                    nb += 1
                self.pert_size.append(nb)
        self.pert_size = np.array(self.pert_size)
        self.nbpert = len(self.configuration)

    def init_configuration(self, config, control, prm):
        """Initialise the configurations for the perturbations. Check that the
            control variables are all perturbed. Make sure that the perturbations
            for non-controlled variables are not updated.
            - config:    dictionary containing the perturbation configuration
            - control:   control variables
        """

        self.configuration = []
        noctl = []

        try:
            # Loop on control variables
            for var in control:
                # Gather all the configurations for this control variable
                tmpvar = [d for d in config if d['variable'] == var or
                          var in prm['composite'] and d['variable'] in prm['composite'][var][0]]

                # Loop on indices
                for ind in control[var]:
                    # Gather all the configurations for this index or zone
                    try:
                        tmp = [d for d in tmpvar if d['index'] == ind]
                    except KeyError:
                        tmp = [d for d in tmpvar if d['zone'] == ind]
                    if len(tmp) == 0:
                        msg = 'No perturbations for {} at {}.'.format(var, ind)
                        self.logger.error(msg)
                        raise PertError(msg)

                    # Check composite variables
                    if var in prm['composite'] and len(tmp) < len(prm['composite'][var][0]):
                        for v in prm['composite'][var][0]:
                            if v not in [d['variable'] for d in tmp]:
                                try:
                                    tmp.append({'variable': v, 'method': tmp[0]['method'],
                                                'index': tmp[0]['index'], 'update': False, 'config': {}})
                                except KeyError:
                                    tmp.append({'variable': v, 'method': tmp[0]['method'],
                                                'zone': tmp[0]['zone'], 'update': False, 'config': {}})
                        # Sort the components in the same order as composite
                        tmp2 = []
                        for v in prm['composite'][var][0]:
                            d = [t for t in tmp if t['variable'] == v]
                            tmp2.append(d[0])
                        tmp = tmp2

                    # Log the configuration and remove it from the temporary list                   
                    for d in tmp:
                        self.configuration.append(d)
                        try:
                            tmpvar.remove(d)
                        except ValueError:
                            pass

                # Log the configuration for the non-controlled indices
                try:
                    indlist = [d['index'] for d in tmpvar]
                except KeyError:
                    indlist = [d['zone'] for d in tmpvar]
                # Loop on non-controlled indices
                for ind in indlist:
                    # Gather all the configurations for this index or zone
                    try:
                        tmp = [d for d in tmpvar if d['index'] == ind]
                    except KeyError:
                        tmp = [d for d in tmpvar if d['zone'] == ind]

                    # Log the configuration 
                    for d in tmp:
                        noctl.append(d)

            # Non-controlled variables
            for d in config:
                if d not in self.configuration and d not in noctl:
                    noctl.append(d)

            # Log the non-controlled variables and/or indices without update
            for d in noctl:
                d['update'] = False
                self.configuration.append(d)

        except Exception:
            msg = 'Incorrect perturbation configuration.'
            self.logger.exception(msg)
            raise PertError(msg)

    def init_perturbation(self):
        """Initialise the perturbations depending on the method"""

        self.perturb = {}

        for method in available_pert:
            listpert = [c for c in self.configuration if c['method'] == method]

            if len(listpert) == 0:
                continue

            if method == 'batman_law':
                self.init_batman_law(listpert)

            elif method == 'batman_gpsampler':
                self.init_batman_gpsampler(listpert)

    def generate_sample(self, size):
        """Generate a sample of perturbations
            - size:    size of the ensemble
        """

        self.sample = []
        for m in range(size):
            self.sample.append([0] * self.nbpert)
        self.extra = [None] * len(self.configuration)

        if 'batman_law' in self.perturb:
            self.sample_batman_law(size)
            for j in range(size):
                count = 0
                for id_pert in self.perturb['batman_law']['id']:
                    if 'vector' in self.configuration[id_pert]:
                        s = count + self.configuration[id_pert]['vector']
                        self.sample[j][id_pert] = self.perturb['batman_law']['sample'][j, count: s]
                        count = s
                    else:
                        self.sample[j][id_pert] = self.perturb['batman_law']['sample'][j, count]
                        count += 1
        if 'batman_gpsampler' in self.perturb:
            self.sample_batman_gpsampler(size)
            for i, id_pert in enumerate(self.perturb['batman_gpsampler']['id']):
                for j in range(size):
                    self.sample[j][id_pert] = self.perturb['batman_gpsampler']['coeff'][i][j, :]
                self.extra[id_pert] = self.perturb['batman_gpsampler']['sample'][i]

    def update(self, xa, model):
        """Update the perturbations
            - xa:      mean analysis
            - model:   model for checking the pertutbations limits
        """

        if 'batman_law' in self.perturb:
            self.update_batman_law(xa, model)

        if 'batman_gpsampler' in self.perturb:
            self.update_batman_gpsampler()

    # =================================== #
    #           Batman law                #
    # =================================== #

    def init_batman_law(self, configlist):
        """Initialise perturbations from laws using batman
            - configlist:   list of configurations
        """

        # Initialisation
        dlist = []
        corners = [[], []]
        labels = []
        idlist = []

        # Loop on dictionary
        for config in configlist:
            dico = config['config']

            # Non-perturbed composite variables
            if dico == {}:
                continue
            if 'range' in dico and dico['range'] == [0., 0.]:
                continue

            # Perturbed variables
            idlist.append(self.configuration.index(config))
            law = dico['law']
            if law == 'Uniform':
                dlist.append('{}({},{})'.format(law, dico['range'][0], dico['range'][1]))
                corners[0].append(dico['range'][0])
                corners[1].append(dico['range'][1])
            elif law == 'Normal':
                dlist.append('Normal({},{})'.format(dico['mu'], dico['sigma']))
                corners[0].append(dico['mu'] - 10. * dico['sigma'])
                corners[1].append(dico['mu'] + 10. * dico['sigma'])
            elif law == 'Beta':
                dlist.append('BetaMuSigma({},{},{},{}).getDistribution()'.
                             format(dico['mu'], dico['sigma'], dico['range'][0], dico['range'][1]))
                corners[0].append(dico['range'][0])
                corners[1].append(dico['range'][1])

            # Take into account vectors of perturbations
            if 'vector' in config and config['vector'] > 1:
                dlist.extend([dlist[-1]] * (config['vector'] - 1))
                corners[0].extend([corners[0][-1]] * (config['vector'] - 1))
                corners[1].extend([corners[1][-1]] * (config['vector'] - 1))
                try:
                    labels.extend(['{}{}@{}'.format(config['variable'], i, config['index'])
                                   for i in range(1, config['vector'] + 1)])
                except KeyError:
                    labels.extend(['{}{}@{}'.format(config['variable'], i, config['zone'])
                                   for i in range(1, config['vector'] + 1)])
            else:
                try:
                    labels.append('{}@{}'.format(config['variable'], config['index']))
                except KeyError:
                    labels.append('{}@{}'.format(config['variable'], config['zone']))
    
        # Dictionary
        if self.perturb == {}:
            self.perturb['batman_law'] = {'id': idlist,
                                          'corners': corners,
                                          'distrib': dlist,
                                          'plabel': labels,
                                          'psize': [1] * len(dlist),
                                          'sample': None}
        else:
            self.perturb['batman_law']['corners'] = corners
            self.perturb['batman_law']['distrib'] = dlist

    def sample_batman_law(self, size):
        """Sample perturbations from law using batman
            - size: number of samples
        """

        pert = self.perturb['batman_law']

        # Generate the design of experiment
        self.space = Space(corners=pert['corners'], sample=size,
                           plabels=pert['plabel'], psizes=pert['psize'])

        # Sampling
        sample = self.space.sampling(kind='lhs', dists=pert['distrib'])
        if self.perturb['batman_law']['sample'] is None:
            self.perturb['batman_law']['sample'] = sample
        else:
            for i, id_pert in enumerate(pert['id']):
                if self.configuration[id_pert]['update']:
                    self.perturb['batman_law']['sample'][:, i] = sample[:, i]

    def update_batman_law(self, xa, model):
        """Update the perturbation from law using batman
            - xa:      mean analysis
            - model:   model for checking the range
        """

        # Update the configuration
        for i, id_pert in enumerate(self.perturb['batman_law']['id']):
            if self.configuration[id_pert]['update']:

                if self.configuration[id_pert]['config']['law'] == 'Uniform':
                    # Uniform law
                    rg = (self.configuration[id_pert]['config']['range'][1] -
                          self.configuration[id_pert]['config']['range'][0]) / 2.
                    try:
                        rg = model.check_range(self.configuration[id_pert]['variable'],
                                               [xa.array[id_pert] - rg, xa.array[id_pert] + rg],
                                               self.configuration[id_pert]['index'])
                    except KeyError:
                        rg = model.check_range(self.configuration[id_pert]['variable'],
                                               [xa.array[id_pert] - rg, xa.array[id_pert] + rg],
                                               self.configuration[id_pert]['zone'] - 1)
                    self.configuration[id_pert]['config']['range'] = rg

                elif self.configuration[id_pert]['config']['law'] == 'Beta':
                    # beta law
                    rgp = self.configuration[id_pert]['config']['range'][1] - \
                        self.configuration[id_pert]['config']['mu']
                    rgm = self.configuration[id_pert]['config']['mu'] - \
                        self.configuration[id_pert]['config']['range'][0]
                    try:
                        rg = model.check_range(self.configuration[id_pert]['variable'],
                                               [xa.array[id_pert] - rgm, xa.array[id_pert] + rgp],
                                               self.configuration[id_pert]['index'])
                    except KeyError:
                        rg = model.check_range(self.configuration[id_pert]['variable'],
                                               [xa.array[id_pert] - rgm, xa.array[id_pert] + rgp],
                                               self.configuration[id_pert]['zone'] - 1)
                    self.configuration[id_pert]['config']['range'] = rg
                    self.configuration[id_pert]['config']['mu'] = xa.array[id_pert]

        # Update the perturbations
        listpert = [c for c in self.configuration if c['method'] == "batman_law"]
        self.init_batman_law(listpert)

    # =================================== #
    #        Batman gpsampler             #
    # =================================== #

    def init_batman_gpsampler(self, configlist):
        """Initialise perturbations from gpsampler using batman
            - configlist:   list of configurations
        """

        # Initialisation
        gpsampler = []
        idlist = []
        labels = []
        psize = []

        # Loop on dictionary
        for c, config in enumerate(configlist):
            dico = config['config']

            # Non-perturbed composite variables
            if dico['sigma'] == 0.:
                continue

            # Perturbed variables
            id_pert = self.configuration.index(config)
            axis = self.boundary[config['index']]
            reference = {'indices': [[t] for t in axis], 'values': [0] * len(axis)}
            self.configuration[id_pert]['config']['reference'] = reference

            if dico['kernel_update']:
                # The gpsampler will be initialise when sampling
                self.logger.warning('No kernel update for the moment.')
                dico['kernel_update'] = False
                configlist[c]['config']['kernel_update'] = False

            # Initialisation of the sampler
            dist = 'Matern({},nu={})'.format(dico['scale'], dico['nu'])
            gpsampler.append(GpSampler(reference=reference, kernel=dist,
                                       add=False, threshold=dico['threshold'],
                                       std=dico['sigma']))
            idlist.append(id_pert)
            psize.append(gpsampler[-1].n_modes)
            labels.append([])
            for m in range(psize[-1]):
                labels[-1].append('a{}@{}'.format(m, config['index']))

        # Dictionary
        self.perturb['batman_gpsampler'] = {'id': idlist,
                                            'gpsampler': gpsampler,
                                            'plabel': labels,
                                            'psize': psize,
                                            'coeff': None,
                                            'sample': None}

    def get_gpsampler_structure(self):
        """Provide the structure of perturbations for the gp sampler"""

        struct = []
        for c, config in enumerate(self.configuration):
            if config['method'] == 'batman_gpsampler':
                struct.append(np.array([0] * self.pert_size[c]))

        return struct

    def sample_batman_gpsampler(self, size):
        """Sample from gp_sampler using batman
            - size: number of samples
        """

        # Sampling
        if self.perturb['batman_gpsampler']['sample'] is None:
            self.perturb['batman_gpsampler']['sample'] = []
            self.perturb['batman_gpsampler']['coeff'] = []
            for i, id_pert in enumerate(self.perturb['batman_gpsampler']['id']):
                sampler = self.perturb['batman_gpsampler']['gpsampler'][i]
                sample = sampler(size)
                self.perturb['batman_gpsampler']['coeff'].append(sample['Coefficients'])
                self.perturb['batman_gpsampler']['sample'].append(sample['Values'])
        else:
            for i, id_pert in enumerate(self.perturb['batman_gpsampler']['id']):
                if self.configuration[id_pert]['update']:
                    sampler = self.perturb['batman_gpsampler']['gpsampler'][i]
                    sample = sampler(size)
                    self.perturb['batman_gpsampler']['coeff'][i] = sample['Coefficients']
                    self.perturb['batman_gpsampler']['sample'][i] = sample['Values']

    def change_gpsampler_sample(self, index, member, value):
        """Change the sample values
            - index:     index of the sample
            - member:    member of the ensemble
            - value:     new values
        """

        i = -1
        for j, l in enumerate(self.perturb['batman_gpsampler']['plabel']):
            if index in l[0]:
                i = j
                break
        self.perturb['batman_gpsampler']['sample'][i][member, :] = value

    def take_inc_batman_gpsampler(self, size, increment):
        """Resample from coefficients after taking into account an increment
            - size: number of samples
            - increment:   increment for the current coefficients
        """

        if 'batman_gpsampler' not in self.perturb:
            self.extra = None
            return

        self.extra = []
        for i, id_pert in enumerate(self.perturb['batman_gpsampler']['id']):
            if np.sum(self.pert_size[:id_pert]) > increment.shape[1]:
                continue
            coeff = self.perturb['batman_gpsampler']['coeff'][i]
            coeff += increment[:, np.sum(self.pert_size[:id_pert]):np.sum(self.pert_size[:id_pert + 1])].array
            sampler = self.perturb['batman_gpsampler']['gpsampler'][i]
            sample = sampler(size, coeff)
            self.perturb['batman_gpsampler']['coeff'][i] = sample['Coefficients']
            self.perturb['batman_gpsampler']['sample'][i] = sample['Values']
            self.extra.append(self.perturb['batman_gpsampler']['sample'][i])

    def update_batman_gpsampler(self):
        """Update the perturbation from gp_sampler using batman
        """

        self.extra = []
        for i, id_pert in enumerate(self.perturb['batman_gpsampler']['id']):
            if self.configuration[id_pert]['update']:
                try:
                    self.extra.append(np.mean(self.perturb['batman_gpsampler']['sample'][i], axis=0))
                except (IndexError, TypeError):
                    self.extra.append(None)
            else:
                self.extra.append(None)

    def __repr__(self):
        """Information"""

        string = ''
        return string
