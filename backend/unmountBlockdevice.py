import subprocess
#import os
import json
import time


#cmdString = ["lsblk --json -p -o NAME,VENDOR,SIZE,SERIAL,TYPE,MAJ:MIN --exclude 1"]
command1 = ["sudo umount"]
command2 = ["sudo udisksctl power-off -b"]



def unmountBlockdevice(blockdeviceName):
    global command
    cmdString1 = f"{command1[0]}  {blockdeviceName}"  
    print(cmdString1)
    p = subprocess.run(cmdString1.split(), capture_output=True,  encoding="utf-8")
    time.sleep(1)
    cmdString2 = f"{command2[0]}  {blockdeviceName}"  
    print(cmdString2)
    p = subprocess.run(cmdString2.split(), capture_output=True,  encoding="utf-8")
    """ blkInfo = json.loads(p.stdout)["blockdevices"]
    for i in blkInfo:
        if i["vendor"] == None:
            i["vendor"] = "unknown"
        else:
            i["vendor"] = i["vendor"].strip()
        if i["size"].endswith("G"):
            i["size"] = i["size"].replace("G", " GB") """
    return f"Unmounted {blockdeviceName} successfully"
