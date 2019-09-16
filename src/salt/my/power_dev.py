
#https://www.raspberrypi.org/forums/viewtopic.php?t=208110

def off():
    # turning off wifi (1)
    sudo ifconfig wlan0 down
    # turning off Ethernet (2)
    sudo ifconfig eth0 down
    # turning off HDMI (3)
    sudo tvservice - -off
    # turning off wifi and bluetooth / sudo apt install rfkill (4)
    sudo rfkill block all

#ADD show the list what is off with checking



def on():
    #
    sudo rfkill unbliock all

#ADD show the list what is on with checking