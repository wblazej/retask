import React from 'react';
import './userInfo.css'
import { useHistory } from 'react-router-dom';

type Props = {
    username: string
}

const UserInfo: React.FunctionComponent<Props> = ({ username }) => {
    const history = useHistory()

    const logout = () => {
        fetch('/api/logout', {
        })
        .then(response => {
            if (response.status === 200) 
                return response.json()
        })
        .then(data => {
            if ('ok' in data) {
                history.push('/')
            }
        })
    }

    return (
        <>
            <div className="user-info">
                <div className="logout" onClick={logout}>Logout</div>
                <span className="username">Logged in as: {username}</span>
            </div>
        </>
    )
}

export default UserInfo;