import React from 'react';
import './users.css'
import {
    BrowserRouter as Router,
    Route
} from "react-router-dom";
import CreateUsers from './CreateUsers'

const Users = () => {
    return (
        <>
            <Router>
                <Route exact path='/dashboard/users/create' component={CreateUsers}></Route>
                <Route exact path='/dashboard/users'>
                    <h1>users</h1>
                </Route>
            </Router>
        </>
    )
}

export default Users;