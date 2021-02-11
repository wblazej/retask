import React, {useState} from 'react';
import './init.css'
import InfoBox from '../../components/InfoBox/InfoBox'

const Init = () => {
    const InitApp = () => {
        fetch('/api/init')
        .then(response => {
            return response.json()
        })
        .then(data => {
            if ('ok' in data)
                showInfoBox('success', data.ok)
            else
                showInfoBox('failure', data.error)
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
            <h1>initialization</h1>
            <div className="init-button" onClick={InitApp}>init app</div>
        </>
    )
}

export default Init;