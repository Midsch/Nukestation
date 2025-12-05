import { React, useState, useEffect } from 'react';

import DropdownMenu from '../uiElements/DropdownMenu.js';
import StartButton from '../uiElements/StartButton.js';
import StopButton from '../uiElements/StopButton.js';
import Progressbar from '../uiElements/Progressbar.js';
import StatusDisplay from '../uiElements/StatusDisplay.js';
import UnmountButton from '../uiElements/UnmountButton.js';


import './BlockdeviceCard.css';
//import iconHDD from '../icons/icon-hdd-100x100.png'

var logfileDir = '/home/pi/Nukestation/log/'


const dropdownList = [{
                        'methodName': 'Overwrite with zeros',                    
                        'methodShortName': 'Zeros',
                        'methodFlag': 'zero',
                      }, {
                        'methodName': 'Overwrite with ones',
                        'methodShortName': 'Ones',
                        'methodFlag': 'one',
                      }, {
                        'methodName': 'Overwrite with PRNG Stream (PRNG: Mersenne Twister)',
                        'methodShortName': 'Random (Mersenne)',
                        'methodFlag': 'random --prng=mersenne',
                    }, {
                        'methodName': 'Overwrite with PRNG Stream (PRNG: ISAAC)',
                        'methodShortName': 'Random (ISAAC)',
                        'methodFlag': 'random --prng=isaac',
                    }, {
                        'methodName': 'Overwrite with PRNG Stream (PRNG: ISAAC64)',
                        'methodShortName': 'Random ISAAC64',
                        'methodFlag': 'random --prng=isaac64',
                      }, {
                        'methodName': 'RCMP TSSIT OPS-II',
                        'methodShortName': 'OPS-II',
                        'methodFlag': 'ops2',
                      }, {
                        'methodName': 'HMG IS5 enhanced',
                        'methodShortName': 'IS5 enhanced',
                        'methodFlag': 'is5enh',
                      }, {
                        'methodName': "Peter Gutmann's Algorithm",
                        'methodShortName': "Gutmann",
                        'methodFlag': 'gutmann',
                      }, {
                        'methodName': '3 pass DOD method',
                        'methodShortName': 'DOD short',
                        'methodFlag': 'dodshort',
                      }, {
                        'methodName': '7 pass DOD 5220.22-M method',
                        'methodShortName': 'DOD 522022M',
                        'methodFlag': 'dod522022m',
                      }];

function BlockdeviceCard(props) {
    const [wipeActive, setWipeActive] = useState(false);
    const [wipeMethod, setWipeMethod] = useState('');
    const [progress, setProgress] = useState(-1);
    const [status, setStatus] = useState(-1);
    //->const [pid, setPid] = useState(-1);

    useEffect(() => {
        if (wipeActive) {
            const interval = setInterval(() => {
                //getBlockdeviceInfo();
                props.getWipeProgressCallback(`${logfileDir}`, `${props.vendor}_${props.serial}.log`, `${props.name}`, setProgress, setStatus);
                //console.log(pr);
                //setProgress(pr);
              }, 2000);
              return () => clearInterval(interval);
        }
    });
    
    const handleStartButtonClick = () => {
        let wipeCommand = `sudo nwipe --autonuke --nogui --method=${wipeMethod}`;
        wipeCommand = wipeCommand + ' ' + `--logfile=${logfileDir}${props.vendor}_${props.serial}.log`;
        wipeCommand = wipeCommand + ' ' + props.name;

        console.log(wipeCommand);
        setWipeActive(true);
        props.setWipeCommandCallback(wipeCommand);
    }

    const handleStopButtonClick = () => {
        console.log('Stop wipe process');
        setWipeActive(false);
        setProgress(-1);
        console.log(`kill process: ${props.name}`);
        props.setKillCommandCallback(props.name);
    }

    const handleUnmountButtonClick = (blockdeviceName) => {
        console.log('Unmount blockdevice');
        setWipeActive(false);
        setProgress(-1);
        props.setUnmountCommandCallback(blockdeviceName);
    }

    const getMethod = (method) => {
        //console.log(method);
        setWipeMethod(method);
    }

    const renderConditionalButton = () => {
        if (wipeActive) {
            if (progress === '100') {
                console.log(`progress: ${progress}`);
                return <UnmountButton blockdeviceIdentifier = {props.name} callbackUnmountButtonClick = {handleUnmountButtonClick}/>
            } else {
                return <StopButton blockdeviceIdentifier = {props.name} toggleActive = {wipeMethod} callbackStopButtonClick = {handleStopButtonClick}/>
            }
        } else {
            return <StartButton blockdeviceIdentifier = {props.name} toggleActive = {wipeMethod} callbackStartButtonClick = {handleStartButtonClick}/> 
        }
    }
    
    return (
        <div className = 'blockdeviceCardContainer' style = {{zIndex: `${props.zIndex}`}}>
            <div className = 'blockdeviceCardRow'>
                {/*<div className = 'blockdeviceCardColumnIcon'>
                    <div className = 'blockdeviceCardIconContainer'>
                        <img src = {iconHDD} alt = "HDD Icon" style = {{width:'100%'}}/>
                    </div>
                </div>*/}
                <div className = 'blockdeviceCardColumnVendor'>
                    <h1>{props.vendor}</h1>
                    <p>{props.name}</p>
                </div>
                <div className = 'blockdeviceCardColumnSize'>
                    <p>Size:</p>
                    <h3>{props.size}</h3>
                </div>
                <div className = 'blockdeviceCardColumnSerial'>
                    <p>Serial:</p>
                    <h3>{props.serial}</h3>
                </div>
                <div className = 'blockdeviceCardColumnDropdown'>
                    <DropdownMenu dropdownList = {dropdownList}
                                  initialDropdownText = {'Choose wipe method'}
                                  callbackGetMethod = {getMethod}
                                  buttonDisabled = {wipeActive}/>
                </div>
                <div className = 'blockdeviceCardColumnAction'>
                    {renderConditionalButton()}
                </div>
            </div>
                <>
                {progress != -1 ? 
                    <>
                        <Progressbar progress = {progress}/>
                        <StatusDisplay progress = {progress} status = {status}/>
                    </>
                : null
                }
            </>
        </div>
    );
}

export default BlockdeviceCard;