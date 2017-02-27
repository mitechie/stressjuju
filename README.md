Stress Juju
===========

`stressjuju.py` is a script to run repeated deploys of Juju solutions into clean
models and then tear them down. It's often used with other tools to help
measure and track controller overhead in CPU, disk, and memory.

Setting up
----------

- clone the repo
- make all
- (setup a controller you want to stress against)


Running
-------

Usage:

    source .venv/bin/activate
    python stressjuju/stressjuju.py -c mymaas --credential=maas-creds -n 4 -p 2 bundles/django


Options

- `-c` is what controller to run against. This name should match the name of the
controller you've already got running. This does not bootstrap any controller.
- `--credential` What credential locally can be used to connect to the
controller. (This should be pulled based on the controller but not currently
available)
- `-n` how many total models should be created and destroyed in the run of this
test.
- `-p` how many parallel models can run at once. In the example we're running 4
total models 2 at a time.
- `bundles/django` this will run the test django bundle that's included ootb.
