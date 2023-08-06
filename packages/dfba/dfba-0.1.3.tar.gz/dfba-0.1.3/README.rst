=============================
Dynamic Flux Balance Analysis
=============================

.. image:: https://img.shields.io/pypi/v/dfba.svg
   :target: https://pypi.org/project/dfba/
   :alt: Current PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/dfba.svg
   :target: https://pypi.org/project/dfba/
   :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/dfba.svg
   :target: http://www.gnu.org/licenses/
   :alt: GPLv3+

.. image:: https://gitlab.com/davidtourigny/dynamic-fba/badges/master/pipeline.svg
   :target: https://travis-ci.org/davidtourigny/dynamic-fba/commits/master
   :alt: Pipeline Status

.. image:: https://gitlab.com/davidtourigny/dynamic-fba/badges/master/coverage.svg
   :target: https://gitlab.com/davidtourigny/dynamic-fba/commits/master
   :alt: Coverage Report

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Black

.. _`Harwood et al., 2016`: https://link.springer.com/article/10.1007/s00211-015-0760-3
.. _GLPK: https://www.gnu.org/software/glpk/
.. _SUNDIALS: https://computation.llnl.gov/projects/sundials
.. _Python: https://www.python.org/
.. _cobrapy: https://github.com/opencobra/cobrapy
.. _optlang: https://github.com/biosustain/optlang
.. _symengine: https://github.com/symengine/symengine

This project provides an object-oriented software package for dynamic
flux-balance analysis (DFBA) simulations using implementations of the direct
method or Algorithm 1 described in the paper `Harwood et al., 2016`_. The main
algorithms for solving embedded LP problems are written in *C++* and use the GNU
Linear Programming Kit (GLPK_) and the Suite of Nonlinear and
Differential/Algebraic Equation Solvers (SUNDIALS_) CVODE or IDA. Extension
modules to cobrapy_ are provided for easy generation and simulation of DFBA
models.

Installation
============

Currently, we cannot provide Python wheels for this package so installation from source is a
bit more involved (see below). The easiest way to run the software is from the provided `Docker <https://docs.docker.com/>`_ image:

.. code-block:: console

    docker run --rm -it davidtourigny/dfba:latest


Prerequisites for installing from source
----------------------------------------

Currently this package is compatible with most UNIX-like operating systems. Provided the following `dependencies <#Dependencies>`_ are
installed, the module can be installed from the root of the repository
using the command:

.. code-block:: console

    pip install .

Dependencies
~~~~~~~~~~~~

.. _`build_glpk.sh`: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/scripts/build_glpk.sh
.. _`build_pybind11.sh`: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/scripts/build_pybind11.sh
.. _`build_sundials.sh`: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/scripts/build_sundials.sh

* A version of Python_ 3.6 or higher is required
* You need `cmake <https://cmake.org/>`_ for the build process
* You will need `git <https://git-scm.com/>`_ to clone this repository to access the scripts and build
  files
* You need a working compiler with C++11 support, for example, by installing ``build-essential`` on
  Debian-derived Linux systems
* GLPK_ version 4.65 is required or can be installed using `build_glpk.sh`_
* SUNDIALS_ version 5.0.0 is required or can be installed using `build_sundials.sh`_
* `pybind11`_ is required or can be installed using `build_pybind11.sh`_

Be aware that some of these packages have their own dependencies that must therefore be installed also (e.g. GLPK_ depends on `GMP <https://gmplib.org/>`_ and `pybind11`_ requires `pytest <https://docs.pytest.org/en/latest/>`_)


Alternatively, a Dockerfile_ is provided for building a `Docker <https://docs.docker.com/>`_
image to run the software from an interactive container. The Docker image can be
built in one step by issuing the command:

.. code-block:: console

    make build

from the root of this repository. It can then be started using:

.. code-block:: console

    make run

Overview
========

.. _`pybind11`: https://github.com/pybind/pybind11
.. _examples: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/examples
.. _example1: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/examples/example1
.. _example2: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/examples/example2
.. _example3: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/examples/example3
.. _example4: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/examples/example4
.. _example5: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/examples/example5
.. _Dockerfile: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/Dockerfile
.. _`example1.py`: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/examples/example1/example1.py

Users are not expected to interact directly with the lower-level *C++* interface
and once installed the package should ideally remain untouched. Instead, the
classes and functions for solving embedded LP problems have been exposed to
*Python* using `pybind11`_. Combined with the provided cobrapy_ extension
modules, this provides the user with the ability to build their own DFBA model
exclusively in *Python*. The *Python* class *DfbaModel* intuitively encapsulates
all the data required for a full definition of a DFBA model by combining an
underlying cobrapy_ object with instances of the *KineticVariable* and
*ExchangeFlux* classes. The *DfbaModel* class instance ensures all user data are
consistent with the initialization and simulation requirements of an embedded LP
problem. User data are passed directly to the algorithms and symbolic functions
are dynamically compiled and loaded prior to simulation. The directory
examples_ also contains scripts for the examples described below, and details on
how the user can adapt these to build and simulate their own model are outlined
at the end of this section.

