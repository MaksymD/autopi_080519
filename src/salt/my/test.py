import logging
import os
import subprocess

log = logging.getLogger(__name__)

ret = {'messages': []}  # type: Dict[str, List[Any]]

def services():
    list_service=subprocess.check_output('service --status-all', shell=True)
    return {"msg": "List of services: \n" + str(list_service)}

def off():
    #Turn off Wifi, Ethernet, Hotspot
    a = subprocess.check_output('sudo ifconfig wlan0 down', shell=True)
    ret['messages'].append("WLAN servise OFF -> SATUTS:")
    ret['messages'].append(a)
    if a == "":
        ret['messages'].append("OK")
    else:
        ret['messages'].append("FAIL")
    b = subprocess.check_output('sudo ifconfig uap0 down', shell=True)
    ret['messages'].append("HotSpot service is OFF")
    ret['messages'].append(b)
    #c = subprocess.check_output('sudo ifconfig eth0 down')
    #ret['messages'].append("LAN off")
    #ret['messages'].append(c)
    #Turn off HDMI
    d = subprocess.check_output('sudo /usr/bin/tvservice -o', shell=True)
    ret['messages'].append("HDMI service is OFF")
    ret['messages'].append(d)
    #Turn off Bluetooth
    e = subprocess.check_output('sudo systemctl disable bluetooth', shell=True)
    ret['messages'].append("Bluetooth on boot DISABLED")
    ret['messages'].append(e)
    f = subprocess.check_output('sudo service bluetooth stop', shell=True)
    ret['messages'].append("Bluetooth service is OFF")
    ret['messages'].append(f)
    g = subprocess.check_output('sudo systemctl disable hciuart', shell=True)
    ret['messages'].append("hciuart on boot DISABLED")
    ret['messages'].append(g)
    j = subprocess.check_output('sudo service hciuart stop', shell=True)
    ret['messages'].append("hciuart service is OFF")
    ret['messages'].append(j)
    #return {"msg": off_status}
    return ret

def on():
    #Turn on Wifi, Ethernet, Hotspot
    os.system('sudo ifconfig wlan0 up')
    os.system('sudo ifconfig uap0 up')
    os.system('sudo ifconfig eth0 up')
    #Turn on HDMI
    os.system('sudo /usr/bin/tvservice -p')
    #Turn on Bluetooth
    os.system('sudo systemctl enable bluetooth')
    os.system('sudo service bluetooth start')
    os.system('sudo systemctl enable hciuart')
    os.system('sudo service hciuart start')
    #return {"msg": off_status}

def ping():
    output = subprocess.check_output(["ping", "-c", "1", "8.8.8.8"])
    #return{"msg": output}
    ret['messages'].append("step 1")
    ret['messages'].append(output)
    return ret