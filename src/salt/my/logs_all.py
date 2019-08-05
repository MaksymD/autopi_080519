import requests
import os
import datetime
import socket
import logging

log = logging.getLogger(__name__)


def test():
    hostname = socket.gethostname()

    dropboxpath = '/logs/minionlogs41.tar.gz'
    gzipfilenamelog = '/etc/salt/minionlogs41.tar.gz'
    os.system('tar -zcvf /etc/salt/minionlogs41.tar.gz /var/log/salt/autopi-fbbc4ade2b11')

    headers = {
        'Authorization': 'Bearer 5a1GcoGAVWAAAAAAAAAAC499oy3snfHjZSmNsRlGewevH1eoDeXfB8icbHE6V09H',
        'Dropbox-API-Arg': '{"path":"' + dropboxpath + '"}',
        'Content-Type': 'application/octet-stream'
    }
    data = open(gzipfilenamelog, 'rb').read()
    response = requests.post('https://content.dropboxapi.com/2/files/upload', headers=headers, data=data, timeout=3600)
    return {"msg": "Log created and moved to DropBox! Folder Name: " + hostname}