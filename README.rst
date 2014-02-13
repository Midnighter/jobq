===========
Job Queue
===========


Outline
-------

This package provides 3 modules:
1. A collection of Python scripts that supply a beanstalkd_ queue with job
definitions.
2. An example of using IPython kernels to consume the queue and run the jobs.  Results are then submitted to a special results tube.
3. A manager class that watches the results tube and writes results to various databases.

.. _beanstalkd: https://github.com/kr/beanstalkd

Requirements
------------

* beanstalkc_
* PyYAML_
* `IPython.parallel`_

.. _beanstalkc: https://github.com/earl/beanstalkc/
.. _PyYAML: http://pyyaml.org/
.. _`IPython.parallel`: http://ipython.org/

Optional
~~~~~~~~

* tables_ for storing results

.. _tables: http://www.pytables.org/

Also take a look at the ``requirements.txt`` and ``opt-requirements.txt`` files
that you can use with ``pip`` to install the necessary packages.

    pip install -r <file>

Authors
-------

* Beber, Moritz Emanuel

