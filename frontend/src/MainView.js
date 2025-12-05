import { useState, useEffect } from 'react';

import BlockdeviceCard from './uiElements/BlockdeviceCard';
import './MainView.css';

// optional für Tests
import blockdevices from './blockdevices';

function MainView(props) {
  const [blockdeviceInfo, setBlockdeviceInfo] = useState([]);

  useEffect(() => {
    // direkt beim Mount einmal holen
    getBlockdeviceInfo();

    // dann alle 5 Sekunden pollen
    const interval = setInterval(() => {
      getBlockdeviceInfo();
      // dummyGetBlockdeviceInfo();     //Dummy für Testzwecke
    }, 5000);

    // beim Unmount Interval aufräumen
    return () => clearInterval(interval);
  }, []);

  const dummyGetBlockdeviceInfo = () => {
    setBlockdeviceInfo(blockdevices);
  };

  async function getBlockdeviceInfo() {
    try {
      const response = await fetch('/getBlockdeviceInfo');
      const data = await response.json();

      // falls dein Backend direkt ein Array liefert:
      const devices = Array.isArray(data) ? data : data.message;

      // Fallback: wenn nichts da ist, leeres Array
      setBlockdeviceInfo(devices || []);
    } catch (error) {
      console.error('Fehler beim Laden der Blockdevice-Infos:', error);
    }
  }

  async function sendKillCommand(payload) {
    try {
      const response = await fetch('/kill', {
        method: 'POST',
        body: JSON.stringify({
          command: payload,
        }),
        headers: {
          'Content-type': 'application/json; charset=UTF-8',
        },
      });
      const res = await response.json();
      console.log('Kill-Response:', res);
    } catch (error) {
      console.error('Error bei /kill:', error);
    }
  }

  async function sendUnmountCommand(payload) {
    try {
      const response = await fetch('/unmount', {
        method: 'POST',
        body: JSON.stringify({
          blockdeviceName: payload,
        }),
        headers: {
          'Content-type': 'application/json; charset=UTF-8',
        },
      });
      const res = await response.json();
      console.log('Unmount-Response:', res);

      // nach dem Unmount Liste leeren (oder neu laden)
      setBlockdeviceInfo([]);
      // oder: getBlockdeviceInfo();
    } catch (error) {
      console.error('Error bei /unmount:', error);
    }
  }

  async function sendWipeCommand(payload) {
    try {
      const response = await fetch('/sendWipeCommand', {
        method: 'POST',
        body: JSON.stringify({
          command: payload,
        }),
        headers: {
          'Content-type': 'application/json; charset=UTF-8',
        },
      });
      const res = await response.json();
      console.log('Wipe-Response:', res);
    } catch (error) {
      console.error('Error bei /sendWipeCommand:', error);
    }
  }

  /* get progress of wipe */
  async function getWipeProgress(
    logfileDir,
    logfileName,
    blockdeviceName,
    setProgress,
    setStatus
  ) {
    try {
      const response = await fetch('/progress', {
        method: 'POST',
        body: JSON.stringify({
          logfileDir: logfileDir,
          logfileName: logfileName,
          blockdeviceName: blockdeviceName,
        }),
        headers: {
          'Content-type': 'application/json; charset=UTF-8',
        },
      });
      const res = await response.json();

      if (res.progress && res.progress.length > 0) {
        // bspw. [{ type: 'progress', text: '23' }, ...]
        const first = res.progress[0];
        const last = res.progress[res.progress.length - 1];

        console.log(first.text);
        console.log(last.text, last.type);

        setStatus(last.text);

        if (last.type === 'success') {
          setProgress('100');
          console.log('100%');
        } else {
          setProgress(first.text);
        }
      }
    } catch (error) {
      console.error('Error bei /progress:', error);
    }
  }

  return (
    <div className="mainviewContainer">
      {/* Debug-Ausgabe ohne Crash-Gefahr */}
      {Array.isArray(blockdeviceInfo) && blockdeviceInfo.length > 0 && (
        console.log('Erstes Device:', blockdeviceInfo[0])
      )}

      {Array.isArray(blockdeviceInfo) &&
        blockdeviceInfo.map((item, index) => (
          <BlockdeviceCard
            key={item.serial || item.name || index}
            name={item.name}
            vendor={item.vendor}
            serial={item.serial}
            size={item.size}
            zIndex={20 - index}
            setWipeCommandCallback={sendWipeCommand}
            setKillCommandCallback={sendKillCommand}
            getWipeProgressCallback={getWipeProgress}
            setUnmountCommandCallback={sendUnmountCommand}
          />
        ))}
    </div>
  );
}

export default MainView;