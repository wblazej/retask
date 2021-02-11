import React, { useState, useEffect } from 'react';
import Init from './../../components/Init/Init';
import Login from './../../components/Login/Login';

const Home = () => {
    const [loading, setLoading] = useState(true)
    const [inited, setInited] = useState(false)

    useEffect(() => {
        fetch('/api/init/check')
        .then(response => {
            if (response.status === 200)
                return response.json()
        })
        .then(data => {
            setInited(data.ok)
            setLoading(false)
        })
    }, [])

    if (inited === false && loading === false)
        return <Init/>
    else if (inited === true && loading === false)
        return <Login/>
    else
        return <></>
}

export default Home;