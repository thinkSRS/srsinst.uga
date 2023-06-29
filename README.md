# `srsinst.uga`

`srsinst.uga` contains a Python instrument driver to control and acquire 
mass spectra of atmospheric gas samples from 
[Stanford Research Systems (SRS) Universal Gas Analyzer (UGA)](https://thinksrs.com/products/uga.html).
It also provides a collection of Python scripts that runs on a graphic user interface (GUI) based on
[srsgui](https://thinksrs.github.io/srsgui/) and 
[srsinst.rga](https://thinksrs.github.io/srsinst.rga/). 

![screenshot](https://github.com/thinkSRS/srsinst.uga/blob/main/docs/_static/image/UGA100_composition_analysis_screenshot.png?raw=true " ")

## Installation
You need a working Python version 3.7 or later with `pip` (Python package installer) installed.
If you don't, [install Python 3](https://www.python.org/) to your system.

To install `srsinst.uga` as an instrument driver only, use Python package installer `pip` 
from the command line.

    python -m pip install srsinst.uga

To use its full GUI application, create a virtual environment, if necessary,
and install with *[full]* option:

    # To create a simple virtual environment (Optional)
    python -m venv venv
    venv\scripts\activate

    # To install full GUI application 
    python -m pip install srsinst.uga[full]


## Run `srsinst.uga` as GUI application
If the Python Scripts directory is in PATH environment variable,
Start the application by typing from the command line:

    uga

If not,

    python -m srsinst.uga

It will start the GUI application.

- Connect to an UGA from the Instruments menu.
- Select a task from the Task menu. The available tasks are to acquire data from UGA
  and to run various RGA scans.
- Press the apply button, if you change parameters of the task.
- Press the green arrow to run the selected task. 

There is a tree view widget displaying commands for interactive control. 
It can be accessed from the main menu/Docks/uga-Capture. You can change the parameter of an item
by Double-clicking on its value display, if allowed.

You can write your own task or modify an existing one and run it from the application.
Refer to [Custom tasks](https://thinksrs.github.io/srsinst.rga/custom_tasks.html) section
in the [srsinst.rga documentation](https://thinksrs.github.io/srsinst.rga/) for details.


## Use `srsinst.uga` as instrument driver

### Connect to UGA
* Start a Python program, a Jupyter notebook, or an editor of your 
  choice to write a Python script.
* import the **UGA100** class from `srsinst.uga` package.
* Instantiate **UGA100** to connect to an SRS UGA.

|

    C:\>python
    Python 3.8.3 (tags/v3.8.3:6f8c832, May 13 2020, 22:37:02) [MSC v.1924 64 bit (AMD64)] on win32
    Type "help", "copyright", "credits" or "license" for more information.    
    >>>
    >>> from srsinst.uga import UGA100
    >>>
    >>> ip_address = '172.25.128.13'  # Use IP address of your UGA
    >>> user_id = 'srsuga'
    >>> password = 'srsuga'
    >>>
    >>> uga = UGA100('tcpip',ip_address, user_id, password)
    >>>
    >>> # for serial communication
    >>> # Baud rate for UGA100 is available: 28800 and 38400
    >>> # uga2 = UGA100('serial', /dev/ttyUSB0', 28800)  # for Linux serial communication
    >>> # or,
    >>> # uga2 = UGA100('serial', 'COM3', 28800)  # for Windows serial communication
    >>> # or,
    >>> # initialize a RGA100 instance without connection, then connect.
    >>> # uga3 = UGA100()
    >>> # uga3.connect('tcpip', ip_address, user_id, password)

* Query check_id() to configure components of the connected UGA properly,    
  depending on the variation: UGA, UGA_LT, UGA_HT, or UGA_PM.

        uga.check_id()
        > ('SRS_UGA', '94224', '1.018')     
 
**UGA100** comprises multiple subcomponents, their associated commands and class methods.
 **Component** class has a convenience attribute `dir` to show its  available attributes 
 and methods in the Python dictionary format.

    >>> uga.dir.keys()
    dict_keys(['components', 'commands', 'methods'])

**UGA100** has more than 10 components holding their remote commands and methods
to configure and acquire data from a UGA unit.

    >>> uga.dir['components']
    {'mode': 'instance of Mode', 
     'bp': 'instance of BypassPump',
     'rp': 'instance of RoughingPump',
     'tp': 'instance of TurboPump',
     'vv': 'instance of VentValve', 
     'rga': 'instance of RGA', 
     'ig': 'instance of IonGauge', 
     'ht': 'instance of Heaters', 
     'temperature': 'instance of Temperature', 
     'pressure': 'instance of Pressure', 
     'ethernet': 'instance of Ethernet', 
     'status': 'instance of Status'}

### Control UGA100 components
Let's control the ion gauge. It has no subcomponents, two commands, and a method.

    >>> uga.ig.dir
    {'components': {}, 
     'commands': {'state': ('DictCommand', 'ZCIG'), 
                  'filament': ('DictCommand', 'ZPFL')}, 
     'methods': ['get_pressure']}

The *state* commands is to turn on and off the ion gauge, and the *filament* command 
is to select a filament to use.

    >>> uga.ig.filament
    'Fil. 1'
    >>> uga1.ig.state
    'Off'
    >>> uga1.ig.state = 'On'
    >>> uga1.ig.state
    'On'

With get_command_info() method, you can find out what parameter to use to set the command
and what parameters to expect for a query reply. For the uga.ig.state command, you can use
'Off', 'On', or 'Degas' parameters to set the state, and you will get one of 12 possible 
states.

    >>> uga.ig.get_command_info('state')
    {'command class': 'DictCommand', 
     'raw remote command': 'ZCIG', 
     'set_dict': {'Off': 0, 
         'On': 1, 
         'Degas': 2}, 
     'get_dict': {'Off': 0, 
         'On': 1, 
         'Idle': 2, 
         'Turning on (3)': 3, 
         'Turning on (4)': 4, 
         'Turning on (5)': 5, 
         'Turning off (6)': 6, 
         'Turning off (7)': 7, 
         'Turning idle (8)': 8, 
         'Turning idle (9)': 9, 
         'Turning idle (10)': 10, 
         'Error': 12}, 
     'index_dict': None}

When the ion gauge is on, you can get a pressure measurement with the get_pressure() method.

    >>> uga.ig.get_pressure()
    1.115742e-07

Commands in other components can be used in a similar way. 

The most important component in a UGA is the Residual Gas Analyzer, 
which has the separate [RGA instrument driver package](https://github.com/thinkSRS/srsinst.rga)
 for its independent usage.
Refer to [RGA documentation](https://thinksrs.github.io/srsinst.rga/) for RGA component usage.  

    >>> uga.rga.status.id_string
    'SRSRGA200VER0.24SN12226'
    >>> uga.rga.ionizer.emission_current
    0.9976
