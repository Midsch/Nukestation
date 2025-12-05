import subprocess
import os
import signal
import threading
import time


nwipePID = None

def executeCommand(args):
    print(f'command executed: {args}')

    p = subprocess.Popen(args.split())
    global nwipePID
    nwipePID = p.pid
    print(f'nwipe process id: {nwipePID}')
    return nwipePID

def executeKill(blockdeviceName):
    os.system(f'pkill -f {blockdeviceName}')
    return 'success'