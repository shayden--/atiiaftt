atiiaftt - ATI-IA force-torque transforms
===============================================================

Python interface to ATI-IA force-torque transform (ATIDAQ) C library, v1.0.7. For use with ATI Industrial Automation force-torque sensors.

This package does not read from hardware. Another package, such as NI-DAQmx, 
must be used for that purpose.

ATIDAQ C Library is available at https://www.ati-ia.com/library/software/daq_ft/ATIDAQ%20C%20Library.zip

Installation
------------------------

pip install atiiaftt

Dependencies
------------------------

CFFI and platform appropriate build tools are required to build the C source
that is included with the package. 

For Linux distributions, install the developer package group.

For Windows, see https://wiki.python.org/moin/WindowsCompilers

Documentation
------------------------

Module help for the python classes is available via docstrings. Documentation
for the wrapped functions is available in `ATIDAQ_c_lib/readme.txt`


Usage examples
------------------------

High level usage is as follows:

1. `import atiiaftt`
2. Create an instance of the `atiiafft.FTsensor` class
3. Load calibration data, either passing the calibration file path as a string during class instantiation or as a parameter while calling `instance.createCalibration('./FT18766cal')`.
4. Optionally, set the tool transform, bias values and units as needed, eg)
	- `instance.setToolTransform([0,0,20,45,0,0],atiiaftt.FTUnit.DIST_MM,atiiaftt.FTUnit.ANGLE_DEG)`
	- `instance.bias([0.254,-1.027,0.025,0.7422.0.9302,-0.230,0.082])`
5. Call the force-torque conversion function: `instance.convertToFt([0.042,1.004,0.952,-0.235,0.091,1.091,0.054])`; this returns the forces and torques as a list `[F.x,F.y,F.z,T.x,T.y,T.z]`. The last transformed values are stored in the instance variable `instance.ft_vector` for later access.

CFFI and python class examples found in 'atiiaftt/samples/ftconvert.py'
