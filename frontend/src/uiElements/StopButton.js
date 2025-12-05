import { useState, useEffect } from 'react';

import './StopButton.css';


function StopButton(props) {


    const handleStopButtonClick = (event) => {
        //event.preventDefault();
        //console.log(event.currentTarget.value)
        props.callbackStopButtonClick(event.currentTarget.value);
    }

    
    return (
        <div className = "stopButtonContainer">
            <button value = {props.blockdeviceIdentifier} 
                    disabled = {props.toggleActive === '' ? true : false}
                    onClick = {handleStopButtonClick}><b>Stop</b></button>
        </div>
    );
}

export default StopButton;