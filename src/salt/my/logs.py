import requests
import os
import os.path
import datetime
import logging
from os import path

log = logging.getLogger(__name__)


# path = '/var/log/salt/'

# TEST timeout on this function // timeout=3600 //
# def test(self, message, timeout=None):
# timeout
# if timeout == None:
#   timeout = message.get("timeout", self._default_timeout)
def test():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
    # hostname = socket.gethostname()
    file = open('/etc/salt/minion_id')
    deviceid = file.read()
    deviceid = deviceid.rstrip('\n')
    dropboxpath = '/donglelogs/{}/{}/log_{}.gz'.format(deviceid, date, time)
    dropboxURL = 'https://content.dropboxapi.com/2/files/upload'
    filenamelog = '/var/log/salt/{}/log_{}'.format(deviceid, time)
    gzipfilenamelog = filenamelog + '.gz'
    os.system('mkdir - p /var/log/salt/{}'.format(deviceid))
    # TEST check if file is exist
    try:
        if path.exists('/var/log/salt/minion'):
            print ("File found!")
            # TEST if file > 0 size
        elif os.stat('/var/log/salt/minion').st_size > 0:
            os.system('mv /var/log/salt/minion.1 {}'.format(filenamelog))
            os.system('gzip --keep -f {} > {}'.format(filenamelog, gzipfilenamelog))
            os.system('rm /var/log/salt/minion')
            # to log file
            log.info("Minion Log file Zipped and moved to: {}".format(deviceid))
            headers = {
                'Authorization': 'Bearer 5a1GcoGAVWAAAAAAAAAAC499oy3snfHjZSmNsRlGewevH1eoDeXfB8icbHE6V09H',
                'Dropbox-API-Arg': '{"path":"' + dropboxpath + '"}',
                'Content-Type': 'application/octet-stream'
            }
            data = open(gzipfilenamelog, 'rb').read()
            # TEST timeout to prevent handing the post requrest
            try:
                response = requests.post(dropboxURL, headers=headers, data=data, timeout=(3600, 3000))
                print(response)
                # to log file
                log.info("Minion Log file copied to Dropbox: {}".format(dropboxpath))
            except requests.ReadTimeout:
                print("READ TIME OUT")
                # to log file
                log.info("Minion Log file NOT copied to Dropbox: {READ TIME OUT}")
        else:
            print ("Minion Log file not exist or less than 0!")
    except:
        print ("Something Wrong!")
    return {"msg": "Log created and moved to DropBox! Folder Name: " + deviceid}


# show all *.GZ logs files saved in folder
def list():
    deviceid = file.read()
    deviceid = deviceid.rstrip('\n')
    minion_path = '/var/log/salt'
    path = '{}/{}'.format(minion_path, deviceid)
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.gz' in file:
                files.append(os.path.join(r, file))
    # ADD if no files -> msg no files exist
    for f in files:
        print(f)

# add functionality to download log by name from //filenamelo // from previus functionality
