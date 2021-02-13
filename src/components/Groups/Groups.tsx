import React, { useState } from 'react';
import './groups.css'
import InfoBox from './../InfoBox/InfoBox'

const Groups = () => {
    const Colors = [ "#D41515", "#E09B34", "#F0E73A", "#68C724", "#2ED1C4", "#2E90D1", "#1225B3", "#E349EB", "#FFFFFF"]

    const [name, setName] = useState("")
    const [color, setColor] = useState("")

    const nameChangeHandler = (Event: React.FormEvent<HTMLInputElement>) => { 
        setName(Event.currentTarget.value) 
    }

    const colorChangeHanlder = (Event: React.FormEvent<HTMLInputElement>) => { 
        setColor(Event.currentTarget.value) 
    }

    const getStyles = (_color: string) => { 
        return {backgroundColor: _color} 
    }

    const colorClickHandler = (_color: string) => { 
        setColor(_color) 
    }
    
    const createGroup = (Event: React.FormEvent) => {
        Event.preventDefault()

        fetch('/api/groups/create', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "name": name,
                "color": color.substring(1)
            })
        })
        .then(response => {
            return response.json()
        })
        .then(data => {
            if ('ok' in data) {
                showInfoBox('success', data.ok)
                setName('')
                setColor('')
            }
            else {
                showInfoBox('failure', data.error)
            }
        })
    }

    const [infoBox, setInfoBox] = useState({type: '', message: ''})
    const showInfoBox = (type: string, message: string) => {
        if (infoBox.type === '') {
            setInfoBox({type: type, message: message})
            setTimeout(() => setInfoBox({type: '', message: ''}), 4000)
        }
    }

    return (
        <>
            { infoBox.type !== '' && <InfoBox type={infoBox.type} message={infoBox.message} />}
            <h1>groups</h1>
            <h2>Create group</h2>
            <div className="colors">
                { Colors.map((element_color) => {
                    return (
                        <div key={element_color} className="color" style={getStyles(element_color)} onClick={() => { colorClickHandler(element_color) }}></div>
                    )
                })}
            </div>
            <form className="new-group-name" onSubmit={createGroup}>
                <div className="input-box">
                    <input type="text" name="name" value={name} onChange={nameChangeHandler} required autoComplete="off" />
                    <label>Name</label>
                </div>
                <div className="input-box">
                    <input type="text" name="color" value={color} onChange={colorChangeHanlder} required autoComplete="off" />
                    <label>Color</label>
                </div>
                <input type="submit" value="Create group"/>
            </form>
        </>
    )
}

export default Groups;