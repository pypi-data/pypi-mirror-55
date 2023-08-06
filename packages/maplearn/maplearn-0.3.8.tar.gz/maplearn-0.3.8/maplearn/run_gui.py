# -*- coding: utf-8 -*-
"""
Mapping Learning's GUI
----------------------

The **Graphical User Interface** (GUI) aims to help you to:

1. **understand** how to do machine learning well
2. **properly configure** the application and get results

To run *maplearn* with its GUI, type in a terminal:
    
.. code-block:: bash

    maplearn_gui

*NB: this command calls the Python script "run_gui.py".*

Structure:

* On the left, you can set paramaters
* On the right, you can read help about these parameters


.. image:: image/gui_welcome.png
    :align: center

*NB: For now, the GUI is only available in French but its translation (at least
in English) is considered.*

The interface will accompany you through the 3 steps necessary to the
configuration.

1. **Input/Output**


.. image:: image/gui_io.png
    :align: center

2. **Preprocessing**


.. image:: image/gui_preprocess.png
    :align: center

3. **Processing**


.. image:: image/gui_process.png
    :align: center

After having defined all the necessary parameters, all you have to do is click
on "Executer" and be a little patient...

"""
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

from maplearn.app.gui.gui import Gui
from maplearn import logger

def main():
    """
    Run Mapping Learning with its GUI (Graphical User Interface)
    """
    logger.info('maplearn Gui starting...')
    # configuration
    app = QApplication(sys.argv)
    window = QMainWindow()
    _ = Gui(window)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
