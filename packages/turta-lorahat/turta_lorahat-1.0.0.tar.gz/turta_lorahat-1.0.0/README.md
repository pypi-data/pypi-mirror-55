# Turta LoRa HAT for Raspberry Pi
LoRa HAT is a long-range communication transceiver for Raspberry Pi.

## Features
- Carries LoRa Transceiver module with onboard LoRaWAN Protocol Stack.
- Securely connects to the cloud services via Cryptographic co-processor.
- Detects theft attempts via accel-tilt sensor.
- Has Grove compatible I2C, digital and analog ports.
- 4Ch single-ended or 2Ch differential analog inputs are available.
- Three LEDs for status indication.
- Stackable design; most of the GPIO pins are free.
- ID EEPROM for Raspberry Pi HAT specification compliance.

## Raspberry Pi Configuration
* You should enable SPI and I2C from the Raspberry Pi's configuration. To do so, type 'sudo raspi-config' to the terminal, then go to 'Interfacing Options' and enable both SPI and I2C.
* You should swap the serial ports of the Raspberry Pi. Set "/dev/ttyAMA0" to 'serial0'. Also, disable the console on 'serial0'. For a how-to, visit our documentation at [docs.turta.io](https://docs.turta.io/how-tos/raspberry-pi/raspbian/swapping-the-serial-ports).

## Documentation
Visit [docs.turta.io](https://docs.turta.io) for documentation.
