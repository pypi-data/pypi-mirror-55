cdef extern from "iarduino_I2C_Expander.cpp":
	pass

cdef extern from "iarduino_I2C_Expander.h":
	cdef cppclass iarduino_I2C_Expander:
		iarduino_I2C_Expander() except +
		iarduino_I2C_Expander(unsigned char) except +
		bint begin()
		bint changeAddress(unsigned char)
		bint reset()
		unsigned char getAddress()
		unsigned char getVersion()
		void pinMode(unsigned char, unsigned char, unsigned char)
		void pinPull(unsigned char, unsigned char)
		void pinOutScheme(unsigned char, unsigned char)
		void digitalWrite(unsigned char, unsigned char)
		unsigned char digitalRead(unsigned char)
		void analogWrite(unsigned char, unsigned short)
		unsigned short analogRead(unsigned char)
		void analogAveraging(unsigned char)
		void levelWrite(unsigned short)
		unsigned char levelRead(unsigned char)
		void levelHyst(unsigned short)
		void freqPWM(unsigned short)
		void servoAttach(unsigned char, unsigned short, unsigned short, short, short)
		void servoWrite(unsigned char, short)
		void servoWriteMicroseconds(unsigned char, unsigned short)
		long map(long, long, long, long, long)
		void changeBus(char*)
