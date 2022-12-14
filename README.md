# read_DS18B20_sensors

Read DS18B20 temperature-sensors on a 1-wire bus
- automatic sensor detection 
- continuously refreshing temperature and status
- indicating current read pointer, timestamp, duration device id, temperature and connection-status

[Video](https://techhub.social/@ernstgreiner/109346875416334526)

This script is running on a Raspberry Pi 3



## Change sensor resolution (in linux shell not Python)

This is optional.  
The lower the resolution the faster the scan... 

[More infos here...](https://raspberrypi.stackexchange.com/questions/14278/how-to-change-ds18b20-reading-resolution)  


### Change resolution temporary

This is the simplest solution i have found, directly via linux shell.

``` shell
cd /sys/bus/w1/devices/  
sudo su  
for dir in 28-*; do echo 10 > "$dir"/resolution; echo "$dir"; done  
```
or
``` shell
sudo su  
for dir in /sys/bus/w1/devices/28-*; do echo 10 > "$dir"/resolution; echo "$dir"; done  
```


### check settings
``` shell
cat 28-*/resolution  
```

or
``` shell
cat /sys/bus/w1/devices/28-*/resolution  
```

### Change resolution persistent (save it in the sensor-eeprom)
``` shell
cd /sys/bus/w1/devices/  
sudo su  
for dir in 28-*; do echo 10   > "$dir"/resolution; echo "$dir"; done  
for dir in 28-*; do echo save > "$dir"/eeprom_cmd; echo "$dir"; done  
```
