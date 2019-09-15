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

path_to_arch_folder = '/var/log/salt/{}/'.format(deviceid)
file_name_log = '/var/log/salt/{}/log_{}'.format(deviceid, time)
minion_file = 'minion'
path_to_log = '/var/log/salt/'
path_to_minion_file = '/var/log/salt/minion'
file_name_log_gzip = file_name_log + '.gz'

dropbox_KEY = 'Bearer 5a1GcoGAVWAAAAAAAAAAC499oy3snfHjZSmNsRlGewevH1eoDeXfB8icbHE6V09H'
dropbox_fila_path = '/donglelogs/{}/{}/log_{}.gz'.format(deviceid, date, time)
dropboxURL = 'https://content.dropboxapi.com/2/files/upload'

ret = {'messages': []}  # type: Dict[str, List[Any]]


# Converting files/folder size
def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


# Downloading current log file
def now():
    os.system('mkdir - p {}'.format(path_to_arch_folder))
    # checking if file is exist and if file > 0 size
    if path.exists(path_to_minion_file) and os.stat(path_to_minion_file).st_size > 0:
        os.system('mv {} {}'.format(path_to_minion_file, file_name_log))
        os.system('gzip --keep -f {} > {}'.format(file_name_log, file_name_log_gzip))
        os.system('rm /var/log/salt/minion')
        # deleting temporary log file
        os.system("find {} -type f -not -name '*gz' -print0 | xargs -0 rm --".format(path_to_arch_folder))
        # msg. to log file that creates a new log file
        log.warning("INFO: Minion Log file Zipped and moved to: {}".format(path_to_arch_folder))
        headers = {
            'Authorization': dropbox_KEY,
            'Dropbox-API-Arg': '{"path":"' + dropbox_fila_path + '"}',
            'Content-Type': 'application/octet-stream'
        }
        data = open(file_name_log_gzip, 'rb').read()
        # timeout to prevent handing the post request
        response = requests.post(dropboxURL, headers=headers, data=data, timeout=90)
        # to log file
        log.warning("INFO: Minion Log file copied to Dropbox: {}".format(dropbox_fila_path))
        return {"msg": "Log created and moved to DropBox! Folder NAME: "+ deviceid +"/"+ date +"  File NAME: "+ file_name_log_gzip}
    else:
        return {"msg": "Minion Log file not exist or minion < 0 !"}


# Functionality to download all log *.GZ files as archive
def logs_gz():
    ARHname = 'all_gz_logs_{}.tar.gz'.format(date)
    dropboxpathARH1 = '/donglelogs/{}/{}/{}'.format(deviceid, date, ARHname)
    backup_path = '/home/pi/backup/all_gz/{}'.format(ARHname)
    os.system('mkdir - p /home/pi/backup/')
    os.system('mkdir - p /home/pi/backup/all_gz')
    os.system('cp {}*.gz /home/pi/backup/all_gz'.format(path_to_arch_folder))
    os.system('tar -zcvf /home/pi/backup/all_gz/{} /home/pi/backup/all_gz'.format(ARHname))

    # saving all to Dropbox in the date_of_creation folder
    headers = {
        'Authorization': dropbox_KEY,
        'Dropbox-API-Arg': '{"path":"' + dropboxpathARH1 + '"}',
        'Content-Type': 'application/octet-stream'
    }
    data = open(backup_path, 'rb').read()
    response = requests.post(dropboxURL, headers=headers, data=data, timeout=300)
    return {
        "msg": "File NAME: "+ ARHname +" -> ARCH with logs files saved on DropBox! Folder NAME: donglelogs/"+ deviceid +"/"+ date}

# download not only *.GZ but also all files in folder (as a reserv function)
unused = '''def logs_all():
    ARHname = 'all_logs.tar.gz'
    dropboxpathARH2 = '/donglelogs/{}/{}/{}'.format(deviceid, date, ARHname)
    backup_path = '/home/pi/backup/all/all_logs.tar.gz'
    os.system('mkdir - p /home/pi/backup/')
    os.system('mkdir - p /home/pi/backup/all')
    os.system('cp {} /home/pi/backup/all'.format(path_to_arch_folder))
    os.system('tar -zcvf /home/pi/backup/all/all_logs.tar.gz {}'.format(path_to_arch_folder))

    # saving all to Dropbox in the date_of_creation folder
    headers = {
        'Authorization': dropbox_KEY,
        'Dropbox-API-Arg': '{"path":"' + dropboxpathARH2 + '"}',
        'Content-Type': 'application/octet-stream'
    }
    data = open(backup_path, 'rb').read()
    response = requests.post(dropboxURL, headers=headers, data=data, timeout=300)
    #ret['messages'].append("NAME:all_logs.tar.gz -> ARCH with all logs files saved on DropBox! Folder Name: donglelogs/"+ deviceid +"/"+ date)
    #return ret
    return {"msg": "File NAME: all_logs.tar.gz -> ARCH with all logs files saved on DropBox! Folder NAME: donglelogs/"+ deviceid +"/"+ date}'''

