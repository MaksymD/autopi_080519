import requests
import os
import os.path
import datetime
import logging
import fnmatch
import glob
from os import path

from typing import Dict, List, Any

log = logging.getLogger(__name__)

date = datetime.datetime.now().strftime("%Y-%m-%d")
time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
fileid = open('/etc/salt/minion_id')
deviceid = fileid.read()
deviceid = deviceid.rstrip('\n')
pathtologfile = '/var/log/salt/minion'
dropboxpath = '/donglelogs/{}/{}/log_{}.gz'.format(deviceid, date, time)
dropboxURL = 'https://content.dropboxapi.com/2/files/upload'
filenamelog = '/var/log/salt/{}/log_{}'.format(deviceid, time)
gzipfilenamelog = filenamelog + '.gz'
minion_path = '/var/log/salt/{}/'.format(deviceid)
ret = {'messages': []}  # type: Dict[str, List[Any]]


# TESTED download current log file
def now(timeout=600):
    os.system('mkdir - p /var/log/salt/{}'.format(deviceid))
    # TESTED check if file is exist and if file > 0 size
    if path.exists(pathtologfile) and os.stat(pathtologfile).st_size > 0:
        os.system('mv /var/log/salt/minion {}'.format(filenamelog))
        os.system('gzip --keep -f {} > {}'.format(filenamelog, gzipfilenamelog))
        os.system('rm /var/log/salt/minion')
        # to log file
        log.info("Minion Log file Zipped and moved to: /var/log/salt/{}".format(deviceid))
        headers = {
            'Authorization': 'Bearer 5a1GcoGAVWAAAAAAAAAAC499oy3snfHjZSmNsRlGewevH1eoDeXfB8icbHE6V09H',
            'Dropbox-API-Arg': '{"path":"' + dropboxpath + '"}',
            'Content-Type': 'application/octet-stream'
        }
        data = open(gzipfilenamelog, 'rb').read()
        # TEST timeout to prevent handing the post request
        response = requests.post(dropboxURL, headers=headers, data=data, timeout=timeout)
        # to log file
        log.info("Minion Log file copied to Dropbox: {}".format(dropboxpath))
        # requests.ReadTimeout:
        # ret['messages'].append("READ TIME OUT")
        # to log file
        # log.info("Minion Log file was NOT copied to Dropbox: {READ TIME OUT}")
        return {"msg": "Log created and moved to DropBox! Folder Name: " + deviceid}
    else:
        return {"msg": "Minion Log file not exist or less than 0!"}


# TESTED show all *.GZ logs files saved in folder
def logs_list():
    files = []
    # TESTED if no files -> msg no files exist
    if len(os.listdir(minion_path)) == 0:
        ret['messages'].append("Directory is empty! No Log files exist in Device!")
    else:
        ret['messages'].append("Here is the list of log files:\n")
        # r=root, d=directories, f = files
        for r, d, f in os.walk(minion_path):
            for file in sorted(f):
                if '.gz' in file:
                    files.append(os.path.join(r, file))
        for f in files:
            ret['messages'].append(f)
    return ret


# ADD functionality to download log by name


# TESTED functionality to download all files as archive
def logs_gz(timeout=300):
    ARHname = 'all_gz_logs.tar.gz'
    dropboxpathARH1 = '/donglelogs/{}/{}/{}'.format(deviceid, date, ARHname)
    backuppath = '/home/pi/backup/all_gz/all_gz_logs.tar.gz'
    os.system('mkdir - p /home/pi/backup/')
    os.system('mkdir - p /home/pi/backup/all_gz')
    os.system('cp /var/log/salt/{}/*.gz /home/pi/backup/all_gz'.format(deviceid))
    os.system('tar -zcvf /home/pi/backup/all_gz/all_gz_logs.tar.gz /home/pi/backup/all_gz')

    # saving all to Dropbox in the date_of_creation folder
    headers = {
        'Authorization': 'Bearer 5a1GcoGAVWAAAAAAAAAAC499oy3snfHjZSmNsRlGewevH1eoDeXfB8icbHE6V09H',
        'Dropbox-API-Arg': '{"path":"' + dropboxpathARH1 + '"}',
        'Content-Type': 'application/octet-stream'
    }
    data = open(backuppath, 'rb').read()
    response = requests.post(dropboxURL, headers=headers, data=data, timeout=timeout)
    # ret['messages'].append("NAME: all_gz_logs.tar.gz -> ARCH with logs files saved on DropBox! Folder Name: donglelogs/"+ deviceid +"/DATE")
    # return ret
    return {
        "msg": "NAME: all_gz_logs.tar.gz -> ARCH with logs files saved on DropBox! Folder Name: donglelogs/" + deviceid + "/DATE"}


