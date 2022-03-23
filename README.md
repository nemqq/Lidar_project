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


### Example of the obtained results 
```
WRONG PROBE & DISTANCES
[[3, 4, 5, 6, 7], [11, 12], [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], [31, 32, 33, 34, 35], [39, 40, 41, 42], [46, 47]]
[[111, 111, 151, 129, 128], [224, 223], [220, 220, 221, 222, 223, 224, 225, 226, 227, 250, 250], [293, 207, 208, 209, 210], 
[190, 192, 193, 195], [180, 180]]
number of detected obstacles:  6

errors detected on the samples: 
[[2, 8, 9], [36]]


Detected obstacles function start here
[5, 2, 11, 5, 4, 2]
[126, 224, 228, 225, 192, 180]

width obstacles
obstacle nr.:1 is average
obstacle nr.:2 is very small
obstacle nr.:3 is huge
obstacle nr.:4 is average
obstacle nr.:5 is small
obstacle nr.:6 is very small

type
object is 1 obstacle
object is 2 hole
object is 3 hole
object is 4 hole
object is 5 obstacle
object is 6 obstacle
```
