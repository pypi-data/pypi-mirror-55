# distutils: language = c++
# cython: language_level = 3

DEF_CHIP_ID_FLASH =  0x3C        
DEF_CHIP_ID_METRO =  0xC3        
DEF_MODEL_EXP   =   0x07        

# Адреса регистров модуля:      
REG_FLAGS_0 = 0x00
REG_BITS_0  = 0x01
REG_FLAGS_1 = 0x02
REG_BITS_1 = 0x03
REG_MODEL = 0x04
REG_VERSION = 0x05
REG_ADDRESS = 0x06
REG_CHIP_ID = 0x07
REG_EXP_FREQUENCY_L = 0x08
REG_EXP_FREQUENCY_H = 0x09
REG_EXP_LEVEL_L = 0x0A
REG_EXP_LEVEL_H = 0x0B
REG_EXP_HYSTERESIS_L= 0x0C
REG_EXP_HYSTERESIS_H= 0x0D
REG_EXP_AVERAGING = 0x0E
REG_EXP_DIRECTION = 0x10
REG_EXP_TYPE = 0x11
REG_EXP_PULL_UP = 0x12
REG_EXP_PULL_DOWN = 0x13
REG_EXP_OUT_MODE = 0x14
REG_EXP_DIGITAL = 0x15
REG_EXP_WRITE_HIGH = 0x16
REG_EXP_WRITE_LOW  = 0x17
REG_EXP_ANALOG = 0x18
EXP_BIT_DIR = 0x80
EXP_BIT_TYP = 0x40
EXP_BIT_PUP = 0x20
EXP_BIT_PDN = 0x10
EXP_BIT_SCH = 0x08
LOW = 0
HIGH = 1
INPUT = 0
OUTPUT = 1
DIGITAL = 2
ANALOG = 3
SERVO = 4
OUT_PUSH_PULL = 5
OUT_OPEN_DRAIN = 6
PULL_UP = 7
PULL_DOWN = 8
PULL_NO = 0xFF
ALL_PIN = 0xFF

NO_BEGIN = 1

from iarduino_I2C_Expander cimport iarduino_I2C_Expander

cdef class pyiArduinoI2Cexpander:
    cdef iarduino_I2C_Expander c_expander

    def __cinit__(self, address=None, auto=None):
        if address is not None:
            self.c_expander = iarduino_I2C_Expander(address)
            if auto is None:
                self.c_expander.begin()
        else:
            self.c_expander = iarduino_I2C_Expander()
            if auto is None:
                self.c_expander.begin()

    def begin(self):
        return self.c_expander.begin()

    def changeAddress(self, unsigned char newAddr):
        return self.c_expander.changeAddress(newAddr)

    def reset(self):
        return self.c_expander.reset()

    def getAddress(self):
        return self.c_expander.getAddress()

    def getVersion(self):
        return self.c_expander.getVersion()

    def pinMode(self, unsigned char pin, unsigned char io_dir, unsigned char io_type=0xff):
        if io_type is not 0xff:
            self.c_expander.pinMode(pin, io_dir, io_type)
        else:
            self.c_expander.pinMode(pin, io_dir, 0xff)

    def pinPull(self, unsigned char pin, unsigned char pull):
        self.c_expander.pinPull(pin, pull)

    def pinOutScheme(self, unsigned char pin, unsigned char mode):
        self.c_expander.pinOutScheme(pin, mode)

    def digitalWrite(self, unsigned char pin, unsigned char level):
        self.c_expander.digitalWrite(pin, level)

    def digitalRead(self, unsigned char pin):
        return self.c_expander.digitalRead(pin)

    def analogWrite(self, unsigned char pin, unsigned short level):
        self.c_expander.analogWrite(pin, level)

    def analogRead(self, unsigned char pin):
        return self.c_expander.analogRead(pin)

    def analogAveraging(self, unsigned char coefficient):
        self.c_expander.analogAveraging(coefficient)

    def levelWrite(self, unsigned short level):
        self.c_expander.levelWrite(level)

    def levelRead(self, unsigned char pin):
        return self.c_expander.levelRead(pin)

    def levelHyst(self, unsigned short hysteresis):
        self.c_expander.levelHyst(hysteresis)

    def freqPWM(self, unsigned short frequency):
        self.c_expander.freqPWM(frequency)

    def servoAttach(self, unsigned char pin, unsigned short width_min, unsigned short width_max, short angle_min, short angle_max):
        self.c_expander.servoAttach(pin, width_min, width_max, angle_min, angle_max)

    def servoWrite(self, unsigned char pin, short angle):
        self.c_expander.servoWrite(pin, angle)

    def servoWriteMicroseconds(self, unsigned char pin, unsigned short width):
        self.c_expander.servoWriteMicroseconds(pin, width)

    def changeBus(self, char* bus):
        self.c_expander.changeBus(bus)

    def mymap(self, long x, long in_min, long in_max, long out_min, long out_max):
        return self.c_expander.map(x, in_min, in_max, out_min, out_max)
