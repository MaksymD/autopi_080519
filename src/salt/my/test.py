import requests
import os
import os.path
import datetime
import logging
import fnmatch
import glob
from os import path

log = logging.getLogger(__name__)

date = datetime.datetime.now().strftime("%Y-%m-%d")
time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
fileid = open('/etc/salt/minion_id')
deviceid = fileid.read()
deviceid = deviceid.rstrip('\n')
pathtologfile = '/home/maxdotsenko/Desktop/Aviloo/minion.txt'
dropboxpath = '/donglelogs/{}/{}/log_{}.gz'.format(deviceid, date, time)
dropboxURL = 'https://content.dropboxapi.com/2/files/upload'
filenamelog = '/var/log/salt/{}/log_{}'.format(deviceid, time)
gzipfilenamelog = filenamelog + '.gz'
minion_path = '/home/maxdotsenko/Desktop/Aviloo/Ticketc/D10'


# TESTED download current log file
def now(timeout=600):
    # TO DO pathtologfile = '/var/log/salt/'
    os.system('mkdir - p /var/log/salt/{}'.format(deviceid))
    # TESTED check if file is exist and if file > 0 size
    if path.exists(pathtologfile) and os.stat(pathtologfile).st_size > 0:
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

    # return {"msg": "Log created and moved to DropBox! Folder Name: " + deviceid}


# TESTED show all *.GZ logs files saved in folder
def logs_list():
    # TO DO minion_path = '/var/log/salt/{}/'.format(deviceid)
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
def logs_gz(timeout=300):
    ARHname = 'all_gz_logs.tar.gz'
    dropboxpathARH1 = '/donglelogs/{}/{}/{}'.format(deviceid, date, ARHname)
    backuppath = '/home/pi/backup/all_gz/all_gz_logs.tar.gz'
    os.system('mkdir - p /home/pi/backup/')
    os.system('mkdir - p /home/pi/backup/all_gz')
    os.system('cp /var/log/salt/{}/*.gz /home/pi/backup/all_gz'.format(deviceid))
    os.system('tar -zcvf /home/pi/backup/all_gz/all_gz_logs.tar.gz /home/pi/backup/all_gz'.format(deviceid))

    # saving all to Dropbox in the date_of_creation folder
    headers = {
        'Authorization': 'Bearer 5a1GcoGAVWAAAAAAAAAAC499oy3snfHjZSmNsRlGewevH1eoDeXfB8icbHE6V09H',
        'Dropbox-API-Arg': '{"path":"' + dropboxpathARH1 + '"}',
        'Content-Type': 'application/octet-stream'
    }
    data = open(backuppath, 'rb').read()
    response = requests.post(dropboxURL, headers=headers, data=data, timeout=timeout)
    print(response)
    return {"msg": "All logs files saved on DropBox! Folder Name: donglelogs/" + deviceid}


# TESTED - OK
def logs_all(timeout=300):
    ARHname = 'all_logs.tar.gz'
    dropboxpathARH2 = '/donglelogs/{}/{}/{}'.format(deviceid, date, ARHname)
    backuppath = '/home/pi/backup/all_gz/all_logs.tar.gz'
    os.system('mkdir - p /home/pi/backup/')
    os.system('mkdir - p /home/pi/backup/all')
    os.system('cp /var/log/salt/{}/*.gz /home/pi/backup/all'.format(deviceid))
    os.system('tar -zcvf /home/pi/backup/all/all_logs.tar.gz /var/log/salt/{}/'.format(deviceid))

    # saving all to Dropbox in the date_of_creation folder
    headers = {
        'Authorization': 'Bearer 5a1GcoGAVWAAAAAAAAAAC499oy3snfHjZSmNsRlGewevH1eoDeXfB8icbHE6V09H',
        'Dropbox-API-Arg': '{"path":"' + dropboxpathARH2 + '"}',
        'Content-Type': 'application/octet-stream'
    }
    data = open(backuppath, 'rb').read()
    response = requests.post(dropboxURL, headers=headers, data=data, timeout=timeout)
    print(response)
    return {"msg": "Folder with all logs files saved on DropBox! Folder Name: donglelogs/" + deviceid}


# ADD functionality to download log by name
def log_file(timeout=300):
    # x, timeout=300
    # TO DO minion_path = '/var/log/salt/{}/'.format(deviceid)
    # TESTED if no files -> msg no files exist
    ARHname = 'requested_log.tar.gz'
    dropboxpathARH3 = '/donglelogs/{}/{}/{}'.format(deviceid, date, ARHname)

    listOfFiles = os.listdir('/home/maxdotsenko/Desktop/Aviloo/Ticketc/D10')
    pattern = "*.gz"
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            print (entry)

    my_filename = input('Please enter a filename: ')
    if os.path.isfile('/home/maxdotsenko/Desktop/Aviloo/Ticketc/D10'+my_filename):
        my_dir = '/home/maxdotsenko/Desktop/Aviloo/Ticketc/D10'
        for my_dir, my_filename in os.walk('.'):
            for i in glob.glob(my_dir+'/*'+my_filename):
                print i
        # saving file to Dropbox in the date_of_creation folder
            headers = {
                'Authorization': 'Bearer 5a1GcoGAVWAAAAAAAAAAC499oy3snfHjZSmNsRlGewevH1eoDeXfB8icbHE6V09H',
                'Dropbox-API-Arg': '{"path":"' + dropboxpathARH3 + '"}',
                'Content-Type': 'application/octet-stream'
            }
            data = open(i, 'rb').read()
            response = requests.post(dropboxURL, headers=headers, data=data, timeout=timeout)
            print(response)
            print ("File "+my_filename+" that you requested saved on DropBox! Folder Name: donglelogs/" + deviceid)
        #return {"msg": "File "+my_filename+" that you requested saved on DropBox! Folder Name: donglelogs/" + deviceid}
    else:
        print ("Something went wrong")
