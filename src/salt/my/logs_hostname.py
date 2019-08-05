import requests
import os
import datetime
import socket
import logging

log = logging.getLogger(__name__)

def test():
    time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
    hostname = socket.gethostname()
    dropboxpath = '/logs/{}/log_{}_{}.gz'.format(hostname, time, hostname)
    filenamelog = '/var/log/salt/{}/log_{}_{}'.format(hostname, time, hostname)
    gzipfilenamelog = filenamelog+'.gz'
    os.system('mkdir - p /var/log/salt/{}'.format(hostname))
    os.system('mv /var/log/salt/minion {}'.format(filenamelog))
    os.system('gzip --keep -f {} > {}'.format(filenamelog, gzipfilenamelog))
    os.system('rm /var/log/salt/minion')

    headers = {
        'Authorization': 'Bearer 5a1GcoGAVWAAAAAAAAAAC499oy3snfHjZSmNsRlGewevH1eoDeXfB8icbHE6V09H',
        'Dropbox-API-Arg': '{"path":"' + dropboxpath + '"}',
        'Content-Type': 'application/octet-stream'
    }
    data = open(gzipfilenamelog, 'rb').read()
    response = requests.post('https://content.dropboxapi.com/2/files/upload', headers=headers, data=data, timeout=600)
    return {"msg": "Log created and moved to DropBox! Folder Name: "+ hostname}