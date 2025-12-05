import { useState, useEffect } from 'react';

import './UnmountButton.css';


function UnmountButton(props) {


    const handleUnmountButtonClick = (event) => {
        //event.preventDefault();
        //console.log(event.currentTarget.value)
        props.callbackUnmountButtonClick(event.currentTarget.value);
        console.log(`handleUnmountButtonClick(): ${event.currentTarget.value}`)
    }

    
    return (
        <div className = "unmountButtonContainer">
            <button value = {props.blockdeviceIdentifier} 
                    onClick = {handleUnmountButtonClick}><b>Eject</b></button>
        </div>
    );
}

export default UnmountButton;