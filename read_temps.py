#!/usr/bin/python

# measures temperatures with DS18B20 sensors

Author = "Ing. Ernst Greiner"
VersionDate = "2022-11-02"
Version = "v0.0.6"

import os
import sys
import time
from datetime import datetime

# script settings
temperature_title    = "| Current | No | Timestamp     | Duration | DeviceId        | Temperature | Status       |"
temperature_template = "|  ---->  | {serial_no:02d} | {timestamp}  |  {duration:04d}ms  | {deviceId} |  {temperature}   | {status} |  "
temperature_error = " xxxxxx "

dir_devices = "/sys/bus/w1/devices/"
reinitialize_after_loops = 7
loop_delay = 1.0
run_loop = True

# define main functions
def main_print_all_temperatures_found_on_1_wire_bus():
    loop_counter = 0
    line_offset = 3

    def initialize():
        os.system('clear')
        print("Measuring temperatures with DS18B20 sensors ({version})".format(version=Version))
        print("")
        print(temperature_title)

    def reinitialize():
        nonlocal loop_counter
        if loop_counter > reinitialize_after_loops:
            loop_counter = 0
            initialize()

    def loop_sensors():
        global run_loop
        nonlocal loop_counter
        while run_loop:
            loop_counter += 1
            print_all_sensors(dir_devices, line_offset)
            time.sleep(loop_delay)
            reinitialize()

    def exit():
        os.system('clear')
        sys.exit(0)

    initialize()
    loop_sensors()
    exit()

def print_all_sensors(dir, offset):
    start_offset = offset
    start_delete_pointer = 3

    def erase_read_pointer():
        if offset > start_offset + 1:
            print_there(start_delete_pointer, offset - 1, "       ")
        if offset == start_offset + 1:
            print_there(start_delete_pointer, start_offset + len(sub_dirs) - 1, "       ")

    serial_no = 0
    for path, sub_dirs, files in os.walk(dir):
        for name in sub_dirs:
            if not run_loop:
                break

            if name.startswith('28-'):
                offset += 1
                serial_no += 1
                print_there(0, offset, read_sensor(name, serial_no))
                erase_read_pointer()
    if serial_no == 0:
        print_there(0, offset+1, temperature_template.format(serial_no=0, timestamp=get_timestamp(), duration=0, deviceId="xx-xxxxxxxxxxxx", temperature=temperature_error, status="No Sensors  "))


def read_sensor(device_id, serial_no):
    def output(timestamp,  duration, temperature, status):
        return temperature_template.format(serial_no=serial_no, timestamp=timestamp, duration=duration,
                                           deviceId=device_id, temperature=temperature, status=status)
    def output_error(timestamp,  duration, status):
        return output(timestamp, duration, temperature_error, status)

    try:
        start = datetime.now()
        timestamp = get_timestamp()

        content = get_file_content("/sys/bus/w1/devices/" + device_id + "/temperature")
        temperature = to_temperature(content, 2)

        duration = int((datetime.now() - start).total_seconds() * 1000)

        # Power up
        if '85.00' in temperature:
            return output_error(timestamp, duration, "PowerUp     ")

        # other error
        if temperature == temperature_error:
            return output_error(timestamp, duration, "Disconnected")

        return output(timestamp, duration, temperature, "Connected   ")
    except FileNotFoundError:
        return output_error(timestamp,  0, "Disconnected")
    except KeyboardInterrupt:
        global run_loop
        run_loop = False
        return output_error(timestamp,  0, "Exit        ")
    except :
        return output_error(timestamp,  0, "Error       ")

# define sub functions
def print_there(x, y, text):
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
    sys.stdout.flush()

def to_temperature(temperature_as_string, decimal_places=1):
    if temperature_as_string == '':
        return temperature_error

    temperature = round(float(temperature_as_string) / 1000, decimal_places)

    decimal = '.' + str(decimal_places) + 'f'
    result = str(format(temperature, decimal)) + "°C"
    return result if temperature < 0.0 else " " + result

def get_timestamp():
    now = datetime.now()
    timestamp = now.strftime('%H:%M:%S.%f')[:-3]
    return timestamp

def get_file_content(filename):
    file = open(filename, 'r')
    content = file.read()
    file.close()
    return content


# call main functions
main_print_all_temperatures_found_on_1_wire_bus()
