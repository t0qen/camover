#!/usr/bin/env python3
import smbus
import struct
import time

# Bus I2C (1 = /dev/i2c-1)
bus = smbus.SMBus(1)
I2C_ADDRESS = 0x08  # Adresse de la XIAO

while True:
    try:
        # Lire 4 octets depuis l'adresse I2C
        data = bus.read_i2c_block_data(I2C_ADDRESS, 0, 4)
        # Convertir les 4 octets en float (little-endian)
        vin = struct.unpack('<f', bytes(data))[0]
        print(f"Tension batterie: {vin:.2f}V")
    except Exception as e:
        print(f"Erreur: {e}")
    time.sleep(2)  # Attendre 2 secondes