# TESTED - OK
def logs_all(timeout=300):
    ARHname = 'all_logs.tar.gz'
    dropboxpathARH2 = '/donglelogs/{}/{}/{}'.format(deviceid, date, ARHname)
    backuppath = '/home/pi/backup/all/all_logs.tar.gz'
    os.system('mkdir - p /home/pi/backup/')
    os.system('mkdir - p /home/pi/backup/all')
    os.system('cp /var/log/salt/{}/ /home/pi/backup/all'.format(deviceid))
    os.system('tar -zcvf /home/pi/backup/all/all_logs.tar.gz /var/log/salt/{}/'.format(deviceid))

    # saving all to Dropbox in the date_of_creation folder
    headers = {
        'Authorization': 'Bearer 5a1GcoGAVWAAAAAAAAAAC499oy3snfHjZSmNsRlGewevH1eoDeXfB8icbHE6V09H',
        'Dropbox-API-Arg': '{"path":"' + dropboxpathARH2 + '"}',
        'Content-Type': 'application/octet-stream'
    }
    data = open(backuppath, 'rb').read()
    response = requests.post(dropboxURL, headers=headers, data=data, timeout=timeout)
    # ret['messages'].append("NAME:all_logs.tar.gz -> ARCH with all logs files saved on DropBox! Folder Name: donglelogs/"+ deviceid +"/DATE")
    # return ret
    return {
        "msg": "NAME: all_logs.tar.gz -> ARCH with all logs files saved on DropBox! Folder Name: donglelogs/" + deviceid + "/DATE"}


def log_file(timeout=300):
    # x, timeout=300
    # TESTED if no files -> msg no files exist
    ARHname = 'requested_log.tar.gz'
    dropboxpathARH3 = '/donglelogs/{}/{}/{}'.format(deviceid, date, ARHname)

    listOfFiles = os.listdir('/var/log/salt/{}/'.format(deviceid))
    pattern = "*.gz"
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            ret['messages'].append(entry)

    my_filename = input('Please enter a filename: ')
    if os.path.isfile('/var/log/salt/{}/'.format(deviceid) + my_filename):
        my_dir = '/var/log/salt/{}/'.format(deviceid)
        for my_dir, my_filename in os.walk('.'):
            for i in glob.glob(my_dir + '/*' + my_filename):
                ret['messages'].append(i)
            # saving file to Dropbox in the date_of_creation folder
            headers = {
                'Authorization': 'Bearer 5a1GcoGAVWAAAAAAAAAAC499oy3snfHjZSmNsRlGewevH1eoDeXfB8icbHE6V09H',
                'Dropbox-API-Arg': '{"path":"' + dropboxpathARH3 + '"}',
                'Content-Type': 'application/octet-stream'
            }
            data = open(i, 'rb').read()
            response = requests.post(dropboxURL, headers=headers, data=data, timeout=timeout)
            ret['messages'].append(response)
            ret['messages'].append(
                "File " + my_filename + " that you requested saved on DropBox! Folder Name: donglelogs/" + deviceid)
        return ret
    else:
        ret['messages'].append("Something went wrong")
        return ret
