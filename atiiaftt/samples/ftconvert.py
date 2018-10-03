from __future__ import print_function

import os
import sys
import datetime
import logging 

from _atiiaftt import ffi,lib
import atiiaftt 

def usage_example():
    """
    Usage example for atiiaftt python classes.

    Functionally the same as the Sample/ftconvert.c example included with ATIDAQ zip
    """
    cal_file="tests/FT18766.cal"
    cal_file_index=1

    # same values as sample program 'ftconvert.c'
    bias_readings=[0.265100,-0.017700,-0.038400,-0.042700,-0.189100,0.137300,-3.242300]
    input_floats=[-3.286300,0.387500,-3.487700,0.404300,-3.934100,0.547400,-3.210600]
    translation_floats=[0,0,20,45,0,0]
    output_floats=[0,0,0,0,0,0,0]
    translation_dist_unit=atiiaftt.FTUnit.DIST_MM
    translation_angle_unit=atiiaftt.FTUnit.ANGLE_DEG
    force_unit_str=atiiaftt.FTUnit.FORCE_N
    torque_unit_str=atiiaftt.FTUnit.TORQUE_N_M

    ftSensor00=atiiaftt.FTSensor()
    try:
        forcetorqueValues=ftSensor00.convertToFt(input_floats)
        forcetorqueValues=ftSensor00.bias(bias_readings)
    except RuntimeError:
        logging.error("Caught expected exception.") 

    print("Using calibration file: '{}'".format(cal_file))
    ftSensor01=atiiaftt.FTSensor(cal_file,cal_file_index)
    print(ftSensor01.calibration)

    # print the working calibration matrix (loaded from file, pre-bias)
    print("Calibration Matrix Dimensions [{} Channels,{} Axes]".format(ftSensor01.calibration.rt.NumChannels,ftSensor01.calibration.rt.NumAxes))
    for ai in range(ftSensor01.calibration.rt.NumAxes):
        print("{}\t".format(ffi.string(ftSensor01.calibration.AxisNames[ai])),end="")
        for ci in range(ftSensor01.calibration.rt.NumChannels):
            print("{}\t".format(ftSensor01.calibration.rt.working_matrix[ai][ci]),end="")
        print("")
            
    print("Running tool transform with translation: {}".format(translation_floats))

    ftSensor01.setToolTransform(translation_floats,translation_dist_unit,translation_angle_unit)
    ftSensor01.bias(bias_readings)
    forcetorqueValues=ftSensor01.convertToFt(input_floats)

    print("Bias reading: {}".format(bias_readings))
    print("Measurement: {}".format(input_floats))
    print("Result: {}".format(forcetorqueValues))
    print("Stored Result: {}".format(ftSensor01.ft_vector))
    
    return 0

def cffi_usage_example():
    """
    Usage example for atiiaftt cffi library.

    Functionally the same as the Sample/ftconvert.c example included with ATIDAQ zip
    """
    cal_file="tests/FT18766.cal"
    cal_file_index=1
    cal_file_path=ffi.new("char[]",os.path.join(os.path.dirname(__file__),cal_file).encode("ascii"))

    print(ffi.string(cal_file_path))
    
    calibrationData=lib.createCalibration(cal_file_path,cal_file_index)
    print(calibrationData)

    # print the working calibration matrix (loaded from file, pre-bias)
    print("Calibration Matrix Dimensions [{} Channels,{} Axes]".format(calibrationData.rt.NumChannels,calibrationData.rt.NumAxes))
    for ai in range(calibrationData.rt.NumAxes):
        print("{}\t".format(ffi.string(calibrationData.AxisNames[ai])),end="")
        for ci in range(calibrationData.rt.NumChannels):
            print("{}\t".format(calibrationData.rt.working_matrix[ai][ci]),end="")
        print("")
            
    # same values as sample program 'ftconvert'
    bias_readings=ffi.new("float[]",[0.265100,-0.017700,-0.038400,-0.042700,-0.189100,0.137300,-3.242300])
    input_floats=ffi.new("float[]",[-3.286300,0.387500,-3.487700,0.404300,-3.934100,0.547400,-3.210600])
    translation_floats=ffi.new("float[]",[0,0,20,45,0,0])
    output_floats=ffi.new("float[]",[0,0,0,0,0,0,0])
    translation_dist_unit=ffi.new("char[]","mm".encode("ascii"))
    translation_angle_unit=ffi.new("char[]","degrees".encode("ascii"))
    force_unit_str=ffi.new("char[]","N".encode("ascii"))
    torque_unit_str=ffi.new("char[]","N-m".encode("ascii"))

    lib.SetForceUnits(calibrationData,force_unit_str)
    lib.SetTorqueUnits(calibrationData,torque_unit_str)
    print("Running tool transform with translation: [",end="")
    for i in range(6):
        print(translation_floats[i],end="")
        if (i<5):
            print(",",end="")
    print("]")
    lib.SetToolTransform(calibrationData,translation_floats,translation_dist_unit,translation_angle_unit)
    
    lib.Bias(calibrationData,bias_readings)
    lib.ConvertToFT(calibrationData,input_floats,output_floats)

    print("Bias reading:")
    for i in range(7):
        print(bias_readings[i],end='')
        if (i < 6):
            print(",",end='')
    print("")

    print("Measurement:")
    for i in range(7):
        print(input_floats[i],end='')
        if (i < 6):
            print(",",end='')
    print("")

    print("Result:")
    for i in range(7):
        print(output_floats[i],end='')
        if (i < 6):
            print(",",end='')
    print("")
    
    return 0;

if __name__ == "__main__":

    logging.basicConfig()
    usage_example()
