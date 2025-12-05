import { useState, useEffect } from 'react';

import './StartButton.css';


function StartButton(props) {


    const handleStartButtonClick = (event) => {
        //event.preventDefault();
        //console.log(event.currentTarget.value)
        props.callbackStartButtonClick(event.currentTarget.value);
    }

    
    return (
        <div className = "startButtonContainer">
            <button value = {props.blockdeviceIdentifier} 
                    disabled = {props.toggleActive === '' ? true : false}
                    onClick = {handleStartButtonClick}><b>Start</b></button>
        </div>
    );
}

export default StartButton;