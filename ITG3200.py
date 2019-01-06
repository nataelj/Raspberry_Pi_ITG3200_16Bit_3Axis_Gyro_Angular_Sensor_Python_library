# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# ITG3200
# This code is designed to work with the ITG-3200_I2CS I2C Mini Module available from ControlEverything.com.
# https:#www.controleverything.com/content/Gyro?sku=ITG-3200_I2CS#tabs-0-product_tabset-2

import smbus
import time

# sensitivity and offset
TEMP_SENSITIVITY = 280 # 280 LSB per °C
TEMP_OFFSET = (13200 + 35*TEMP_SENSITIVITY) # 13200 LSB + 35°C
GYRO_SENSITIVITY = 14.375 # 14.375 LSB per °/s

# Get I2C bus
bus = smbus.SMBus(1)

# I2C address of the device
ITG3200_DEFAULT_ADDRESS				= 0x68

# ITG3200 Register Map
ITG3200_WHO_AM_I					= 0x00 # Who Am I Register
ITG3200_SMPLRT_DIV					= 0x15 # Sample Rate Divider
ITG3200_DLPF_PS						= 0x16 # Digital Low Pass Filter Register
ITG3200_INT_CFG						= 0x17 # Interrupt Configuration
ITG3200_INT_STATUS					= 0x1A # Interrupt Status
ITG3200_TEMP_OUT_H					= 0x1B # Temperature High Byte
ITG3200_TEMP_OUT_L					= 0x1C # Temperature Low Byte
ITG3200_GYRO_XOUT_H					= 0x1D # X-Axis High Byte
ITG3200_GYRO_XOUT_L					= 0x1E # X-Axis Low Byte
ITG3200_GYRO_YOUT_H					= 0x1F # Y-Axis High Byte
ITG3200_GYRO_YOUT_L					= 0x20 # Y-Axis Low Byte
ITG3200_GYRO_ZOUT_H					= 0x21 # Z-Axis High Byte
ITG3200_GYRO_ZOUT_L					= 0x22 # Z-Axis Low Byte
ITG3200_PWR_MGM						= 0x3E # Power Management

# ITG3200 Digital Low Pass Filter Register
ITG3200_FULLSCALE_2000				= 0x18 # Gyro Full-Scale Range = +/-2000 per sec
ITG3200_DLPF_BW_256					= 0x00 # Bandwidth = 256Hz
ITG3200_DLPF_BW_188					= 0x01 # Bandwidth = 188Hz
ITG3200_DLPF_BW_98					= 0x02 # Bandwidth = 98Hz
ITG3200_DLPF_BW_42					= 0x03 # Bandwidth = 42Hz
ITG3200_DLPF_BW_20					= 0x04 # Bandwidth = 20Hz
ITG3200_DLPF_BW_10					= 0x05 # Bandwidth = 10Hz
ITG3200_DLPF_BW_5					= 0x06 # Bandwidth = 5Hz

# ITG3200 Interrupt Config Register
ITG_3200_REG_GYRO_INTCNF_ACTL_MASK 				= 0x80      # Logic level for INT Output Pin
ITG_3200_REG_GYRO_INTCNF_ACTL_HIGH            	= 0x00      # Active High
ITG_3200_REG_GYRO_INTCNF_ACTL_LOW               = 0x80      # Active Low

ITG_3200_REG_GYRO_INTCNF_OPEN_MASK              = 0x40      # Drive Type for INT Output Pin
ITG_3200_REG_GYRO_INTCNF_OPEN_PUSH_PULL         = 0x00      # Push-Pull
ITG_3200_REG_GYRO_INTCNF_OPEN_OPEN              = 0x40      # Open Drain

ITG_3200_REG_GYRO_INTCNF_LATCH_INT_EN_MASK      = 0x20      # Latch Mode
ITG_3200_REG_GYRO_INTCNF_LATCH_INT_EN_50US      = 0x00      # 50us Pulse
ITG_3200_REG_GYRO_INTCNF_LATCH_INT_EN_LATCH     = 0x20      # Latch until Interrupt is Cleared

ITG_3200_REG_GYRO_INTCNF_INT_ANYRD_2CLEAR_MASK  = 0x10      # Latch Clear Method
ITG_3200_REG_GYRO_INTCNF_INT_ANYRD_2CLEAR_STAT  = 0x00      # Status Register Read Only
ITG_3200_REG_GYRO_INTCNF_INT_ANYRD_2CLEAR_ANY   = 0x10      # Any Register Read

