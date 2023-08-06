import os
from time import time_ns


class LogFile(object):
    """
    An object representing a log file to store data
    :param base_name: Basic file name to be created i.e. tuna_01, tuna_02, etc.
    :param path: Path to file, recommended in /home/user/... or /media/usb_stick/...
    """
    def __init__(self, base_name, path):
        self.base_name = str(base_name)
        self.name = self.make_file(path)

    def make_file(self, path):
        name = self.base_name
        name += "_00.csv"
        path_name = path
        for i in range(100):
            path_name = path
            name_l = list(name)
            name_l[-1-5] = str(int(i / 10))
            name_l[-1-4] = str(int(i % 10))
            name = "".join(name_l)
            path_name += '/'
            path_name += name
            if os.path.exists(path_name) is False:
                break
        return path_name

    def write_data_log(self, opc_object, time=time_ns()):

        log = open(self.name, "a+")
        log.write(str(time))

        counts = opc_object.hist
        data_array = ",".join(str(i) for i in counts)
        data_array = data_array.replace("]", "").replace("[", "")
        log.write(data_array)

        mtofs = opc_object.mtof
        data_array = ",".join(str(i) for i in mtofs)
        data_array = data_array.replace("]", "").replace("[", "")
        log.write(data_array)

        log.write(str(opc_object.period))
        log.write(str(opc_object.checksum))

        log.write(str(opc_object.reject_glitch))
        log.write(str(opc_object.reject_ltof))
        log.write(str(opc_object.reject_range))
        log.write(str(opc_object.reject_ratio))

        log.write(str(opc_object.PM_A_ugm3))
        log.write(str(opc_object.PM_B_ugm3))
        log.write(str(opc_object.PM_C_ugm3))

        log.write(str(opc_object.temp_degC))
        log.write(str(opc_object.RH_true))

        log.write(str(opc_object.flow_rate))
        log.write(str(opc_object.fan_revs))
        log.write(str(opc_object.laser_status))

        log.write('\n')
        log.flush()
        log.close()

    def make_headers(self, opc_object, date="Null", time=time_ns(), epoch="Null"):

        log = open(self.name, "a+")
        log.write(date)
        log.write(',')
        log.write(time)
        log.write(',')
        log.write(str(epoch))
        log.write('\n')
        log.write(opc_object.info_string)
        log.write('\n')
        log.write(opc_object.serial_string)
        log.write('\n')

        log.write("Bin Boundaries (12 bit ADC):,")
        bbs_adc = opc_object.bbs_adc
        bb_str = ",".join(str(i) for i in bbs_adc)
        bb_str = bb_str.replace("]", "").replace("[", "")
        log.write(bb_str)
        log.write('\n')
        log.write("Bin Boundaries (um):,")
        bbs_um = opc_object.bbs_um
        bb_str = ",".join(str(i) for i in bbs_um)
        bb_str = bb_str.replace("]", "").replace("[", "")
        log.write(bb_str)
        log.write('\n')
        log.write("Bin Weights:,")
        bws = opc_object.bws
        bb_str = ",".join(str(i) for i in bws)
        bb_str = bb_str.replace("]", "").replace("[", "")
        log.write(bb_str)
        log.write('\n')

        log.write("PM A Threshold (um), PM B Threshold (um), PM C Threshold (um)")
        log.write(str(opc_object.PMd_A_um) + "," + str(opc_object.PMd_B_um) + "," + str(opc_object.PMd_C_um))
        log.write('\n')

        log.write("AM Sample Interval Count, AM Idle Interval Count, AM MAX Data Arraying in File, AM Only Save PM, "
                  "AM Fan ON During Idle, AM Laser ON During Idle")
        log.write(str(opc_object.AM_sample_interval_count) + "," + str(opc_object.AM_idle_interval_count) + "," +
                  str(opc_object.AM_max_data_arrays_in_file) + "," + str(opc_object.AM_only_save_PM) + "," +
                  str(opc_object.AM_fan_on_idle) + "," + str(opc_object.AM_laser_on_idle))
        log.write('\n')

        log.write("MAX ToF, ToF to SFR Factor, Particle Validation Period, Bin Weighting Index")
        log.write(str(opc_object.max_ToF) + "," + str(opc_object.ToF_SFR_factor) + "," + str(opc_object.PVP) + "," +
                  str(opc_object.bin_weighting_index))
        log.write('\n\n')

        log.write("time,b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,b17,b18,b19,b20,b21,b22,b23,"
                  "b1ToF,b3ToF,b5ToF,b7ToF,period,CSum,Reject glitch,Reject longToF,Reject Range,RejRat,"
                  "PM A (ugm3),PM B_(ugm3),PM C (ugm3),Temp degC,RH (%),Flow Rate,Fan Revs,Laser Status")
        log.write('\n')
        log.flush()
        log.close()
