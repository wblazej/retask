import React from 'react';
import './userInfo.css'

const UserInfo = () => {
    return (
        <>
            <div className="user-info">
                <div className="logout">Logout</div>
                <span className="username">Logged in as: root</span>
            </div>
        </>
    )
}

export default UserInfo;