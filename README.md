# Lidar - object detection module project
### About
----------
This project uses a Lidar [Slamtec A1](https://www.slamtec.com/en/Lidar/A1) device to detect objects in front of the vehicle and categorize them into appropriate entities. The project uses the [rplidar](https://github.com/SkoltechRobotics/rplidar) module.

----------

The modules file contains a set of scripts to i.a. process data received from lidar over serial port. 

## Modules :
 ### The project contains three modules and main script:

- main.py  contains:
    - fnc. reading - main function which gets data form specific angle range (330 - 30 degree)
    - save_data_to_txt - function save data form lidar to txt file
    - save_data_to_xml - function save data to excel sheets
    - standard run - run without saving the data but prints the data to the console
    - test_modules - uses a manually typed array of data
- eks.py  -	module have function to work with excel (save distance, angle, quality data etc.)
- lidr.py - this module includes functions that work with lidar. The main task is to detect deviations
from standard data and classify them as obstacles.
- navi.py - includes functions for detecting the possibility of the vehicle running over or next to obstacles

