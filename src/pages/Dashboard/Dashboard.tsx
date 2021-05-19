import React, { useEffect, useState } from 'react';
import UserInfo from './../../components/UserInfo/UserInfo'
import Menu from './../../components/Menu/Menu'
import { useHistory } from 'react-router-dom'
import './dashboard.css'
import ChangePassword from './../../components/ChangePassword/ChangePassword'
import Groups from './../../components/Groups/Groups'
import Users from './../../components/Users/Users'
import StudentsTasks from './../../components/StudentsTasks/StudentsTasks'
import Tasks from './../../components/Tasks/Tasks'
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

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
                <Router>
                    <div className="menu-box">
                        <Menu type={type}/>
                    </div>

                    <div className="content">
                        <Switch>
                            <Route path='/dashboard/change-password' component={ChangePassword}></Route>
                            <Route path='/dashboard/groups' component={Groups}></Route>
                            <Route path='/dashboard/users' component={Users}></Route>
                            <Route path='/dashboard/tasks' component={StudentsTasks}></Route>
                            <Route exact path='/dashboard' component={Tasks}></Route>
                        </Switch>
                    </div>
                </Router>
            </div>
        </>
    )
}

export default Dashboard;