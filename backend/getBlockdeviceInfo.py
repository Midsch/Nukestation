import subprocess
#import os
import json


#cmdString = ["lsblk --json -p -o NAME,VENDOR,SIZE,SERIAL,TYPE,MAJ:MIN --exclude 1"]
cmdString = ["/usr/bin/lsblk --json -p -o NAME,VENDOR,SIZE,SERIAL,TYPE,MAJ:MIN --exclude 1,179"]



def getBlockdeviceInfo():
    p = subprocess.run(cmdString[0].split(), capture_output=True,  encoding="utf-8")
    blkInfo = json.loads(p.stdout)["blockdevices"]
    #print(blkInfo)
    for i in blkInfo:
        if i["vendor"] == None:
            i["vendor"] = "unknown"
        else:
            i["vendor"] = i["vendor"].strip()
        if i["size"].endswith("G"):
            i["size"] = i["size"].replace("G", " GB")
    #print(blkInfo)
    return blkInfo
