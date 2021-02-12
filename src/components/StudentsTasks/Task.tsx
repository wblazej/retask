import React from 'react';
import { useParams } from 'react-router-dom'

const Task = () => {
    const params: any = useParams()
    return (
        <>
            <h1>tasks</h1>
            <div>{params.id}</div>
        </>
    )
}

export default Task;