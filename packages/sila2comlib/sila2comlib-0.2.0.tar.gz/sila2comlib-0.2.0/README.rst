SiLA2 Communication Library - a Python3 library to hardware interfaces
========================================================================

Installation
------------

The easiest installation can be done via pip :

::

    pip install --user sila2comlib  # --user option installs sila2comlib for current user only

alternatively one could use the setup.py script, like:

.. code:: bash

    cd [sila_library folder containing setup.py]
    pip3 install --user -r requirements_base.txt
    python3 setup.py install

Installation on Raspberry Pi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    pip install sila2comlib

Testing the library with unittests
----------------------------------

.. code:: bash

    cd [sila_library folder containing setup.py]
    python3 setup.py test

sila2lib package Content
------------------------


com - Communication modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~

serial
serial interface communication
provides connections to common libraries, like RS232 serial, CAN bus and

SPI

CAN
^^^

SPI
^^^

tests
~~~~~

unittests
