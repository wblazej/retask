import React, { useEffect, useState } from 'react'
import './studentsTasks.css'
import InfoBox from './../InfoBox/InfoBox'
import {
    BrowserRouter as Router,
    Route
} from "react-router-dom";
import Task from './Task'

const StudentsTasks = () => {
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

    const [name, setName] = useState(String)
    const [group, setGroup] = useState(String)
    const [deadline, setDeadline] = useState(Number)
    const [tasksCount, setTasksCount] = useState(1)

    const nameHandler = (Event: React.FormEvent<HTMLInputElement>) => {
        setName(Event.currentTarget.value)
    }

    const groupHandler = (Event: React.ChangeEvent<HTMLSelectElement>) => {
        setGroup(Event.currentTarget.value)
    }

    const deadlineHandler = (Event: React.FormEvent<HTMLInputElement>) => {
        setDeadline(new Date(Event.currentTarget.value).getTime())
    }

    const tasksCountHandler = (Event: React.FormEvent<HTMLInputElement>) => {
        setTasksCount(parseInt(Event.currentTarget.value))
    }

    const createTask = (Event: React.FormEvent) => {
        Event.preventDefault()

        if (group === '' || group === 'null') {
            showInfoBox('failure', "Choose task group")
            return
        }

        fetch('/api/tasks/create', {
            headers: {
                "Content-Type": "application/json"
            },
            method: 'post',
            body: JSON.stringify({
                "name": name,
                "group-id": group,
                "tasks-count": tasksCount,
                "deadline": deadline
            })
        })
        .then(response => {
            return response.json()
        })
        .then(data => {
            if ('ok' in data) {
                showInfoBox('success', data.ok)
                setName("")
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
            <Router>
                <Route exact path='/dashboard/tasks'>
                    { infoBox.type !== '' && <InfoBox type={infoBox.type} message={infoBox.message} />}

                    <h1>student's tasks</h1>
                    <h2>Create new task</h2>

                    <form className="create-task-form" onSubmit={createTask}>
                        <div className="input-box">
                            <input type="text" value={name} onChange={nameHandler} required />
                            <label>Name</label>
                        </div>

                        <div className="input-box">
                            <select onChange={groupHandler} required>
                                <option value="null">Choose group</option>
                                { optionsGroups.map((element: any) => {
                                    return (
                                        <option key={element.id} value={element.id}>{element.name}</option>
                                    )
                                })}
                            </select>
                        </div>

                        <br/>

                        <div className="input-box">
                            <span>Deadline</span>
                            <input type="datetime-local" onChange={deadlineHandler} required />
                        </div>

                        <div className="input-box">
                            <span>Tasks count</span>
                            <input defaultValue="1" onChange={tasksCountHandler} type="number" min="1" max="26" required />
                        </div>

                        <br/>

                        <input type="submit" value="Create task"/>
                    </form>

                    <h2>Student's solutions</h2>
                    <div className="groups">
                        { optionsGroups.map((element: any) => {
                            return (
                                <a key={element.id} href={`/dashboard/tasks/${element.id}`} className="group-button">
                                    <div style={{backgroundColor: `#${element.color}`}}></div>
                                    {element.name}
                                </a>
                            )
                        })}
                    </div>
                </Route>
                <Route exact path='/dashboard/tasks/:id' component={Task}></Route>
            </Router>
        </>
    )
}

export default StudentsTasks;