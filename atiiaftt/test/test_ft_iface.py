from __future__ import print_function

import os
import sys
import datetime
import logging 

from _atiiaftt import ffi,lib
import atiiaftt 

import unittest 

general_log_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.level = logging.DEBUG
log_filepath = os.path.join(".",datetime.datetime.now().strftime('%Y%m%d%H%M')+".atiiaftt.test.log")
#file_log_hndl=logging.FileHandler(log_filepath)
#file_log_hndl.setFormatter(general_log_formatter)
#logger.addHandler(file_log_hndl)

class TestAtiiaFTT(unittest.TestCase):
    def setUp(self):
        self.cal_file="atiiaftt/test/FT18766.cal"
        self.bias_readings=[0.265100,-0.017700,-0.038400,-0.042700,-0.189100,0.137300,-3.242300]
        self.input_floats=[-3.286300,0.387500,-3.487700,0.404300,-3.934100,0.547400,-3.210600]
        self.translation_floats=[0,0,20,45,0,0]
        self.output_floats_n=[-4.285730,-908.400635,-928.162720,-0.679282,-1.102992,-1.988170]
        self.output_floats_kn=[-0.004286, -0.908401, -0.928163, -0.679282, -1.102992, -1.98817]
        self.not_a_unit=ffi.new("char[]","invalid".encode("ascii"))
        self.test_sensor=atiiaftt.FTSensor()

    def test_FTSensor_CreateCal_OK(self):
        """
        Test that a calibration file can be loaded.
        """
        self.test_sensor.createCalibration(self.cal_file,1)
        self.assertNotEqual(self.test_sensor.calibration,ffi.NULL)

    def test_FTSensor_CreateCal_FAIL01(self):
        """
        Test that an exception is raised when the calibration index is out of bounds.
        """
        self.assertRaises(IndexError,self.test_sensor.createCalibration,self.cal_file,0)

    def test_FTSensor_CreateCal_FAIL02(self):
        """
        Test that an exception is rased when the file path does not point to a calibration file.
        """
        self.assertRaises(IOError,self.test_sensor.createCalibration,"/not-a-calfile.txt",1)

    def test_FTSensor_Bias_OK01(self):
        """
        Test that a bias vector can be stored.
        """
        logger.info("start test 'test_FTSensor_Bias01'")
        self.test_sensor.createCalibration(self.cal_file,1)
        logger.info("Created {}".format(self.test_sensor))
        logger.debug("Calibration Object: {}".format(self.test_sensor.calibration))
        self.test_sensor.bias(self.bias_readings)
        logger.debug(self.test_sensor.bias)
        self.assertEqual(self.bias_readings,self.test_sensor.bias_vector)

    def test_FTSensor_Bias_OK02(self):
        """
        Test that a bias vector can be stored by checking the cdata values.
        """
        logger.info("start test 'test_FTSensor_Bias02'")
        self.test_sensor.createCalibration(self.cal_file,1)
        logger.info("Created {}".format(self.test_sensor))
        logger.debug("Calibration Object: {}".format(self.test_sensor.calibration))
        self.test_sensor.bias(self.bias_readings)
        cffi_bias_vector=self.test_sensor.calibration.rt.bias_vector
        logger.debug(cffi_bias_vector)
        bias_vector=[]
        for c_bias in cffi_bias_vector:
            logger.debug("{}".format(c_bias))
            if c_bias!=0.0:
                bias_vector.append(round(c_bias,6))
        logger.debug("{}".format(bias_vector))
        self.assertEqual(self.bias_readings,bias_vector)

    def test_FTSensor_Bias_FAIL01(self):
        """
        Test that an exception is raised while trying to bias an instance with no calibration.
        """
        #self.test_sensor.createCalibration(self.cal_file,1)
        #self.test_sensor.bias(self.bias_readings)
        self.assertRaises(RuntimeError,self.test_sensor.bias,self.bias_readings)

    def test_FTSensor_SetTT_OK01(self):
        """
        Test the setToolTransform wrapper function.
        """
        self.test_sensor.createCalibration(self.cal_file,1)
        self.test_sensor.setToolTransform(self.translation_floats,atiiaftt.FTUnit.DIST_MM,atiiaftt.FTUnit.ANGLE_DEG)
        new_aunit=ffi.string(self.test_sensor.calibration.cfg.UserTransform.AngleUnits)
        new_dunit=ffi.string(self.test_sensor.calibration.cfg.UserTransform.DistUnits)
        tt_vector=list(self.test_sensor.calibration.cfg.UserTransform.TT)
        logger.debug("{}, {}".format(new_aunit,new_dunit))
        logger.debug("{}".format(tt_vector))
        self.assertEqual(b"deg",new_aunit)
        self.assertEqual(b"mm",new_dunit)
        self.assertEqual(self.translation_floats,tt_vector)

    def test_FTSensor_SetTT_OK02(self):
        """
        Test the setToolTransform wrapper function.
        """
        self.test_sensor.createCalibration(self.cal_file,1)
        self.test_sensor.setToolTransform(self.translation_floats,atiiaftt.FTUnit.DIST_FT,atiiaftt.FTUnit.ANGLE_RAD)
        new_aunit=ffi.string(self.test_sensor.calibration.cfg.UserTransform.AngleUnits)
        new_dunit=ffi.string(self.test_sensor.calibration.cfg.UserTransform.DistUnits)
        tt_vector=list(self.test_sensor.calibration.cfg.UserTransform.TT)
        logger.debug("{}, {}".format(new_aunit,new_dunit))
        logger.debug("{}".format(tt_vector))
        self.assertEqual(b"rad",new_aunit)
        self.assertEqual(b"ft",new_dunit)
        self.assertEqual(self.translation_floats,tt_vector)
 
    def test_FTSensor_SetTT_FAIL01(self):
        """
        Test that an exception is raised while trying to use the tool transform on an instance with no calibration.
        """
        self.assertRaises(RuntimeError,self.test_sensor.setToolTransform,self.translation_floats,atiiaftt.FTUnit.DIST_MM,atiiaftt.FTUnit.ANGLE_DEG)
 
    def test_FTSensor_SetTT_FAIL02(self):
        """
        Test that an exception is raised while trying to using an invalid unit with the tool transform wrapper function.
        """
        self.test_sensor.createCalibration(self.cal_file,1)
        self.assertRaises(ValueError,self.test_sensor.setToolTransform,self.translation_floats,self.not_a_unit,atiiaftt.FTUnit.ANGLE_DEG)
 
    def test_FTSensor_SetTT_FAIL03(self):
        """
        Test that an exception is raised while trying to using an invalid unit with the tool transform wrapper function.
        """
        self.test_sensor.createCalibration(self.cal_file,1)
        self.assertRaises(ValueError,self.test_sensor.setToolTransform,self.translation_floats,atiiaftt.FTUnit.DIST_MM,self.not_a_unit)
 
    def test_FTSensor_SetForceUnits_OK01(self):
        """
        Test that the setForceUnits wrapper function properly sets 'FORCE_LB' units.
        """
        self.test_sensor.createCalibration(self.cal_file,1)
        self.test_sensor.setForceUnits(atiiaftt.FTUnit.FORCE_LB)
        new_funit=ffi.string(self.test_sensor.calibration.cfg.ForceUnits)
        self.assertEqual(b"lb",new_funit)

    def test_FTSensor_SetForceUnits_OK02(self):
        """
        Test that the setForceUnits wrapper function properly sets 'FORCE_KG' units.
        """
        self.test_sensor.createCalibration(self.cal_file,1)
        self.test_sensor.setForceUnits(atiiaftt.FTUnit.FORCE_KG)
        new_funit=ffi.string(self.test_sensor.calibration.cfg.ForceUnits)
        self.assertEqual(b"kg",new_funit)

    def test_FTSensor_SetForceUnits_OK03(self):
        """
        Test that the setForceUnits wrapper function properly sets 'FORCE_KN' units.
        """
        self.test_sensor.createCalibration(self.cal_file,1)
        self.test_sensor.setForceUnits(atiiaftt.FTUnit.FORCE_KN)
        new_funit=ffi.string(self.test_sensor.calibration.cfg.ForceUnits)
        self.assertEqual(b"kN",new_funit)

    def test_FTSensor_SetForceUnits_OK04(self):
        """
        Test that the setForceUnits wrapper function properly sets 'FORCE_G' units.
        """
        cal_ok=self.test_sensor.createCalibration(self.cal_file,1)
        self.test_sensor.setForceUnits(atiiaftt.FTUnit.FORCE_G)
        new_funit=ffi.string(self.test_sensor.calibration.cfg.ForceUnits)
        self.assertEqual(b"g",new_funit)

    def test_FTSensor_SetForceUnits_OK06(self):
        """
        Test that the setForceUnits wrapper function properly sets 'FORCE_KLB' units.
        """
        cal_ok=self.test_sensor.createCalibration(self.cal_file,1)
        self.test_sensor.setForceUnits(atiiaftt.FTUnit.FORCE_KLB)
        new_funit=ffi.string(self.test_sensor.calibration.cfg.ForceUnits)
        self.assertEqual(b"klb",new_funit)

    def test_FTSensor_SetForceUnits_FAIL01(self):
        """
        Test that an exception is raised when using the setForceUnits wrapper function 
        on an instance with no calibration data.
        """
        self.assertRaises(RuntimeError,self.test_sensor.setForceUnits,atiiaftt.FTUnit.DIST_MM)

    def test_FTSensor_SetForceUnits_FAIL02(self):
        """
        Test that an exception is raised when using the setForceUnits wrapper function 
        on an instance with an incorrect unit.
        """
        cal_ok=self.test_sensor.createCalibration(self.cal_file,1)
        self.assertRaises(ValueError,self.test_sensor.setForceUnits,self.not_a_unit)

    def test_FTSensor_SetTorqueUnits_OK01(self):
        """
        Test that the setTorqueUnits wrapper function properly sets 'TORQUE_IN_LB' units.
        """
        cal_ok=self.test_sensor.createCalibration(self.cal_file,1)
        self.test_sensor.setTorqueUnits(atiiaftt.FTUnit.TORQUE_IN_LB)
        new_tunit=ffi.string(self.test_sensor.calibration.cfg.TorqueUnits)
        self.assertEqual(b"in-lb",new_tunit)

    def test_FTSensor_SetTorqueUnits_OK02(self):
        """
        Test that the setTorqueUnits wrapper function properly sets 'TORQUE_N_M' units.
        """
        cal_ok=self.test_sensor.createCalibration(self.cal_file,1)
        self.test_sensor.setTorqueUnits(atiiaftt.FTUnit.TORQUE_N_M)
        new_tunit=ffi.string(self.test_sensor.calibration.cfg.TorqueUnits)
        self.assertEqual(b"N-m",new_tunit)

    def test_FTSensor_SetTorqueUnits_OK03(self):
        """
        Test that the setTorqueUnits wrapper function properly sets 'TORQUE_N_MM' units.
        """
        cal_ok=self.test_sensor.createCalibration(self.cal_file,1)
        self.test_sensor.setTorqueUnits(atiiaftt.FTUnit.TORQUE_N_MM)
        new_tunit=ffi.string(self.test_sensor.calibration.cfg.TorqueUnits)
        self.assertEqual(b"N-mm",new_tunit)

    def test_FTSensor_SetTorqueUnits_OK04(self):
        """
        Test that the setTorqueUnits wrapper function properly sets 'TORQUE_KG_CM' units.
        """
        cal_ok=self.test_sensor.createCalibration(self.cal_file,1)
        self.test_sensor.setTorqueUnits(atiiaftt.FTUnit.TORQUE_KG_CM)
        new_tunit=ffi.string(self.test_sensor.calibration.cfg.TorqueUnits)
        self.assertEqual(b"kg-cm",new_tunit)

    def test_FTSensor_SetTorqueUnits_FAIL01(self):
        """
        Test that an exception is raised when using the setTorqueUnits wrapper function 
        on an instance with no calibration data.
        """
        self.assertRaises(RuntimeError,self.test_sensor.setTorqueUnits,atiiaftt.FTUnit.TORQUE_IN_LB)

    def test_FTSensor_SetTorqueUnits_FAIL02(self):
        """
        Test that an exception is raised when using the setTorqueUnits wrapper function 
        on an instance with an incorrect unit.
        """
        cal_ok=self.test_sensor.createCalibration(self.cal_file,1)
        self.assertRaises(ValueError,self.test_sensor.setTorqueUnits,self.not_a_unit)

    def test_FTSensor_ConvertToFt_OK01(self):
        """
        Test the convertToFt wrapper function with a specific tool transform and units.
        """
        cal_ok=self.test_sensor.createCalibration(self.cal_file,1)
        self.test_sensor.bias(self.bias_readings)
        self.test_sensor.setToolTransform(self.translation_floats,atiiaftt.FTUnit.DIST_MM,atiiaftt.FTUnit.ANGLE_DEG)
        self.test_sensor.setTorqueUnits(atiiaftt.FTUnit.TORQUE_N_M)
        self.test_sensor.setForceUnits(atiiaftt.FTUnit.FORCE_N)
        self.test_sensor.convertToFt(self.input_floats)
        logger.debug(self.test_sensor.ft_vector)
        rnd_ft_vector=[]
        for c_ft in self.test_sensor.ft_vector:
            rnd_ft_vector.append(round(c_ft,6))
        logger.debug(rnd_ft_vector)
        self.assertEqual(self.output_floats_n,rnd_ft_vector)

    def test_FTSensor_ConvertToFt_OK02(self):
        """
        Test the convertToFt wrapper function with a specific tool transform and units.
        """
        cal_ok=self.test_sensor.createCalibration(self.cal_file,1)
        self.test_sensor.bias(self.bias_readings)
        self.test_sensor.setToolTransform(self.translation_floats,atiiaftt.FTUnit.DIST_MM,atiiaftt.FTUnit.ANGLE_DEG)
        self.test_sensor.setTorqueUnits(atiiaftt.FTUnit.TORQUE_N_M)
        self.test_sensor.setForceUnits(atiiaftt.FTUnit.FORCE_KN)
        self.test_sensor.convertToFt(self.input_floats)
        rnd_ft_vector=[]
        for c_ft in self.test_sensor.ft_vector:
            rnd_ft_vector.append(round(c_ft,6))
        logger.debug(rnd_ft_vector)
        self.assertEqual(self.output_floats_kn,rnd_ft_vector)

    def test_FTSensor_ConvertToFt_OK03(self):
        """
        Test the convertToFt wrapper function stores the last conversion values.
        """
        cal_ok=self.test_sensor.createCalibration(self.cal_file,1)
        self.test_sensor.bias(self.bias_readings)
        self.test_sensor.setToolTransform(self.translation_floats,atiiaftt.FTUnit.DIST_MM,atiiaftt.FTUnit.ANGLE_DEG)
        self.test_sensor.setTorqueUnits(atiiaftt.FTUnit.TORQUE_N_M)
        self.test_sensor.setForceUnits(atiiaftt.FTUnit.FORCE_N)
        ft_readings=self.test_sensor.convertToFt(self.input_floats)
        self.assertEqual(self.test_sensor.ft_vector,ft_readings)

    def test_FTSensor_ConvertToFt_FAIL01(self):
        """
        Test that an exception is raised when the convertToFt wrapper function is used on an instance with
        no calibration data.
        """
        self.assertRaises(RuntimeError,self.test_sensor.convertToFt,self.input_floats)


if __name__ == "__main__":

    unittest.main()
