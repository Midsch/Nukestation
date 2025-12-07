import subprocess
import os
import signal
import threading
import time
import shlex

# Absoluter Pfad zu nwipe (mit `which nwipe` prüfen!)
NWIPE_BIN = "/usr/local/bin/nwipe"

nwipePID = None


def executeCommand(args: str):
    """
    args: kompletter Befehl als String, z.B.
          'sudo nwipe --autonuke --nogui --method=zero --logfile=/.../log.log /dev/sda'

    - entfernt 'sudo'
    - ersetzt 'nwipe' durch den absoluten Pfad NWIPE_BIN
    - startet den Prozess und speichert die PID in nwipePID
    """
    print(f'raw command received: {args}')

    # In Teile splitten (beachtet auch Anführungszeichen korrekt)
    parts = shlex.split(args)

    if not parts:
        raise ValueError("empty command string")

    # Falls vorne 'sudo' steht, entfernen – wir laufen idealerweise als root-Service
    if parts[0] == "sudo":
        parts = parts[1:]

    # 'nwipe' durch absoluten Pfad ersetzen
    if parts[0] == "nwipe":
        parts[0] = NWIPE_BIN

    # Debug-Ausgabe
    print(f'command executed (normalized): {" ".join(parts)}')

    # Prozess starten
    p = subprocess.Popen(parts)
    global nwipePID
    nwipePID = p.pid
    print(f'nwipe process id: {nwipePID}')
    return nwipePID


def executeKill(blockdeviceName: str):
    """
    Beendet alle Prozesse, die den Blockdevice-Namen im Command enthalten.
    (Wie bisher per pkill -f)
    """
    os.system(f'pkill -f {blockdeviceName}')
    return 'success'