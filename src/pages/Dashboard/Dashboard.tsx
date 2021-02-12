import React, { useEffect, useState } from 'react';
import UserInfo from './../../components/UserInfo/UserInfo'
import Menu from './../../components/Menu/Menu'
import { useHistory } from 'react-router-dom'
import './dashboard.css'
import ChangePassword from './../../components/ChangePassword/ChangePassword'

import {
    BrowserRouter as Router,
    Route
} from "react-router-dom";

const Dashboard = () => {
    const history = useHistory()

    const [username, setUsername] = useState("")
    const [type, setType] = useState("")

    useEffect(() => {
        fetch('/api/info')
        .then(response => {
            if (response.status === 200) 
                return response.json()
        })
        .then(data => {
            if ('error' in data) {
                if (data.error === "NOT_LOGGED_IN")
                    history.push('/')
            }
            else {
                setUsername(data.username)
                setType(data.type)
            }
        })
    }, [history])

    return (
        <>
            <UserInfo username={username} />
            <div className="dashboard">
                <div className="menu-box">
                    <Menu type={type}/>
                </div>

                <div className="content">
                    <Router>
                        <Route path='/dashboard/change-password' component={ChangePassword}></Route>
                    </Router>
                </div>
            </div>
        </>
    )
}

export default Dashboard;