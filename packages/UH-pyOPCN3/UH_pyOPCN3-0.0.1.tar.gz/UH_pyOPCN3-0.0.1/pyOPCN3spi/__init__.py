from time import sleep
from gpiozero import DigitalOutputDevice
import spidev
import struct


class OPCN3(object):
    """
    A OPCN3 Object to be used as an SPI slave, uses SPI 0 on pi0 by default (mode 1)
    :param cs_gpio: Which GPIO pin is the chip select (slave select) for this OPC
    """
    def __init__(self, cs_gpio):

        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.mode = 1
        self.spi.max_speed_hz = 300000
        self.cs = DigitalOutputDevice(cs_gpio, initial_value=True)
        self.cs.on()

        self.info_string = ""
        self.serial_string = ""

        self.bbs_adc = []
        self.bbs_um = []
        self.bws = []
        self.PMd_A_um = 0
        self.PMd_B_um = 0
        self.PMd_C_um = 0
        self.max_ToF = 0
        self.AM_sample_interval_count = 0
        self.AM_idle_interval_count = 0
        self.AM_max_data_arrays_in_file = 0
        self.AM_only_save_PM = 0
        self.AM_fan_on_idle = 0
        self.AM_laser_on_idle = 0
        self.ToF_SFR_factor = 0
        self.PVP = 0
        self.bin_weighting_index = 0

        self.hist = []
        self.mtof = []
        self.period = 0
        self.checksum = 0
        self.reject_glitch = 0
        self.reject_ratio = 0
        self.reject_ltof = 0
        self.flow_rate = 0
        self.temp_degC = 0
        self.RH_true = 0
        self.PM_A_ugm3 = 0
        self.PM_B_ugm3 = 0
        self.PM_C_ugm3 = 0
        self.reject_range = 0
        self.fan_revs = 0
        self.laser_status = 0

    def command_byte(self, command):
        self.cs.off()
        response = 0x00
        timeout = 0
        while response != 0xF3:
            timeout += 1
            if timeout > 20:
                raise RuntimeError("Not receiving correct response from OPC-N3")
            response = self.spi.xfer2(command)[0]
            sleep(0.001)

    def read_info_string(self):
        self.info_string = ""
        self.command_byte([0x3F])
        for i in range(60):
            sleep(0.00001)
            buf = self.spi.xfer2([0x01])[0]
            self.info_string += chr(buf)
        self.cs.on()

    def read_serial_string(self):
        self.serial_string = ""
        self.command_byte([0x01])
        for i in range(60):
            sleep(0.00001)
            buf = self.spi.xfer2([0x01])[0]
            self.serial_string += chr(buf)
        self.cs.on()

    def read_config_vars(self):
        self.command_byte([0x3C])
        self.bbs_adc = []
        self.bbs_um = []
        raw = []
        for i in range(168):
            sleep(0.00001)
            buf = self.spi.xfer2([0x01])[0]
            raw.append(buf)
        self.cs.on()
        index = 0
        for i in range(25):
            self.bbs_adc.append(byte_to_int16(raw[index*2], raw[index*2+1]))
            index += 2
        for i in range(25):
            self.bbs_um.append(byte_to_int16(raw[index*2], raw[index*2+1]))
            index += 2
        for i in range(24):
            self.bws.append(byte_to_int16(raw[index*2], raw[index*2+1]))
            index += 2
        self.PMd_A_um = byte_to_int16(raw[index], raw[index+1])
        self.PMd_B_um = byte_to_int16(raw[index+2], raw[index+3])
        self.PMd_C_um = byte_to_int16(raw[index+4], raw[index+5])
        self.max_ToF = byte_to_int16(raw[index+6], raw[index+7])
        self.AM_sample_interval_count = byte_to_int16(raw[index+8], raw[index+9])
        self.AM_idle_interval_count = byte_to_int16(raw[index+10], raw[index+11])
        self.AM_max_data_arrays_in_file = byte_to_int16(raw[index+12], raw[index+13])
        self.AM_only_save_PM = raw[index+14]
        self.AM_fan_on_idle = raw[index+15]
        self.AM_laser_on_idle = raw[index+16]
        self.ToF_SFR_factor = raw[index+17]
        self.PVP = raw[index+18]
        self.bin_weighting_index = raw[index+19]

    def read_histogram_data(self):
        self.command_byte([0x30])
        self.hist = []
        self.mtof = []
        raw = []
        index = 0
        for i in range(86):
            sleep(0.00001)
            buf = self.spi.xfer2([0x01])[0]
            raw.append(buf)
        self.cs.on()
        for i in range(24):
            self.hist.append(byte_to_int16(raw[i*2], raw[i*2+1]))
            index = index+2
        for i in range(4):
            self.mtof.append(raw[index])
            index = index+1
        self.period = byte_to_int16(raw[index], raw[index+1])
        self.flow_rate = byte_to_int16(raw[index+2], raw[index+3])
        self.temp_degC = byte_to_int16(raw[index+4], raw[index+5])
        self.RH_true = byte_to_int16(raw[index+6], raw[index+7])
        self.PM_A_ugm3 = byte_to_float(raw[index+8], raw[index+9], raw[index+10], raw[index+11])
        self.PM_B_ugm3 = byte_to_float(raw[index + 12], raw[index + 13], raw[index + 14], raw[index + 15])
        self.PM_C_ugm3 = byte_to_float(raw[index + 16], raw[index + 17], raw[index + 18], raw[index + 19])
        self.reject_glitch = byte_to_int16(raw[index + 20], raw[index + 21])
        self.reject_ltof = byte_to_int16(raw[index + 22], raw[index + 23])
        self.reject_ratio = byte_to_int16(raw[index + 24], raw[index + 25])
        self.reject_range = byte_to_int16(raw[index + 26], raw[index + 27])
        self.fan_revs = byte_to_int16(raw[index + 28], raw[index + 29])
        self.laser_status = byte_to_int16(raw[index + 30], raw[index + 31])
        self.checksum = byte_to_int16(raw[index + 32], raw[index + 33])

    def start_opc(self):
        self.command_byte([0x03])
        self.spi.xfer2([0x07])
        self.cs.on()
        sleep(1)

        self.command_byte([0x03])
        self.spi.xfer2([0x03])
        self.cs.on()
        sleep(5)

    def stop_opc(self):
        self.command_byte([0x03])
        self.spi.xfer2([0x06])
        self.cs.on()
        sleep(1)

        self.command_byte([0x03])
        self.spi.xfer2([0x02])
        self.cs.on()
        sleep(5)


def byte_to_int16(lsb, msb):
    return (msb << 8) | lsb


def byte_to_float(b1, b2, b3, b4):
    arr = bytearray([b1, b2, b3, b4])
    return struct.unpack('<f', arr)
