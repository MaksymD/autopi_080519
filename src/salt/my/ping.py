import logging
import os

log = logging.getLogger(__name__)

def test():
    hostname = "google.com"
    response = os.system("ping -c 1 " + hostname, timeout=300)
    if response == 0:
        print(hostname, 'is up!')
    else:
        print(hostname, 'is down!')
    return {"msg": "pinging done"}