ITG_3200_REG_GYRO_INTCNF_INT_ITG_RDY_EN_MASK    = 0x04      # Interrupt Status when Device is Ready (PLL Ready after changing Clock Source)
ITG_3200_REG_GYRO_INTCNF_INT_ITG_RDY_EN_DISABLE = 0x00      # Disable Interrupt when Device is Ready (PLL Ready after changing Clock Source)
ITG_3200_REG_GYRO_INTCNF_INT_ITG_RDY_EN_ENABLE  = 0x04      # Enable Interrupt when Device is Ready (PLL Ready after changing Clock Source)

ITG_3200_REG_GYRO_INTCNF_INT_RAW_RDY_EN_MASK    = 0x01      # Interrupt Status when Data is Ready
ITG_3200_REG_GYRO_INTCNF_INT_RAW_RDY_EN_DISABLE = 0x00      # Disable Interrupt when Data is Ready
ITG_3200_REG_GYRO_INTCNF_INT_RAW_RDY_EN_ENABLE  = 0x01      # Enable Interrupt when Data is Ready

#INTERRUPT STATUS REGISTER
ITG_3200_REG_GYRO_INTSTAT_INT_ITG_RDY_MASK      = 0x04      # PLL Ready Status
ITG_3200_REG_GYRO_INTSTAT_INT_ITG_RDY_NOT       = 0x00      # PLL Not Ready
ITG_3200_REG_GYRO_INTSTAT_INT_ITG_RDY_READY     = 0x04      # PLL Ready

ITG_3200_REG_GYRO_INTSTAT_INT_RAW_RDY_MASK      = 0x01      # Raw Data Ready Status
ITG_3200_REG_GYRO_INTSTAT_INT_RAW_RDY_NOT       = 0x00      # Raw Data Not Ready
ITG_3200_REG_GYRO_INTSTAT_INT_RAW_RDY_READY     = 0x01      # Raw Data is Ready

# ITG3200 Power Management Register
ITG3200_PWR_H_RESET					= 0x80 # Reset device and internal registers to the power-up-default settings
ITG3200_PWR_SLEEP					= 0x40 # Enable low power sleep mode
ITG3200_PWR_NRML_X_Y_Z				= 0x00 # Put all gyro axis in normal mode
ITG3200_PWR_STBY_XG					= 0x20 # Put gyro X in standby mode
ITG3200_PWR_STBY_YG					= 0x10 # Put gyro Y in standby mode
ITG3200_PWR_STBY_ZG					= 0x08 # Put gyro Z in standby mode
ITG3200_CLOCK_INTERNAL				= 0x00 # Internal oscillator
ITG3200_CLOCK_PLL_XGYRO				= 0x01 # PLL with X Gyro reference
ITG3200_CLOCK_PLL_YGYRO				= 0x02 # PLL with Y Gyro reference
ITG3200_CLOCK_PLL_ZGYRO				= 0x03 # PLL with Z Gyro reference
ITG3200_CLOCK_PLL_EXT32K			= 0x04 # PLL with external 32.768kHz reference
ITG3200_CLOCK_PLL_EXT19M			= 0x05 # PLL with external 19.2MHz reference

calibration =[ 105.10601, -16.84151, 12.15584] #Zero offsets, X,Y,Z

# TODO Add interrupt managing capability - cpp examples at https:#github.com/Cameri/Itg3200 and https://github.com/ncdcommunity/Arduino_Library_ITG3200_16Bit_3Axis_Gyro_Angular_Sensor

