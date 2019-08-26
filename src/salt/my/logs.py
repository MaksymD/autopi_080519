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
def test(timeout=(600)):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
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
            print("File found!")
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
            # TEST timeout to prevent handing the post request
            try:
                response = requests.post(dropboxURL, headers=headers, data=data, timeout=timeout)
                print(response)
                # to log file
                log.info("Minion Log file copied to Dropbox: {}".format(dropboxpath))
            except requests.ReadTimeout:
                print("READ TIME OUT")
                # to log file
                log.info("Minion Log file was NOT copied to Dropbox: {READ TIME OUT}")
        else:
            print("Minion Log file not exist or less than 0!")
    except:
        print("Something went wrong!")
    return {"msg": "Log created and moved to DropBox! Folder Name: " + deviceid}


# TESTED show all *.GZ logs files saved in folder

def logs_list():
    file = open('/etc/salt/minion_id')
    deviceid = file.read()
    deviceid = deviceid.rstrip('\n')
    minion_path = '/var/log/salt/{}/'.format(deviceid)
    #minion_path = '/home/maxdotsenko/Desktop/Aviloo/Ticketc/D10'
    files = []
    # TESTED if no files -> msg no files exist
    if len(os.listdir(minion_path)) == 0:
        print("Directory is empty! No Log files exist in Device!")
    else:
        print ("Here is the list of log files:\n ")
        # r=root, d=directories, f = files
        for r, d, f in os.walk(minion_path):
            for file in f:
                if '.gz' in file:
                    files.append(os.path.join(r, file))
        for f in files:
            print(f)

# TESTED functionality to download all files as archive
def logs_gz(timeout=(300)):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    archname = 'all_gz_logs.tar.gz'
    file = open('/etc/salt/minion_id')
    deviceid = file.read()
    deviceid = deviceid.rstrip('\n')
    dropboxpath = '/donglelogs/{}/{}/{}'.format(deviceid, date, archname)
    dropboxURL = 'https://content.dropboxapi.com/2/files/upload'
    backuppath = '/home/pi/backup/all_gz/all_gz_logs.tar.gz'
    os.system('mkdir - p /home/pi/backup/')
    os.system('mkdir - p /home/pi/backup/all_gz')
    os.system('cp /var/log/salt/{}/*.gz /home/pi/backup/all_gz'.format(deviceid))
    os.system('tar -zcvf /home/pi/backup/all_gz/all_gz_logs.tar.gz /home/pi/backup/all_gz'.format(deviceid))

    # saving all to Dropbox in the date_of_creation folder
    headers = {
        'Authorization': 'Bearer 5a1GcoGAVWAAAAAAAAAAC499oy3snfHjZSmNsRlGewevH1eoDeXfB8icbHE6V09H',
        'Dropbox-API-Arg': '{"path":"' + dropboxpath + '"}',
        'Content-Type': 'application/octet-stream'
    }
    data = open(backuppath, 'rb').read()
    response = requests.post(dropboxURL, headers=headers, data=data, timeout=timeout)
    print(response)
    return {"msg": "All logs files saved on DropBox! Folder Name: donglelogs/" + deviceid}


# ADD functionality to download log by name

# TESTED - OK
def logs_all(timeout=(300)):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    archname = 'all_logs.tar.gz'
    file = open('/etc/salt/minion_id')
    deviceid = file.read()
    deviceid = deviceid.rstrip('\n')
    dropboxpath = '/donglelogs/{}/{}/{}'.format(deviceid, date, archname)
    dropboxURL = 'https://content.dropboxapi.com/2/files/upload'
    backuppath = '/home/pi/backup/all_gz/all_logs.tar.gz'
    os.system('mkdir - p /home/pi/backup/')
    os.system('mkdir - p /home/pi/backup/all')
    os.system('cp /var/log/salt/{}/*.gz /home/pi/backup/all'.format(deviceid))
    os.system('tar -zcvf /home/pi/backup/all/all_logs.tar.gz /var/log/salt/{}/'.format(deviceid))

    # saving all to Dropbox in the date_of_creation folder
    headers = {
        'Authorization': 'Bearer 5a1GcoGAVWAAAAAAAAAAC499oy3snfHjZSmNsRlGewevH1eoDeXfB8icbHE6V09H',
        'Dropbox-API-Arg': '{"path":"' + dropboxpath + '"}',
        'Content-Type': 'application/octet-stream'
    }
    data = open(backuppath, 'rb').read()
    response = requests.post(dropboxURL, headers=headers, data=data, timeout=timeout)
    print(response)
    return {"msg": "Folder with all logs files saved on DropBox! Folder Name: donglelogs/" + deviceid}