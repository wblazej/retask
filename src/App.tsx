import React from 'react';
import {
    BrowserRouter as Router,
    Route
} from "react-router-dom";

import Home from './pages/Home/Home';
import Dashboard from './pages/Dashboard/Dashboard';

function App() {
    return (
        <>
            <Router>
                <Route exact path='/' component={Home}></Route>
                <Route exact path='/dashboard' component={Dashboard}></Route>
            </Router>
        </>
    );
}

export default App;