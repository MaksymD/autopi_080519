import logging
import os
import subprocess

log = logging.getLogger(__name__)


def services():
    list_service = subprocess.check_output('service --status-all', shell=True)
    return {"msg": "List of services: \n" + str(list_service)}


def off():
    # turning off wifi on boot (1)
    os.system('echo "dtoverlay=pi3-disable-wifi" | sudo tee -a /boot/config.txt')
    # turning off wifi
    os.system('sudo ifconfig wlan0 down')
    os.system('sudo ifconfig uap0 down')  # disable hotspot
    # turning off Ethernet on boot (RPi3) (2)
    os.system('echo 0x0 > /sys/devices/platform/bcm2708_usb/buspower') #check
    # turning off Ethernet
    os.system('sudo ifconfig eth0 down')
    # turning off HDMI on boot (3)
    # save original version of rc.local
    os.system('sudo cp /etc/rc.local /etc/rc.local.bak')
    os.system("sed -i '/exit/d' /etc/rc.local")
    os.system('echo "/usr/bin/tvservice -o" | sudo tee -a /etc/rc.local')
    os.system('echo "exit 0" | sudo tee -a /etc/rc.local')
    # turning off HDMI
    os.system('sudo /usr/bin/tvservice -o')
    # turning off bluetooth on boot/ sudo apt install rfkill (4)
    os.system('echo "dtoverlay=pi3-disable-bt, pi3-disable-bt" | sudo tee -a /boot/config.txt')
    os.system('sudo systemctl disable bluetooth')
    os.system('sudo service bluetooth stop')
    os.system('sudo systemctl disable hciuart')
    os.system('sudo service hciuart stop')
    return {"msg": "OFF!"}


def on():
    # turning on wifi on boot (1)
    os.system("sed -i '/dtoverlay=pi3/d\' /boot/config.txt")
    # turning on wifi
    os.system('sudo ifconfig wlan0 up')
    os.system('sudo ifconfig uap0 up')
    # turning on Ethernet on boot (RPi3) (2)
    os.system('echo 0x1 > /sys/devices/platform/bcm2708_usb/buspower') #check
    # turning on Ethernet
    os.system('sudo ifconfig eth0 up')
    # turning off HDMI on boot (3)
    os.system("sed -i '/usr/d' /etc/rc.local")
    # turning on HDMI (3)
    os.system('sudo /opt/vc/bin/tvservice -p')
    # turning on wifi and bluetooth (4)
    os.system("sed -i '/dtoverlay=pi3/d\' /boot/config.txt")
    os.system('sudo systemctl enable bluetooth')
    os.system('sudo service bluetooth start')
    os.system('sudo systemctl enable hciuart')
    os.system('sudo service hciuart start')
    return {"msg": "ON!"}