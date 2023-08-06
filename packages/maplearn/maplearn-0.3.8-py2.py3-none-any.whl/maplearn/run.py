# -*- coding: utf-8 -*-
"""
Mapping Learning's CLI
----------------------

The CLI (Commande Line Interface) is one of the main entry to play with 
Mapping Learning. Just specify a well-formatted configuration file and run.

The syntax of configuration file is described on
https://bitbucket.org/thomas_a/maplearn/wiki/configuration. A few examples of
configuration are also available in "examples" sub-folder.

**Example**::

    maplearn -c /path/to/configfile

With its CLI you can call Maplearn in an **automated** way through planified
tasks for instance. You can also check easily the effect of a (few)
parameter(s).

To get available parameters, type:

.. code-block:: bash

    maplearn --help
    # or
    maplearn -h


.. image:: image/cli_help.png

Now you can easy change the value of a parameter without creating a new
configuration file:

**Example**:

.. code-block:: bash

    # Changing the number of k-folds (to 5):
    maplearn -c /path/to/configfile -k 5


Be careful about the output folder, or every new run of maplearn will replace
previous results. Don't worry: there is a parameter for that.

.. code-block:: bash

    maplearn -c /path/to/configfile -k 5 -out /path/to/new/directory

"""
from __future__ import print_function
from __future__ import unicode_literals
import os
import sys

from maplearn.app.main import Main
from maplearn.app.reporting import ReportWriter
from maplearn.app.cli import cfg as config
from maplearn import logger

def run():
    """
    Run Mapping Learning using the previously loaded configuration
    """
    logger.info('Maplearn is going to start')

    if config.check() != 0:
        return None

    # redirect stdout to a file
    report_file = os.path.join(config.io['output'], 'index')
    report_writer = ReportWriter(report_file)
    sys.stdout = report_writer

    print(config)
    appli = Main(config.io['output'], codes=config.codes, na=config.io['na'],
                 **config.process)

    # TODO: ugly PATCH to remove ASAP
    if config.process['type'] == 'clustering' and \
            config.io['samples'] is None:
        config.io['samples'] = config.io['data']

    appli.load(source=config.io['samples'], **config.io)
    if config.io['data'] is not None:
        appli.load_data(config.io['data'], features=config.io['features'])
    #basename = os.path.splitext(os.path.basename(config.io['samples']))[0]
    #appli.dataset.plot(os.path.join(config.io['output'],
    #                              'sig_%s.png' % basename))
    #print(appli.dataset)
    appli.preprocess(**config.preprocess)
    appli.process(optimize=config.process['optimize'],
                  predict=config.process['predict'])

    report_writer.close()
    # export configuration in output folder
    config.write(os.path.join(config.io['output'], 'configuration.cfg'))
    logger.info('Maplearn: quit.')

if __name__ == "__main__":
    run()