Example DFBA models provided with current version
-------------------------------------------------

The current version is distributed with several examples_ related to Examples
6.2.1 and 6.3 in `Harwood et al., 2016`_.  example1_ and example2_ are based on
`Hanly & Henson, 2011
<https://onlinelibrary.wiley.com/doi/abs/10.1002/bit.22954>`_ and also Example 1
in `DFBAlab
<https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-014-0409-8>`_.
The genome-scale metabolic network model of the *Escherichia coli* bacterium
`iJR904 <http://bigg.ucsd.edu/models/iJR904>`_ contains 761 metabolites and 1075
reaction fluxes. example3_ and example4_ are based on `Hjersted, Henson, &
Mahadevan, 2007 <https://onlinelibrary.wiley.com/doi/abs/10.1002/bit.21332>`_.
The genome-scale metabolic network model of the *Saccharomyces cerevisiae*
strain S288C `iND750 <http://bigg.ucsd.edu/models/iND750/>`_ contains 1059
metabolites and 1266 reaction fluxes. The above examples all use the default
solver options (see below).  example5_ implements the same model as example1_,
but uses the direct method in place of Algorithm 1 from Harwood *et al*.


Instructions for creating and simulating a DFBA model
-----------------------------------------------------

The following modifications to the script `example1.py`_ will enable the user to
define and simulate their own DFBA model:

* specify path for loading file containing genome-scale metabolic model as
  cobrapy_ model object (line 27)
* set GLPK as LP solver of choice (line 28)
* instantiate object of class *DfbaModel* with cobrapy_ model (line 29)
* instantiate kinetic variables as objects of class *KineticVariable* (lines
  32-36)
* add kinetic variables to the model using the *DfbaModel* method
  *add_kinetic_variables* (line 39)
* instantiate exchange fluxes using the class *ExchangeFlux* (lines 42-46)
* add exchange fluxes to the model using the *DfbaModel* method
  *add_exchange_fluxes* (line 49)
* provide symbolic expression for the time derivative of each kinetic variable
  using the *DfbaModel* method *add_rhs_expression* (lines 52-56)
