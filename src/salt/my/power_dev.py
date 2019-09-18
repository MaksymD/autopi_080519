import os
import subprocess
import logging

log = logging.getLogger(__name__)
#https://www.raspberrypi.org/forums/viewtopic.php?t=208110
#https://frederik.lindenaar.nl/2018/05/11/raspberry-pi-power-saving-disable-hdmi-port-and-others-the-systemd-way.html

def off():
    # turning off wifi on boot (1)
    cmd = 'echo "dtoverlay=pi3-disable-wifi, pi3-disable-bt" | sudo tee -a /boot/config.txt'
    # turning off wifi
    cmd = 'sudo ifconfig wlan0 down'
    cmd = 'sudo ifconfig uap0 down' #disable hotspot
    # turning off Ethernet on boot (RPi3) (2)
    cmd = 'echo -n “1-1.1:1.0” | sudo tee /sys/bus/usb/drivers/smsc95xx/unbind'
    # turning off Ethernet
    cmd = 'sudo ifconfig eth0 down'
    # turning off HDMI on boot (3)
    cmd = 'echo "/usr/bin/tvservice -o" | sudo tee -a /etc/rc.local'
    # turning off HDMI
    cmd = 'sudo /usr/bin/tvservice -o'
    # turning off bluetooth on boot/ sudo apt install rfkill (4)
    cmd = 'echo "dtoverlay=pi3-disable-bt" | sudo tee -a /boot/config.txt'
    cmd = 'sudo systemctl disable bluetooth'
    cmd = 'sudo service bluetooth stop'
    cmd = 'sudo systemctl disable hciuart'
    cmd = 'sudo service hciuart stop'
    #sudo rfkill block all

    #reboot
    cmd = 'sudo shutdown -r now'
    os.system(cmd)


#sudo tvservice --off &&
#sudo sh -c 'echo 0 > /sys/class/leds/led1/brightness' &&
#sudo sh -c 'echo 0 > /sys/class/leds/led0/brightness' &&
#sudo ifconfig eth0 down && sudo ifconfig wlan0 down &&
#sudo systemctl disable bluetooth &&
#sudo service bluetooth stop &&
#sudo systemctl disable hciuart &&
#sudo service  hciuart stop
#aplay -l
#ADD show the list what is off with checking
def services():
    service=subprocess.check_output('service --status-all', shell=True)
    return {"msg": "List of services: \n" + str(service)}

def on():
    # turning on wifi on boot (1)
    # turning on wifi
    cmd = 'sudo ifconfig wlan0 up'
    # turning on Ethernet on boot (RPi3) (2)
    # turning on Ethernet
    cmd = 'sudo ifconfig eth0 up'
    # turning on HDMI (3)
    cmd = 'sudo /opt/vc/bin/tvservice -p'
    # turning on wifi and bluetooth / sudo apt install rfkill (4)
    #sudo rfkill unbliock all

    os.system(cmd)

#ADD show the list what is on with checking