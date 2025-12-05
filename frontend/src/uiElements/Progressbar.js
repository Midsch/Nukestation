import { useState, useEffect } from 'react';

import './Progressbar.css';


function Progressbar(props) {
    //const [progress, setProgress] = useState(props.progress);
    
    return (
        <div className = "progressbarContainer">
            <div className = "progressbar" style = {{width: `${props.progress}%`}}>
            </div>
        </div>
    );
}

export default Progressbar;