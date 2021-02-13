import React, { useState } from 'react';
import './changePassword.css'
import InfoBox from './../../components/InfoBox/InfoBox'

const ChangePassword = () => {
    const [currentPassword, setCurrentPassword] = useState("")
    const [newPassword, setNewPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")

    const currentPasswordHanlder = (Event: React.FormEvent<HTMLInputElement>) => {
        setCurrentPassword(Event.currentTarget.value)
    }

    const newPasswordHanlder = (Event: React.FormEvent<HTMLInputElement>) => {
        setNewPassword(Event.currentTarget.value)
    }

    const confirmPasswordHandler = (Event: React.FormEvent<HTMLInputElement>) => {
        setConfirmPassword(Event.currentTarget.value)
    }

    const changePassword = (Event: React.FormEvent) => {
        Event.preventDefault()

        fetch('/api/users/change-password', {
            method: 'post',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                password: currentPassword,
                new_password: newPassword,
                confirm_password: confirmPassword
            })
        })
        .then(response => {
            return response.json()
        })
        .then(data => {
            if ('ok' in data) {
                showInfoBox('success', data.ok)
                setCurrentPassword("")
                setNewPassword("")
                setConfirmPassword("")
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
            <h1>change password</h1>
            <form className="change-password-form" onSubmit={changePassword}>
                <div className="input-box">
                    <input type="password" name="current-password" onChange={currentPasswordHanlder} value={currentPassword} required/>
                    <label>Current password</label>
                </div>
                <div className="input-box">
                    <input type="password" name="new-password" onChange={newPasswordHanlder} value={newPassword} required/>
                    <label>New password</label>
                </div>
                <div className="input-box">
                    <input type="password" name="confirm-password" onChange={confirmPasswordHandler} value={confirmPassword} required/>
                    <label>Confirm password</label>
                </div>
                <input type="submit" value="Change password"/>
            </form>
        </>
    )
}

export default ChangePassword;