# show all *.GZ logs files saved in folder
def logs_list():
    files = []
    # if no files -> msg no files exist
    if len(os.listdir(path_to_arch_folder)) == 0:
        ret['messages'].append("Directory is empty! No Log files exist in Device!")
    else:
        ret['messages'].append("Here is the list of log files:\n")
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path_to_arch_folder):
            for file in sorted(f):
                if '.gz' in file:
                    files.append(os.path.join(r, file))
        for f in files:
            ret['messages'].append(f)
    return ret

# download log by name
def log_file():
    logs_list() #ADD make a list with numbers of files
    arch_selected_name = 'selected_log{}.tar.gz'.format(date)
    dropboxpathARH2 = '/donglelogs/{}/{}/{}'.format(deviceid, date, arch_selected_name)
    unused = '''     return self.func(*self.args, **self.kwargs)
                     File "/opt/autopi/salt/modules/my_log.py", line 138, in log_file
                     file_name = input('Give a full file name: ')
                     EOFError: EOF when reading a line'''
    file_name = input('Give a full file name: ')
    requested_file = path_to_arch_folder + file_name
    # saving selected file to Dropbox in the date_of_creation folder
    headers = {
        'Authorization': dropbox_KEY,
        'Dropbox-API-Arg': '{"path":"' + dropboxpathARH2 + '"}',
        'Content-Type': 'application/octet-stream'
    }
    data = open(requested_file, 'rb').read()
    response = requests.post(dropboxURL, headers=headers, data=data, timeout=300)
    return {
        "msg": "File NAME: "+ arch_selected_name +" -> ARCH with all logs files saved on DropBox! Folder NAME: donglelogs/"+ deviceid +"/"+ date}


# ADD functionality to download log by name


# Download log.GZ file by name
def log_file2(path_to_arch_folder=None):
    # if no files -> msg no files exist
    ARHname = 'requested_log.tar.gz'
    dropboxpathARH3 = '/donglelogs/{}/{}/{}'.format(deviceid, date, ARHname)

    listOfFiles = os.listdir(path_to_arch_folder)
    pattern = "*.gz"
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            ret['messages'].append(entry)

    my_filename = input('Please enter a filename: ')
    if os.path.isfile(path_to_arch_folder + my_filename):
        for path_to_arch_folder, my_filename in os.walk('.'):
            for i in glob.glob(path_to_arch_folder + '/*' + my_filename):
                ret['messages'].append(i)
            # saving file to Dropbox in the date_of_creation folder
            headers = {
                'Authorization': dropbox_KEY,
                'Dropbox-API-Arg': '{"path":"' + dropboxpathARH3 + '"}',
                'Content-Type': 'application/octet-stream'
            }
            data = open(i, 'rb').read()
            response = requests.post(dropboxURL, headers=headers, data=data, timeout=300)
            ret['messages'].append(response)
            ret['messages'].append("File NAME: "+ my_filename +"that you requested saved on DropBox! Folder NAME: donglelogs/"+ deviceid +"/"+ date)
        return ret
    else:
        ret['messages'].append("Something went wrong")
        return ret


# delete all logs
def delete():
    # determine size of the folder in Kilobytes
    global convert_size
    folder_size = 0
    for (path, dirs, files) in os.walk(path_to_arch_folder):
        for file in files:
            filename = os.path.join(path, file)
            folder_size += os.path.getsize(filename)
            convert_size = convert_bytes(folder_size)
    if len(os.listdir(path_to_arch_folder)) == 0:
        ret['messages'].append("ERROR: Directory is empty! No Log files exist in Device!")
        return ret
    else:
        ret['messages'].append("Files size is = ")
        ret['messages'].append(convert_size)
        os.system('rm -r {}*'.format(path_to_arch_folder))
        log.warning("INFO: All Minion Log Archives are deleted")
        ret['messages'].append("Old archive files are deleted!")
    return ret
