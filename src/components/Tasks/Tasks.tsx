import React, { useEffect, useState } from 'react';
import './tasks.css'
import {getDateFromTimestamp} from './../../ts/getDateFromTimestamp'
import InfoBox from './../InfoBox/InfoBox'

const Tasks = () => {
    const [tasks, setTasks] = useState(Array<any>())
    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    useEffect(() =>{
        fetch('/api/tasks/my/current')
        .then(response => {
            return response.json()
        })
        .then(data => {
            if ('ok' in data) {
                setTasks(data.ok.reverse())
            }
        })
    }, [])
    
    const solutionCheckChangeHandler = (Event: React.FormEvent<HTMLInputElement>, task_id: number, solution_id: number) => {
        let url = ''
        if (Event.currentTarget.checked)
            url = `/api/tasks/${task_id}/check/${solution_id}`
        else url = `/api/tasks/${task_id}/uncheck/${solution_id}`

        fetch(url)
        .then(response => {
            return response.json()
        })
        .then(data => {
            if ('ok' in data) showInfoBox('success', data.ok)
            else showInfoBox('failure', data.error)
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

            <h1>tasks</h1>
            { tasks.length === 0 && <p className='no-tasks'>no tasks for you<br/>#win</p> }

            <div className="tasks">
                { tasks.map((element: any) => {
                    return (
                        <div className="task" key={element.id}>
                            <div className="group">
                                <div style={{backgroundColor: `#${element.group_color}`}}></div><span>{element.group_name}</span>
                            </div>
                            <div className="title">{element.name}</div>
                            <div className="solutions">
                                { element.solutions.map((solution: any) => {
                                    return (
                                        <div className="row" key={solution.id}>
                                            <span className="name">{letters[solution.id - 1]}</span>
                                            { solution.checked === true && <input type="checkbox" checked onChange={(Event: React.FormEvent<HTMLInputElement>) => {solutionCheckChangeHandler(Event, element.id, solution.id)}} />}
                                            { solution.checked === false && <input type="checkbox" onChange={(Event: React.FormEvent<HTMLInputElement>) => {solutionCheckChangeHandler(Event, element.id, solution.id)}} />}
                                            <span className="points">{solution.points}</span>
                                        </div>
                                    )
                                })}
                            </div>
                            <span className="info">
                                Deadline: {getDateFromTimestamp(element.deadline)} <br/>
                                Your points: {element.points}
                            </span>
                        </div>
                    )
                })}
            </div>
        </>
    )
}

export default Tasks