[![ITG3200](ITG3200_I2C.png)](https://store.ncd.io/product/itg-3200-16-bit-3-axis-mems-gyro-angular-rate-sensors-i2c-mini-module/).

# ITG3200

This is InvenSense’s ITG-3200, a groundbreaking triple-axis, digital output MEMS gyroscope.The ITG-3200 features three 16-bit analog-to-digital converters (ADCs) for digitizing the gyro outputs, a user-selectable internal low-pass filter bandwidth, and a Fast-Mode I2C (400kHz) interface.
This Device is available from www.ncd.io

[SKU: ITG3200]

(https://store.ncd.io/product/itg-3200-16-bit-3-axis-mems-gyro-angular-rate-sensors-i2c-mini-module/)
This Sample code can be used with Raspberry Pi.

Hardware needed to interface ITG3200 3Axis gyro angular sensor With Raspberry Pi :

1. <a href="https://store.ncd.io/product/itg-3200-16-bit-3-axis-mems-gyro-angular-rate-sensors-i2c-mini-module/">ITG3200 16Bit 3Axis gyro angular Sensor</a>

2. <a href="https://store.ncd.io/product/i2c-shield-for-raspberry-pi-3-pi2-with-outward-facing-i2c-port-terminates-over-hdmi-port/">Raspberry Pi I2C Shield</a>

3. <a href="https://store.ncd.io/product/i%C2%B2c-cable/">I2C Cable</a>

## Python

Download and install smbus library on Raspberry pi. Steps to install smbus are provided at:

https://pypi.python.org/pypi/smbus-cffi/0.5.1

Download (or git pull) the code in pi. Run the program.

```cpp
$> python ITG3200.py
```
The lib is a sample library, you will need to calibrate the sensor according to your application requirement.
