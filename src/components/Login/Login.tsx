import React, { useState } from 'react';
import InfoBox from '../InfoBox/InfoBox';
import { useHistory } from 'react-router-dom';
import './login.css'
import { Link } from 'react-router-dom';

const Login = () => {
    const history = useHistory()
    
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")

    const onUsernameChange = (event: React.FormEvent<HTMLInputElement>) => {
        setUsername(event.currentTarget.value)
    }

    const onPasswordChange = (event: React.FormEvent<HTMLInputElement>) => {
        setPassword(event.currentTarget.value)
    }

    const LoginRquest = (event: React.FormEvent) => {
        event.preventDefault()

        fetch('/api/login', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "login": username,
                "password": password
            })
        })
        .then(response => {
            return response.json()
        })
        .then(data => {
            if ('ok' in data) {
                history.push('/dashboard')
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
            <h1>retask</h1>
            <form onSubmit={LoginRquest}>
                <div className="input-box">
                    <input type="text" name="login" onChange={onUsernameChange} required autoComplete="off"/>
                    <label>Login</label>
                </div>

                <div className="input-box">
                    <input type="password" name="password" onChange={onPasswordChange} required/>
                    <label>Password</label>
                </div>

                <input type="submit" value="Login"/>
            </form>

            <div className="dashboard-button-box">
                <Link to="/dashboard" className="dashboard-button">go to dashboard</Link>
            </div>
        </>
    )
}

export default Login;