* add symbolic expressions for upper/lower bounds of selected exchange fluxes
  using the *DfbaModel* methods *add_exchange_flux_ub*/*add_exchange_flux_lb*
  (lines 59-63). In many applications, vector components (e.g., concentrations)
  in the true solution are always positive or non-negative, though at times very
  small.  In the numerical solution, however, small negative (hence unphysical)
  values can then occur. To prevent these from interfering with the simulation,
  the user can supply a symbolic expression that must be non-negative for
  correct evaluation of upper/lower bounds
* add initial conditions for the kinetic variables in the model using the
  *DfbaModel* method *add_initial_conditions* (line 73)
* provide desired simulation times *tstart*, *tstop*, *tout* (simulation start,
  stop, and output times, respectively) to the *DfbaModel* method *simulate*
  (line 84). Results (trajectories of kinetic variables) will be returned as pandas DataFrame. Optionally, the user can also provide a list of reaction ids whose
  flux trajectories will also be returned as a separate DataFrame

There are a number of additional features not covered in example1_, but
whose usages are illustrated in other example scripts. These are outlined below.

The module *SolverData* accessed through the *solver_data* attribute of class
*DfbaModel* allows users to select their preferred algorithm and solver
specifications prior to simulation:

* Custom tolerances (default values are all *1.0e-4*) can be set using the methods
  *set_rel_tolerance* and *set_abs_tolerances*. The former takes a positive
  float value and sets the relative tolerance. The latter takes a list of
  positive floats and uses this to set absolute tolerance values for each
  dynamic variable. The convention for setting absolute tolerance values is that
  the first of how ever many floats are supplied in the list are set to those
  values, while any remaining are set equal to the last. See example2_ for
  illustration
* The choice of SUNDIALS_ *SunMatrix* type (default *dense*) can be set using
  the method *set_sunmatrix*. The choice of SUNDIALS_ *SunLinSolver* (default
  *dense*) can be set using the method *set_sunlinsolver*. See SUNDIALS_
  documentation for details. Currently, the only compatible matrix and linear
  solver combination implemented is the default setting
* If using the direct method (see below), the choice of ODE solver method (ADAMS
  or BDF, default ADAMS) can be set using the method *set_ode_method*. See
  example5_ for illustration
* The choice of DFBA algorithm, Harwood et al. or direct method (default
  *Harwood*), can be set using the method *set_algorithm*. If using the direct
  method, the third parameter of the *DfbaModel* method *simulate* also
  indicates the frequency of calls to the LP solver, and some trial and error
  may be required to establish its optimal value. See
  example5_ for illustration
* The simulation display settings (default *full*) can be set to *full*,
  *glpk_only*, *sundials_only*, or *none* using the method *set_display*. See
  example5_ for illustration

The class *ControlParameter* allows discontinuous parameters, such as model
parameters controlled by an experimentalist, to appear in the symbolic
expressions for derivatives of kinetic variables and upper/lower bounds of
exchange fluxes. Objects of class *ControlParameter* are to be instantiated with
their symbolic expression, an ordered list of times corresponding to
discontinuous change points in the value of the control parameter, and the
corresponding values the control parameter takes at each of the intervals
between change points. *ControlParameter* objects can then can be included in
any symbolic expression added to a *DfbaModel* object using the methods
*add_rhs_expression*, *add_exchange_flux_ub*, and *add_exchange_flux_lb*. A list
of *ControlParameter* objects appearing in each symbolic expression must also be
supplied at this stage. See example3_ for illustration.

Visualization tools are available as an extra dependency, optionally installed from the root of the repository using the commands

.. code-block:: console

    pip install .[plotly]

or

.. code-block:: console

    pip install .[matplotlib]

This also installs `plotly <https://plot.ly/>`_ or `matplotlib <https://matplotlib.org/>`_, respectively. The code commented out at the end of the script `example1.py`_ illustrates how to: plot concentrations during the time (x-axis) of simulation with two y-axes for biomass and metabolites; and plot fluxes trajectories (y-axis) during the time (x-axis) of the simulation.

Awaiting implementation
-----------------------

.. _`Scott et al., 2018`: https://www.sciencedirect.com/science/article/pii/S0098135418309190

Some additional features listed below are awaiting a full implementation:

* Lexicographic optimization as described in `Harwood et al., 2016`_. Although
  the *DfbaModel* method *add_objectives* will direct the selected algorithms to
  perform lexicographic optimization using the supplied objectives during
  simulation, interactions between the LP and ODE/DAE integration routines do
  not appear robust. Users are therefore advised not to use this feature until
  the matter is resolved in a future version

* An algorithm for simulating DFBA models based on an interior point formulation
  has recently been proposed in `Scott et al., 2018`_. Implementation of this
  algorithm as a choice for the user is work in progress

Authors
=======

* David S. Tourigny
* Moritz E. Beber

Additional contributors
=======================

* Jorge Carrasco Muriel (visualization)

Funding
=======

* David S. Tourigny is a Simons Foundation Fellow of the Life Sciences Research
  Foundation.

Copyright
=========

* Copyright © 2018,2019 Columbia University Irving Medical Center, New York, USA
* Copyright © 2019 Novo Nordisk Foundation Center for Biosustainability,
  Technical University of Denmark
* Free software distributed under the `GNU General Public License v3 or later
  (GPLv3+) <http://www.gnu.org/licenses/>`_.

Source Files
============

.. _src: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/src
.. _extension: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/src/extension
.. _`dfba_utils.cpp`: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/src/extension/dfba_utils.cpp
.. _emblp: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/src/extension/emblp
.. _methods: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/src/extension/methods
.. _`solver_data.h`: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/src/extension/solver_data.h
.. _`user_data.h`: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/src/extension/user_data.h
.. _dfba: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/src/dfba
.. _`control.py`: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/src/dfba/control.py
.. _`exchange.py`: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/src/dfba/exchange.py
.. _`helpers.py`: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/src/dfba/helpers.py
.. _`jit.py`: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/src/dfba/jit.py
.. _`model.py`: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/src/dfba/model.py
.. _`library.py`: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/src/dfba/library.py
.. _`variables.py`: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/src/dfba/variables.py
.. _`plot`: https://gitlab.com/davidtourigny/dynamic-fba/tree/master/src/dfba/plot


Source files contained within the directory src_ are split between two
sub-directories separated by their language of implementation.

*C++*
-------

The sub-directory extension_ contains the following content:

* `dfba_utils.cpp`_: contains source code for exposing module to *Python*
* emblp_: contains class and function declarations for embedded LP problems
* methods_: contains algorithms for integration of embedded LP problems
* `solver_data.h`_: struct exposed to *Python* for solver options
* `user_data.h`_: struct exposed to *Python* for model specification

*Python*
----------

The directory dfba_ contains the following content:

* `control.py`_: definition of class *ControlParameter*
* `exchange.py`_: definition of class *ExchangeFlux*
* `helpers.py`_: general helper functions
* `jit.py`_: tools for JIT compilation of dynamic library
* `model.py`_: definition of class *DfbaModel*
* `library.py`_: methods for writing dynamic library
* `variables.py`_: definition of class *KineticVariable*
* `plot`_: directory for additional visualization dependency
