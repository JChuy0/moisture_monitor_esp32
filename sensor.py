"""This module handles the sensor."""

from machine import ADC, Pin
import time

class Sensor:
    """The sensor class."""

    global a0
    a0 = ADC(Pin(36))
    a0.atten(ADC.ATTN_11DB)

    def moisture():
        """Handles the moisture sensor and returns a dictionary."""

        now = time.time()
        year, month, day, hour, minute, sec, _, _ = time.localtime(now - 21600)
        
        raw = a0.read()
        percent = (100 * raw / 4095)
        volts = (3.3 * raw / 4095)
        timestamp = f"{year}-{month}-{day} {hour}:{minute}:{sec}"

        moisture_dict = {"raw": raw, "percent": percent, "volts": volts, "timestamp": timestamp}

        return moisture_dict