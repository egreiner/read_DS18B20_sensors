# read_DS18B20_sensors

Read DS18B20 temperature-sensors on a 1-wire bus
- automatic sensor detection 
- and continuously refreshing temperature and status

This script is running on a Raspberry Pi 3


## Change sensor resolution (in linux shell not Python)
### Change resolution temporary
https://raspberrypi.stackexchange.com/questions/14278/how-to-change-ds18b20-reading-resolution

``` shell
cd /sys/bus/w1/devices/  
sudo su  
for dir in 28-*; do echo 10 > "$dir"/resolution; echo "$dir"; done  
```

### check settings
cat 28-*/resolution  

### to save it in eeprom use:
cd /sys/bus/w1/devices/  
sudo su  
for dir in 28-*; do echo 10   > "$dir"/resolution; echo "$dir"; done  
for dir in 28-*; do echo save > "$dir"/eeprom_cmd; echo "$dir"; done  

