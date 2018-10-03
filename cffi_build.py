import os
from cffi import FFI

ffibuilder = FFI()

# have this build script with the ATIDAQ source for now
PATH = os.path.dirname(__file__)

with open(os.path.join(PATH, 'ATIDAQ_c_lib/ATIDAQ/ftconfig.h'),'r') as f:
    ffibuilder.set_source("_atiiaftt", f.read(),
                          sources=[os.path.join(PATH,'ATIDAQ_c_lib/ATIDAQ/ftconfig.c'),
                                   os.path.join(PATH,'ATIDAQ_c_lib/ATIDAQ/ftrt.c'),
                                   os.path.join(PATH,'ATIDAQ_c_lib/ATIDAQ/dom.c'),
                                   os.path.join(PATH,'ATIDAQ_c_lib/ATIDAQ/expatls.c'),
                                   os.path.join(PATH,'ATIDAQ_c_lib/ATIDAQ/node.c'),
                                   os.path.join(PATH,'ATIDAQ_c_lib/ATIDAQ/stack.c'),
                                   os.path.join(PATH,'ATIDAQ_c_lib/ATIDAQ/xmlparse.c'),
                                   os.path.join(PATH,'ATIDAQ_c_lib/ATIDAQ/xmlrole.c'),
                                   os.path.join(PATH,'ATIDAQ_c_lib/ATIDAQ/xmltok.c')
                                   ],
                          include_dirs=[os.path.join(PATH,'ATIDAQ_c_lib/ATIDAQ')]
                          )

ffibuilder.cdef(
    """
    #define MAX_AXES 6
    #define MAX_GAUGES 8

    typedef char *Units;
    typedef struct Configuration Configuration;
    typedef struct Calibration Calibration;
    typedef struct Transform Transform;
    typedef int BOOL;

    typedef struct RTCoefs RTCoefs;

    struct RTCoefs {
        unsigned short NumChannels;
        unsigned short NumAxes;
        float working_matrix[MAX_AXES][MAX_GAUGES];
        float bias_slopes[MAX_GAUGES];
        float gain_slopes[MAX_GAUGES];
        float thermistor;
        float bias_vector[MAX_GAUGES+1];
        float TCbias_vector[MAX_GAUGES];
    };

    struct Transform {
        float TT[6];
        Units DistUnits;
        Units AngleUnits;
    };


    struct Configuration {
        Units ForceUnits;        // force units of output
        Units TorqueUnits;       // torque units of output
        Transform UserTransform; // coordinate system transform set by user
        BOOL TempCompEnabled;    // is temperature compensation enabled?
    };

    struct Calibration {
        float BasicMatrix[MAX_AXES][MAX_GAUGES];
        Units ForceUnits;
        Units TorqueUnits;
        BOOL TempCompAvailable;
        Transform BasicTransform;
        float MaxLoads[MAX_AXES];
        char *AxisNames[MAX_AXES];
        char *Serial;
        char *BodyStyle;
        char *PartNumber;
        char *Family;
        char *CalDate;
        Configuration cfg;
        RTCoefs rt;
    };

    Calibration *createCalibration(char *CalFilePath, unsigned short index);
    void destroyCalibration(Calibration *cal);
    short SetToolTransform(Calibration *cal, float Vector[6],char *DistUnits,char *AngleUnits);
    short SetForceUnits(Calibration *cal, char *NewUnits);
    short SetTorqueUnits(Calibration *cal, char *NewUnits);
    void Bias(Calibration *cal, float voltages[]);
    void ConvertToFT(Calibration *cal, float voltages[],float result[]);

    """
    )

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
