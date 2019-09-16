import requests
import os
import datetime
import socket
import logging

from os import path
from typing import Dict, List, Any

log = logging.getLogger(__name__)

hostname = socket.gethostname()
date = datetime.datetime.now().strftime("%Y-%m-%d")

archname = 'system_backup_{}_{}.tar.gz'.format(hostname, date)  # type: str
file = open('/etc/salt/minion_id')
deviceid = file.read()
deviceid = deviceid.rstrip('\n')

pki_path = '/etc/salt/pki/minion/'
dropboxpath = '/Device_Files/Key_and_ConfigurationFiles/{}/{}'.format(deviceid, archname)
backuppath = '/home/pi/backup/{}'.format(archname)

ret = {'messages': []}  # type: Dict[str, List[Any]]

# Creating and coping ARCH of config/Keys files form /etc/salt/ folder
def now():
    os.system('mkdir -p /home/pi/backup/')
    os.system('tar -zcvf /home/pi/backup/{} /etc/salt'.format(archname))

    # saving all to Dropbox with creating the folder
    headers = {
        'Authorization': 'Bearer 5a1GcoGAVWAAAAAAAAAAC499oy3snfHjZSmNsRlGewevH1eoDeXfB8icbHE6V09H',
        'Dropbox-API-Arg': '{"path":"' + dropboxpath + '"}',
        'Content-Type': 'application/octet-stream'
    }
    data = open(backuppath, 'rb').read()
    response = requests.post('https://content.dropboxapi.com/2/files/upload', headers=headers, data=data, timeout=300)
    return {"msg": "Backup of device System files & Keys is created and moved to DropBox! Folder Name: " + deviceid}

# Deleting Keys files from the device
def delete_key():
    if os.path.exists(pki_path):
        os.system('rm -r {}'.format(pki_path))
        os.system('sudo shutdown -r now')
        return {"msg": "Minion Keys are deleted. The device will perform restart to generate new keys!"}
    else:
        return {"msg": "Something went wrong!"}