class ITG3200():
	def __init__(self):
		self.power_configuration()
		self.fullscale_configuration()

	def __del__(self):
		# Set the sleep bit to on in the power management register to sleep the device
		bus.write_byte_data(ITG3200_DEFAULT_ADDRESS,ITG3200_PWR_MGM, ITG3200_PWR_SLEEP)
	
	def power_configuration(self):
		"""Select the Power Management Register configuration of the gyroscope from the given provided values"""
		POWER_CONFIG = (ITG3200_CLOCK_PLL_XGYRO | ITG3200_PWR_NRML_X_Y_Z) # Note: This is a bitwise or operator to set the appropriate bits on the power management register
		bus.write_byte_data(ITG3200_DEFAULT_ADDRESS, ITG3200_PWR_MGM, POWER_CONFIG)
		

	def verify_device_identity(self):
		return bus.read_byte_data(ITG3200_DEFAULT_ADDRESS,ITG3200_WHO_AM_I)
	
	def fullscale_configuration(self):
		"""Select the Digital Low Pass Filter Register configuration of the gyroscope from the given provided values"""
		FULLSCALE_CONFIG = (ITG3200_FULLSCALE_2000 | ITG3200_DLPF_BW_256)
		bus.write_byte_data(ITG3200_DEFAULT_ADDRESS, ITG3200_DLPF_PS, FULLSCALE_CONFIG)

	def read_temperature(self):
		"""Read data back from ITG3200_TEMP_OUT_H(0x1B), 2 bytes
		Adjust by offset and scale by sensitivity and then return.
		Temperature given in degrees C"""
		# Read a block of 2 bytes from ITG3200_DEFAULT_ADDRESS, offset ITG3200_TEMP_OUT_H
		data = bus.read_i2c_block_data(ITG3200_DEFAULT_ADDRESS, ITG3200_TEMP_OUT_H, 2)

		# Convert the first two bytes (presumably the high and low) to an unsigned int equivalent
		temp = data[0] * 256 + data[1]
		if temp > 32767 : # If value is indeed an unsigned int equivalent (e.g. 0 to 65,535) in 2's complement format
			temp -= 65536 # Convert it to signed int equivalent (-32,767 to 32,767)

		temp+=TEMP_OFFSET # Add temperature offset
		temp/=TEMP_SENSITIVITY # Scale by temperature sensitivity
		# TODO Check this- maybe need a negative sign here? Check for inversion need

		return temp
	
	def read_gyro_raw(self):
		"""Read data back from ITG3200_GYRO_XOUT_H(0x1D), 6 bytes
		X-Axis MSB, X-Axis LSB, Y-Axis MSB, Y-Axis LSB, Z-Axis MSB, Z-Axis LSB
		Data returned as a dictionary with keys x, y, and z and values in units of LSB."""
		# Read a block of 6 bytes from ITG3200_DEFAULT_ADDRESS, offset ITG3200_GYRO_XOUT_H
		data = bus.read_i2c_block_data(ITG3200_DEFAULT_ADDRESS, ITG3200_GYRO_XOUT_H, 6)
		
		# Convert the first two bytes (presumably the high and low) to an unsigned int equivalent
		xGyro = data[0] * 256 + data[1]
		if xGyro > 32767 : # If value is indeed an unsigned int equivalent (e.g. 0 to 65,535) in 2's complement format
			xGyro -= 65536 # Convert it to signed int equivalent (-32,767 to 32,767)
		
		# Convert the next two bytes (presumably the high and low) to an unsigned int equivalent
		yGyro = data[2] * 256 + data[3]
		if yGyro > 32767 : # If value is an unsigned int equivalent (e.g. 0 to 65,535) in 2's complement format
			yGyro -= 65536 # Convert it to signed int equivalent (-32,767 to 32,767)
		
		# Convert the next two bytes (presumably the high and low) to an unsigned int equivalent
		zGyro = data[4] * 256 + data[5]
		if zGyro > 32767 : # If value is an unsigned int equivalent (e.g. 0 to 65,535) in 2's complement format
			zGyro -= 65536 # Convert it to signed int equivalent (-32,767 to 32,767)
			
		#Apply calibrations
		xGyro = xGyro + calibration[0]
		yGyro = yGyro + calibration[1]
		zGyro = zGyro + calibration[2]
		
		# Return a new dictionary
		return {'x' : xGyro, 'y' : yGyro, 'z' : zGyro}

	def read_gyro(self):
		"""Read raw data from gyro and then scale it and return.
		Data returned as a dictionary with keys x, y, and z and values in degrees/S."""
		data=self.read_gyro_raw() # Read the raw values

		# Scale the values by the sensitivity
		xGyro=data['x']/GYRO_SENSITIVITY
		yGyro=data['y']/GYRO_SENSITIVITY
		zGyro=data['z']/GYRO_SENSITIVITY

		# Return a new dictionary
		return {'x' : xGyro, 'y' : yGyro, 'z' : zGyro}


if __name__ == "__main__":
    # if run directly we'll just create an instance of the class and output the current readings
	itg3200 = ITG3200()

	print('device id',itg3200.verify_device_identity())

	while True :
		itg3200.power_configuration()
		itg3200.fullscale_configuration()
		time.sleep(0.5)
		gyro = itg3200.read_gyro_raw()
		print("Raw data readings, use to calibrate")
		print("X-Axis of Rotation : %d" %(gyro['x']))
		print("Y-Axis of Rotation : %d" %(gyro['y']))
		print("Z-Axis of Rotation : %d" %(gyro['z']))
		print(" ************************************* ")
		gyro = itg3200.read_gyro()
		print("Scaled data readings in degrees")
		print("X-Axis of Rotation : %d" %(gyro['x']))
		print("Y-Axis of Rotation : %d" %(gyro['y']))
		print("Z-Axis of Rotation : %d" %(gyro['z']))
		print(" ************************************* ")
		time.sleep(0.5)
