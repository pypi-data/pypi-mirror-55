.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://gitlab.aicrowd.com/flatland/flatland/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the Repository Issue Tracker for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the Repository Issue Tracker for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

flatland could always use more documentation, whether as part of the
official flatland docs, in docstrings, or even on the web in blog posts,
articles, and such. A quick reference for writing good docstrings is available at : https://docs.python-guide.org/writing/documentation/#writing-docstrings

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://gitlab.aicrowd.com/flatland/flatland/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `flatland` for local development.

1. Fork the `flatland` repo on https://gitlab.aicrowd.com/flatland/flatland .
2. Clone your fork locally::

    $ git clone git@gitlab.aicrowd.com:flatland/flatland.git

3. Install the software dependencies via Anaconda-3 or Miniconda-3. (This assumes you have Anaconda installed by following the instructions `here <https://www.anaconda.com/distribution>`_)

    $ conda install -c conda-forge tox-conda
    $ conda install tox
    $ tox -v --recreate

    This will create a virtual env you can then use.

    These steps are performed if you run

    $ getting_started/getting_started.bat/.sh

    from Anaconda prompt.


4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the
   tests, including testing other Python versions with tox::

    $ flake8 flatland tests examples benchmarks
    $ python setup.py test or py.test
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes and push your branch to Gitlab::

    $ git add .
    $ git commit -m "Addresses #<issue-number> Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a merge request through the Gitlab repository website.

Merge Request Guidelines
-------------------------

Before you submit a merge request, check that it meets these guidelines:

1. The merge request should include tests.
2. If the merge request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The merge request should work for Python 3.6, 3.7 and for PyPy. Check
   https://gitlab.aicrowd.com/flatland/flatland/pipelines
   and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::

$ py.test tests.test_flatland


Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed .
Then run::

$ bumpversion patch # possible: major / minor / patch
$ git push
$ git push --tags

TODO: Travis will then deploy to PyPI if tests pass. (To be configured properly by Mohanty)


Local Evaluation
----------------

This document explains you how to locally evaluate your submissions before making
an official submission to the competition.

Requirements
~~~~~~~~~~~~

* **flatland-rl** : We expect that you have `flatland-rl` installed by following the instructions in  [README.md](README.md).

* **redis** : Additionally you will also need to have  `redis installed <https://redis.io/topics/quickstart>`_ and **should have it running in the background.**

Test Data
~~~~~~~~~

* **test env data** : You can `download and untar the test-env-data <https://www.aicrowd.com/challenges/flatland-challenge/dataset_files>`, at a location of your choice, lets say `/path/to/test-env-data/`. After untarring the folder, the folder structure should look something like:


.. code-block:: console

    .
    └── test-env-data
        ├── Test_0
        │   ├── Level_0.pkl
        │   └── Level_1.pkl
        ├── Test_1
        │   ├── Level_0.pkl
        │   └── Level_1.pkl
        ├..................
        ├..................
        ├── Test_8
        │   ├── Level_0.pkl
        │   └── Level_1.pkl
        └── Test_9
            ├── Level_0.pkl
            └── Level_1.pkl

Evaluation Service
~~~~~~~~~~~~~~~~~~

* **start evaluation service** : Then you can start the evaluator by running :

.. code-block:: console

    flatland-evaluator --tests /path/to/test-env-data/

RemoteClient
~~~~~~~~~~~~

* **run client** : Some `sample submission code can be found in the starter-kit <https://github.com/AIcrowd/flatland-challenge-starter-kit/>`_, but before you can run your code locally using `FlatlandRemoteClient`, you will have to set the `AICROWD_TESTS_FOLDER` environment variable to the location where you previous untarred the folder with `the test-env-data`:


.. code-block:: console

    export AICROWD_TESTS_FOLDER="/path/to/test-env-data/"

    # or on Windows :
    #
    # set AICROWD_TESTS_FOLDER "\path\to\test-env-data\"

    # and then finally run your code
    python run.py


