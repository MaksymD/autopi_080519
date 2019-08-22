import requests
import os
import datetime
import TimeoutSauce
import logging

log = logging.getLogger(__name__)

#add timeout on this function // timeout=3600 // $timeout=3600
def test():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
    #hostname = socket.gethostname()
    file = open('/etc/salt/minion_id')
    deviceid = file.read()
    deviceid = deviceid.rstrip('\n')
    dropboxpath = '/donglelogs/{}/{}/log_{}.gz'.format(deviceid, date, time)
    filenamelog = '/var/log/salt/{}/log_{}'.format(deviceid, time)
    gzipfilenamelog = filenamelog + '.gz'
    os.system('mkdir - p /var/log/salt/{}'.format(deviceid))
    #add check if file is exist
    #add if file > 0 size
    os.system('mv /var/log/salt/minion.1 {}'.format(filenamelog))
    os.system('gzip --keep -f {} > {}'.format(filenamelog, gzipfilenamelog))
    os.system('rm /var/log/salt/minion')

    headers = {
        'Authorization': 'Bearer 5a1GcoGAVWAAAAAAAAAAC499oy3snfHjZSmNsRlGewevH1eoDeXfB8icbHE6V09H',
        'Dropbox-API-Arg': '{"path":"' + dropboxpath + '"}',
        'Content-Type': 'application/octet-stream'
    }
    data = open(gzipfilenamelog, 'rb').read()
    response = requests.post('https://content.dropboxapi.com/2/files/upload', headers=headers, data=data, timeout=None)
    #add timeout to prevent handing the post requrest
    return {"msg": "Log created and moved to DropBox! Folder Name: " + deviceid}

#add functionality to show all logs files saved in folder // filenamelog // -> delete last log_{} and show all files with ending .gz


#add functionality to download log by name from //filenamelo // from previus functionality