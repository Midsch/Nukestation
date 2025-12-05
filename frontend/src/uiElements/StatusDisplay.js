import { useState, useEffect } from 'react';

import './StatusDisplay.css';


function StatusDisplay(props) {
    //const [progress, setProgress] = useState(props.progress);
    
    return (
        <div className = "statusDisplayContainer">
            <p>Progress: {props.progress}% - Status: {props.status}</p>
        </div>
    );
}

export default StatusDisplay;