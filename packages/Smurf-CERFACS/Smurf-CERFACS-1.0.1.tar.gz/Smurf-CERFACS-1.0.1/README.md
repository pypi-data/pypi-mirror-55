### Smurf: System for Modelling with Uncertainty Reduction, and Forecasting

#### 1) Introduction
Smurf is an open source modular system developed in Python for running and 
cycling data assimilation systems. It is organised around three super classes
for the numerical model management, the assimilation schemes and the observation
instruments. Any new item can be easily plugged in by defining a child class
that will override as many methods as necessary. Non intrusive, Smurf can be
used in any domains for numerical models written in any languages.

Smurf is provided under the CeCILL-B license. 

Contacts: mirouze@cerfacs.fr or ricci@cerfacs.fr.

#### 2) Installation
Smurf runs on python 3. 

##### 2.1) Environment
The easiest way for installing Smurf, is to create first a python 3 environment:

Choose a path for your environment (replace `path_env` by your own path)

<pre>
python -m venv path_env/pyenv
</pre>

Source the environment (**this must be done for any new session**)

<pre>
source path_env/pyenv/bin/activate
</pre>  

##### 2.2) Installing Smurf

Depending on the purpose, there are three different ways for installing Smurf

##### Demonstration only:
The sources are not available

<pre>
pip install Smurf-CERFACS
</pre>

##### Self purpose development:
Developments and modifications can be done on the
local repository but cannot be pushed on the remote repository. A path must be
chosen where to install Smurf (replace `mypath` by your own path)

<pre>
cd mypath
git clone https://gitlab.com/cerfacs/Smurf.git
cd Smurf
python setup.py develop
</pre>

##### Smurf development:
To participate to the Smurf development. This option 
requires to be registred on the Cerfacs Nitrox. A path must be
chosen where to install Smurf (replace `mypath` by your own path)

<pre>
cd mypath
git clone https://nitrox.cerfacs.fr/globc/Smurf.git
cd Smurf
python setup.py develop
</pre>

#### 3) Version 1.0.1
##### 3.1) Assimilation scheme

* Ensemble Kalman filter (stochastic)

##### 3.2) Models
###### 3.2.1) Available 

* Barbatruc: toy model, https://nitrox.cerfacs.fr/open-source/barbatruc
* Mascaret: Hydraulic 1D, http://www.opentelemac.org/

###### 3.2.2) Available on demand

* Opm: Simulation of porous media processes: https://opm-project.org/
* Pixie: Crowd dynamics and evacuation, https://research.csiro.au/pixie

##### 3.3) Instruments
###### 3.3.1) Available

* Barbametre (Barbatruc): tracer values
* Gauge (Mascaret): limnimetric station

###### 3.3.2) Available on demand

* Chronos (Pixie): chronometre
* Clicker (Pixie): people count
* WellInstrument (Opm): well measurements

###### 3.3.3) On-going work

* Swot (Mascaret): Swot observations 
  * SwotPixelCloud (Mascaret): pixel cloud observations from Swot
  * SwotRiverNode (Mascaret): river node averaged observations from Swot
  * SwotRiverReach (Mascaret): river reach averaged observations from Swot

##### 3.4) Contributors
###### Authors

  * Isabelle Mirouze, CECI, CNRS UMR 5318
  * Sophie Ricci, CECI, CERFACS / CNRS UMR 5318

###### Collaborators

* Barbatruc:
  * Antoine Dauptain, CERFACS
* Mascaret
  * Nicole Goutal, LNHE-EDF / LHSV
  * Vanessya Laborie, CEREMA / LHSV
  * Anne-Laure Tiberi, CEREMA
* Opm
  * Camille Besombes, CERFACS
  * Corentin Lapeyre, CERFACS
  * Rabeb Selmi, TOTAL
* Pixie:
  * Matt Bolger, CSIRO Data61
  * Vincent Lemiale, CSIRO Data61
* General purposes:
  * Antoine Dauptain, CERFACS
  * Corentin Lapeyre, CERFACS

#### 4) Getting started
Testing cases are available in *Smurf/testing_case*. For a first go with Smurf,
the toy model Barbatruc can easily be tried 
(see *Smurf/testing_case/Barbatruc/readme.md*). 
If you installed Smurf using pip, the testing cases for Mascaret and Barbatruc 
can be downloaded from 
[here](https://gitlab.com/cerfacs/Smurf/tree/master/testing_case).

#### 5) New features
##### 5.1) New experiment
To help configuring a new experiment, templates of configuration files are available
in *Smurf/templates*

* *template_conf_expriment.yml*: to configure the experiment
* *template_conf_assim.yml*: to configure the assimilation part
* *template_parameter.yml*: to define the parameters of the model

##### 5.1) New model
To plug in a new model:

Create the new model class (replace `newmodel` by the name of your model)
<pre>
cp Smurf/templates/template_new_model.py Smurf/Smurf/models/newmodel.py
</pre>

Define the required method following the instructions of the model template 

##### 5.2) New observation instrument
To plug in a new instrument:

Create the new instrument class (replace `newinstrument` by the name of your instrument)
<pre>
cp Smurf/templates/template_new_instrument.py Smurf/Smurf/observations/newinstrument.py
</pre>

Define the required method following the instructions of the instrument template 

