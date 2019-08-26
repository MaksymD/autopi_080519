import os
import os.path
import logging

log = logging.getLogger(__name__)

def list():
    file = open('/etc/salt/minion_id')
    deviceid = file.read()
    deviceid = deviceid.rstrip('\n')
    #minion_path = '/var/log/salt/{}'.format(deviceid)  # type: str
    minion_path = '/home/maxdotsenko/Desktop/Aviloo/Ticketc/D10'
    files = []
    # TEST if no files -> msg no files exist
    if len(os.listdir(minion_path)) == 0:
        printtext = "Directory is empty! No Log files exist in Device!"
        return {"msg": + printtext}
    else:
        print ("Here is the list of log files:\n")
        # r=root, d=directories, f = files
        for r, d, f in os.walk(minion_path):
            for file in f:
                if '.gz' in file:
                    files.append(os.path.join(r, file))
        for f in files:
            print(f)


