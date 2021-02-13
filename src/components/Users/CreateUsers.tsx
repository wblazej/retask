import React, { useEffect, useState } from 'react';
import InfoBox from './../InfoBox/InfoBox'

const CreateUsers = () => {
    const [count, setCount] = useState(1)
    const countChangeHandler = (Event: React.FormEvent<HTMLInputElement>) => { 
        setCount(parseInt(Event.currentTarget.value)) 
    }

    const [optionsGroups, setOptionsGroups] = useState(Array<object>())

    useEffect(() => {
        fetch('/api/groups')
        .then(response => {
            return response.json()
        })
        .then(data => {
            if ('ok' in data) {
                setOptionsGroups(data.ok)
            }
        })
    }, [])

    const [usernames] = useState(Array<string>())
    const [groups] = useState(Array<string>())
    const [adminStatus] = useState(Array<boolean>())

    const setUsername = (Event: React.FormEvent<HTMLInputElement>, id: number) => {
        usernames[id] = Event.currentTarget.value
    }

    const setGroup = (Event: React.ChangeEvent<HTMLSelectElement>, id: number) => {
        groups[id] = Event.currentTarget.value
    }

    const setAdminStatus = (Event: React.FormEvent<HTMLInputElement>, id: number) => {
        adminStatus[id] = Event.currentTarget.checked
    }

    const elements: JSX.Element[] = []
    for (let i = 0; i < count; i++) {
        elements.push(
            <div className="row" key={i}>
                <div className="input-box">
                    <input type="text" onChange={(Event: React.FormEvent<HTMLInputElement>) => setUsername(Event, i)} required/>
                    <label>Username</label>
                </div>
                <div className="input-box">
                    <select onChange={(Event: React.ChangeEvent<HTMLSelectElement>) => setGroup(Event, i)}>
                        <option value="null">Without group</option>
                        { optionsGroups.map((element: any) => {
                            return (
                                <option key={element.id} value={element.id}>{element.name}</option>
                            )
                        })}
                    </select>
                </div>
                <div className="input-box checkbox-container">
                    <div className="inner">
                        <input type="checkbox" onChange={(Event: React.FormEvent<HTMLInputElement>) => setAdminStatus(Event, i)} />
                        <label>Admin</label>
                    </div>
                </div>
            </div>
        )
    }

    const [defaultPassword, setDefaultPassword] = useState("")
    const [defaultGroup, setDefaultGroup] = useState("")
    
    const defaultPasswordHandler = (Event: React.FormEvent<HTMLInputElement>) => {
        setDefaultPassword(Event.currentTarget.value)
    }
    const defaultGroupHandler = (Event: React.ChangeEvent<HTMLSelectElement>) => {
        setDefaultGroup(Event.currentTarget.value)
    }

    const createUsers = (Event: React.FormEvent) => {
        Event.preventDefault()

        const body = {
            "default-password": defaultPassword,
            "default-groups": Array<number>(),
            "accounts": Array<object>()
        }

        if (defaultGroup !== '' && defaultGroup !== 'null')
            body['default-groups'].push(parseInt(defaultGroup))

        for (let i = 0; i < usernames.length; i++) {
            const account = {
                username: usernames[i],
                groups: Array<number>(),
                admin: false
            }

            if (groups[i])
                account.groups.push(parseInt(groups[i]))

            if (adminStatus[i] === true)
                account.admin = true

            body.accounts.push(account)
        }

        fetch('/api/users/create', {
            headers: {
                "Content-Type": "application/json"
            },
            method: 'post',
            body: JSON.stringify(body)
        })
        .then(response => {
            return response.json()
        })
        .then(data => {
            if ('ok' in data) {
                showInfoBox('success', data.ok)
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

            <h1>create users</h1>

            <form className="create-users-form" onSubmit={createUsers}>
                <span className="count-label">Count</span>
                <input type="number" defaultValue="1" name="count" min="1" max="30" onChange={countChangeHandler} />

                <div className="input-box">
                    <input type="password" required value={defaultPassword} onChange={defaultPasswordHandler} />
                    <label>Default password</label>
                </div>

                <div className="input-box">
                    <select onChange={defaultGroupHandler}>
                        <option value="null">Default group</option>
                        { optionsGroups.map((element: any) => {
                            return (
                                <option key={element.id} value={element.id}>{element.name}</option>
                            )
                        })}
                    </select>
                </div>

                {elements}
                <input type="submit" value="Create users"/>
            </form>
        </>
    )
}

export default CreateUsers;