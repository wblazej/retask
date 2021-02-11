import React from 'react';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from "react-router-dom";

import Home from './components/home/home';

function App() {
    return (
        <Router>
            <Route path='/' component={Home}></Route>
        </Router>
    );
}

export default App;