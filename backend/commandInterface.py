import subprocess
import os
import shlex
import signal
import time

# Pfad zu nwipe (mit `which nwipe` prüfen!)
NWIPE_BIN = "/usr/local/bin/nwipe"

# Basispfad für PID-Dateien
PID_DIR = "/tmp"


def _device_to_pidfile(blockdevice_name: str) -> str:
    """
    /dev/sda -> /tmp/nukestation_nwipe_dev_sda.pid
    """
    safe = blockdevice_name.replace("/", "_")
    return os.path.join(PID_DIR, f"nukestation_nwipe{safe}.pid")


def _normalize_command(args: str):
    """
    Entfernt 'sudo' und ersetzt 'nwipe' durch NWIPE_BIN.
    """
    parts = shlex.split(args)

    if not parts:
        raise ValueError("empty command string")

    # sudo vorne weg
    if parts[0] == "sudo":
        parts = parts[1:]

    # nwipe durch absoluten Pfad ersetzen
    if parts[0] == "nwipe":
        parts[0] = NWIPE_BIN

    return parts


def executeCommand(args: str):
    """
    args: kompletter Befehl als String, z.B.
          'sudo nwipe --autonuke --nogui --method=one --logfile=... /dev/sda'

    - normalisiert den Command
    - findet das Blockdevice (Token mit '/dev/')
    - startet nwipe
    - schreibt die PID in eine PID-Datei pro Blockdevice
    """
    print(f'[executeCommand] raw command received: {args}', flush=True)

    parts = _normalize_command(args)
    print(f'[executeCommand] normalized command: {" ".join(parts)}', flush=True)

    # Blockdevice ermitteln (letztes Token mit '/dev/')
    blockdevice_name = None
    for token in reversed(parts):
        if token.startswith("/dev/"):
            blockdevice_name = token
            break

    if blockdevice_name is None:
        raise ValueError(f"no /dev/... blockdevice found in command: {args}")

    print(f'[executeCommand] blockdevice: {blockdevice_name}', flush=True)

    # Prozess starten
    p = subprocess.Popen(parts)
    pid = p.pid
    print(f'[executeCommand] nwipe PID for {blockdevice_name}: {pid}', flush=True)

    # PID-Datei schreiben
    pidfile = _device_to_pidfile(blockdevice_name)
    try:
        with open(pidfile, "w") as f:
            f.write(str(pid))
        print(f'[executeCommand] wrote PID file: {pidfile}', flush=True)
    except OSError as e:
        print(f'[executeCommand] ERROR writing PID file {pidfile}: {e}', flush=True)

    return pid


def executeKill(blockdeviceName: str):
    """
    Beendet den nwipe-Prozess für das angegebene Blockdevice.

    Ablauf:
    1. PID-Datei lesen und gezielt SIGTERM -> ggf. SIGKILL schicken
    2. Fallback: pkill -f auf Kommandozeile mit NWIPE_BIN und blockdeviceName
    """
    print(f'[executeKill] called for blockdevice: {blockdeviceName}', flush=True)

    pidfile = _device_to_pidfile(blockdeviceName)
    pid = None

    # 1) Versuch: PID aus PID-Datei
    if os.path.exists(pidfile):
        try:
            with open(pidfile, "r") as f:
                content = f.read().strip()
                if content:
                    pid = int(content)
            print(f'[executeKill] read PID {pid} from {pidfile}', flush=True)
        except Exception as e:
            print(f'[executeKill] ERROR reading PID file {pidfile}: {e}', flush=True)

    # 1a) Wenn wir eine PID haben: gezielt killen
    if pid is not None:
        try:
            os.kill(pid, signal.SIGTERM)
            print(f'[executeKill] sent SIGTERM to PID {pid}', flush=True)
        except ProcessLookupError:
            print(f'[executeKill] PID {pid} does not exist anymore', flush=True)
        except PermissionError as e:
            print(f'[executeKill] PermissionError on SIGTERM to {pid}: {e}', flush=True)

        # kurz warten, ob Prozess weg ist
        for i in range(10):
            try:
                os.kill(pid, 0)  # existiert Prozess noch?
                time.sleep(0.5)
            except ProcessLookupError:
                print(f'[executeKill] PID {pid} terminated after SIGTERM', flush=True)
                break
        else:
            # lebt immer noch -> SIGKILL
            try:
                os.kill(pid, signal.SIGKILL)
                print(f'[executeKill] sent SIGKILL to PID {pid}', flush=True)
            except ProcessLookupError:
                print(f'[executeKill] PID {pid} died before SIGKILL', flush=True)
            except PermissionError as e:
                print(f'[executeKill] PermissionError on SIGKILL to {pid}: {e}', flush=True)

        # PID-Datei aufräumen
        try:
            os.remove(pidfile)
            print(f'[executeKill] removed PID file {pidfile}', flush=True)
        except OSError:
            pass

    # 2) Fallback: pkill -f mit eindeutigem Pattern
    pattern = f"{NWIPE_BIN} .* {blockdeviceName}"
    print(f"[executeKill] fallback pkill -f '{pattern}'", flush=True)
    rc = os.system(f"pkill -f '{pattern}'")
    print(f"[executeKill] pkill return code: {rc}", flush=True)

    if pid is not None or rc == 0:
        return "killed"
    else:
        return "no-match"