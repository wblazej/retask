import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom'
import InfoBox from './../InfoBox/InfoBox'
import {getDateFromTimestamp} from './../../ts/getDateFromTimestamp'

const Task = () => {
    const params: any = useParams()

    const [tasks, setTasks] = useState(Array<object>())

    useEffect(() => {
        fetch(`/api/tasks/${params.id}`)
        .then(response => {
            return response.json()
        })
        .then(data => {
            if ('ok' in data) {
                setTasks(data.ok)
            }
            else {
                showInfoBox('failure', data.error)
            }
        })
    }, [params])

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
            
            <table className="tasks">
                <tbody>
                    <tr className="header">
                        <td>ID</td>
                        <td>Name</td>
                        <td>Active</td>
                        <td>Deadline</td>
                    </tr>
                    { tasks.map((element: any) => {
                        return (
                            <tr>
                                <td>{element.id}</td>
                                <td><a href={`/dashboard/tasks/solutions/${element.id}`}>{element.name}</a></td>
                                { element.expired === false && <td>Yes</td> }
                                { element.expired === true && <td>No</td> }
                                <td>{getDateFromTimestamp(element.deadline)}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
        </>
    )
}

export default Task;