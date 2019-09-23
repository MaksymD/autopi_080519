import logging
import os
import subprocess

log = logging.getLogger(__name__)

ret = {'messages': []}  # type: Dict[str, List[Any]]


def off():
    # a1, b1 = ""
    all_status = []
    all_info = []

    # Turn off Wifi, Ethernet, Hotspot
    # a1 = subprocess.check_output('sudo ifconfig wlan0 down', shell=True)
    a1 = "1"
    b1 = "WLAN network turning off -> STATUS: "
    print(all_status)
    all_status.insert(0, a1)
    all_info.insert(0, b1)

    # a2 = subprocess.check_output('sudo ifconfig uap0 down', shell=True)
    a2 = "2"
    b2 = "HotSpot network turning off -> STATUS: "
    all_status.insert(1, a2)
    all_info.insert(1, b2)
    print(all_status)
    print(all_info)

    z = all_status.append(all_info)

    output = []
    for i in z:
        for j in z:
            output.append((i, j))
            print(output)
    #return all_info
    off()

    # # length = len(all_results)
    #
    # for i in all_status:
    #     if i == "":
    #         ret['messages'].append("OK")
    #     else:
    #         ret['messages'].append("FAIL")
    #         ret['messages'].append(i)
    # return ret
