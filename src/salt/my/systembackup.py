import requests
import os
import datetime
import socket
import logging

log = logging.getLogger(__name__)


def test():
    hostname = socket.gethostname()

    date = datetime.datetime.now().strftime("%Y-%m-%d")

    archname = 'system_{}_{}.tar.gz'.format(hostname, date)

    file = open('/etc/salt/minion_id')
    deviceid = file.read()
    deviceid = deviceid.rstrip('\n')

    dropboxpath = '/Device_Files/Key_and_ConfigurationFiles/{}/{}'.format(deviceid, archname)
    backuppath = '/home/pi/backup/{}'.format(archname)

    os.system('tar -zcvf /home/pi/backup/{} /var/log/salt').format(archname)

    # saving all to Dropbox with creating the folder
    headers = {
        'Authorization': 'Bearer 5a1GcoGAVWAAAAAAAAAAC499oy3snfHjZSmNsRlGewevH1eoDeXfB8icbHE6V09H',
        'Dropbox-API-Arg': '{"path":"' + dropboxpath + '"}',
        'Content-Type': 'application/octet-stream'
    }
    data = open(backuppath, 'rb').read()
    response = requests.post('https://content.dropboxapi.com/2/files/upload', headers=headers, data=data, timeout=900)
    return {"msg": "Backup of device System files & Keys is created and moved to DropBox! Folder Name: " + deviceid}
