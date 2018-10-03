import os
import sys
import logging
from _atiiaftt import ffi,lib

class FTUnit:
    """
    Convenience class holding accepted units for the atiia functions. 
    
    Constants declared from 'ftconfig.c'.
    """
    FORCE_LB=ffi.new("char[]","lb".encode("ascii"))
    """lb\\0"""
    FORCE_KLB=ffi.new("char[]","klb".encode("ascii"))
    """klb\\0"""
    FORCE_N=ffi.new("char[]","N".encode("ascii"))
    """N\\0"""
    FORCE_KN=ffi.new("char[]","kN".encode("ascii"))
    """kN\\0"""
    FORCE_G=ffi.new("char[]","g".encode("ascii"))
    """g\\0"""
    FORCE_KG=ffi.new("char[]","kg".encode("ascii"))
    """kg\\0"""
    TORQUE_IN_LB=ffi.new("char[]","in-lb".encode("ascii"))
    """in-lb\\0"""
    TORQUE_FT_LB=ffi.new("char[]","ft-lb".encode("ascii"))
    """ft-lb\\0"""
    TORQUE_N_M=ffi.new("char[]","N-m".encode("ascii"))
    """N-m\\0"""
    TORQUE_N_MM=ffi.new("char[]","N-mm".encode("ascii"))
    """N-mm\\0"""
    TORQUE_KG_CM=ffi.new("char[]","kg-cm".encode("ascii"))
    """kg-cm\\0"""
    DIST_M=ffi.new("char[]","m".encode("ascii"))
    """m\\0"""
    DIST_CM=ffi.new("char[]","cm".encode("ascii"))
    """cm\\0"""
    DIST_MM=ffi.new("char[]","mm".encode("ascii"))
    """mm\\0"""
    DIST_FT=ffi.new("char[]","ft".encode("ascii"))
    """ft\\0"""
    ANGLE_DEG=ffi.new("char[]","deg".encode("ascii"))
    """deg\\0"""
    ANGLE_RAD=ffi.new("char[]","rad".encode("ascii"))
    """rad\\0"""

class FTSensor:
    """
    Wrapper class to hold force-torque sensor calibration and values.
    """
    def __init__(self,CalFilePath=None,index=1):
        """
        Force-torque sensor instance constructor. Optionally takes calibration file info.

        @param CalFilePath: Path string passed to self.createCalibration
        @type CalFilePath: string
        @param index: Index value passed to self.createCalibration
        @type index: int
        """
        self.logger=logging.getLogger("atiiaftt.FTSensor")

        self.calibration=ffi.NULL
        if CalFilePath!=None:
            self.createCalibration(CalFilePath,index)

        self.voltage_vector=[]
        self.bias_vector=[]
        self.ft_vector=[]

    def createCalibration(self,CalFilePath,index):
        """
        Wraps c function 'createCalibration()'.

        @param CalFilePath: Path string of calibration file for the sensor
        @type CalFilePath: string
        @param index: Index value of the requested calibration data.
        @type index: int
        @raises IOError: exception raised if 'CalFilePath' fails os.path.exists()
        @raises IndexError: exception raised if index value not found in calibration file
        """
        if not (os.path.exists(CalFilePath)):
            self.logger.error("Can't find calibration file: "+CalFilePath)
            raise IOError("Calibration file not found.")

        cffi_cal_filepath=ffi.new("char[]",CalFilePath.encode("ascii"))
        self.calibration=lib.createCalibration(cffi_cal_filepath,index)
        if self.calibration==ffi.NULL:
            self.logger.error("Index not found in calibration file.")
            raise IndexError("Passed calibration index not found.")
        # else ok

    def setToolTransform(self,vector,distunits,angleunits):
        """
        Wraps c function 'SetToolTransform()'.

        @param vector: 
        @type vector: list of floats
        @param distunits:
        @type distunits: atiiaftt.FTUnit.DIST_* class member
        @param angleunits:
        @type angleunits: atiiaftt.FTUnit.ANGLE_* class member
        @raises RuntimeError: exception raised if function is called before loading a calibration dataset.
        @raises ValueError: exception raised if unknown unit is passed.
        """
        cffi_vector=ffi.new("float[]",vector)
        ret_val=lib.SetToolTransform(self.calibration,cffi_vector,distunits,angleunits)
        if ret_val == 1:
            raise RuntimeError("Calibration data not loaded.")
        elif ret_val == 2:
            raise ValueError("Invalid distance unit.")
        elif ret_val == 3:
            raise ValueError("Invalid angle unit.")

    def setForceUnits(self,newunits):
        """
        Wraps c function 'SetForceUnits()'

        @param newunits: New force unit to used. Stored in 'calibration.cfg.ForceUnits'
        @type newunits: atiiaftt.FTUnit.FORCE_* class member
        @raises RuntimeError: exception raised if function is called before loading a calibration dataset.
        @raises ValueError: exception raised if unknown unit is passed.

        """
        ret_val=lib.SetForceUnits(self.calibration,newunits)
        if ret_val == 1:
            raise RuntimeError("Calibration data not loaded.")
        elif ret_val == 2:
            raise ValueError("Invalid force unit.")

    def setTorqueUnits(self,newunits):
        """
        Wraps c function 'SetTorqueUnits()'

        @param newunits: New torque unit to used. Stored in 'calibration.cfg.TorqueUnits'
        @type newunits: atiiaftt.FTUnit.TORQUE_* class member
        @raises RuntimeError: Exception raised if function is called before loading a calibration dataset.
        @raises ValueError: Exception raised if unknown unit is passed.

        """
        ret_val=lib.SetTorqueUnits(self.calibration,newunits)
        if ret_val == 1:
            raise RuntimeError("Calibration data not loaded.")
        elif ret_val == 2:
            raise ValueError("Invalid torque unit.")

    def bias(self,voltages):
        """
        Wraps c function 'Bias()'

        @param voltages: Averaged set of ADC readings from a sensor
        @type voltages: list of floats, also stored in self.bias_vector
        @raises RuntimeError: exception raised if function is called before loading a calibration dataset.

        """
        self.bias_vector=voltages
        if self.calibration==ffi.NULL:
            self.logger.error("Calibration data not loaded.")
            raise RuntimeError("Calibration data not loaded.")

        cffi_bias=ffi.new("float[]",voltages)
        self.logger.debug("{}".format(cffi_bias))
        lib.Bias(self.calibration,cffi_bias)

    def convertToFt(self,voltages):
        """
        Wraps c function 'ConvertToFT()'. 
        The most recent voltages are also stored in self.voltage_vector
        The most recent conversion is also stored in self.ft_vector

        @param voltages: values read from an ADC connected to a sensor
        @type voltages: list of floats
        @raises RuntimeError: exception raised if function is called before loading a calibration dataset.
        @return: Force-torque values, also stored in self.ft_vector
        @rtype: list of floats, format [F.x,F.y,F.z,T.x,T.y,T.z]

        """
        self.voltage_vector=voltages
        if self.calibration==ffi.NULL:
            self.logger.error("Calibration data not loaded.")
            raise RuntimeError("Calibration data not loaded.")

        cffi_ft_vector=ffi.new("float[]",[0,0,0,0,0,0])
        cffi_voltages=ffi.new("float[]",voltages)
        lib.ConvertToFT(self.calibration,cffi_voltages,cffi_ft_vector)
        self.ft_vector=list(cffi_ft_vector)
        return self.ft_vector
