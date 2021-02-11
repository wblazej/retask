import React, { useState, useEffect } from 'react';

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
            console.log(inited)
            setLoading(false)
        })
    }, [])

    if (inited === false) {
        return (
            <div>please, init</div>
        )
    }
    else {
        return (
            <div>plase, log in</div>
        )
    }
}

export default Home;