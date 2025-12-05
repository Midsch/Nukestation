import { useState, useEffect } from 'react';

import './DropdownMenu.css';


function DropdownMenu(props) {
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const [dropdownText, setDropdownText] = useState(props.initialDropdownText);
    const [disabled, setDisabled] = useState(props.buttonDisabled);
    
    useEffect(() => {
        if (props.buttonDisabled) {
            //console.log("triggered");
            handleDisableButton(props.buttonDisabled);
        } else if (!props.buttonDisabled) {
            //console.log("triggered");
            handleDisableButton(props.buttonDisabled);
        }
      }, [props.buttonDisabled]);

    
    const handleDropdownOpen = () => {
        setDropdownOpen(!dropdownOpen);
    }

    const handleDropdownSelect = (event) => {
        event.preventDefault();
        const dropdownIndex = event.target.attributes.index.value;
        let methodFlag = props.dropdownList[parseInt(dropdownIndex)]['methodFlag']

        //console.log(dropdownIndex);
        setDropdownText(event.target.value);
        //console.log(`handleDropdownSelect: ${methodFlag}`);
        handleGetMethod(methodFlag);
        handleDropdownOpen();
    }

    const handleGetMethod = (value) => {
        //console.log(value);
        props.callbackGetMethod(value);
    }

    const handleDisableButton = (b) => {
        setDisabled(b);
    }

    
    return (
        <div className = "dropdownMenuContainer">
            <button disabled = {disabled} onClick = {handleDropdownOpen}><span className = "dropdownMenuText">{dropdownText}</span><span className = "dropdownMenuArrow">&#709;</span></button>
            {dropdownOpen ? (
                <ul className="dropdownMenuEntries">
                    {props.dropdownList.map((item, index) => {
                        return (
                                <li key = {item['methodFlag']}>
                                <button value = {item['methodShortName']} index = {index} onClick = {handleDropdownSelect}>{item['methodName']}</button>
                                </li>
                        )})
                    }
                </ul>
            ) : null}
        </div>
    );
}

export default DropdownMenu;