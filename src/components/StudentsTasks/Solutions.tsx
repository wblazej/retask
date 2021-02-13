import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import InfoBox from './../InfoBox/InfoBox'

const Solutions = () => {
    const params: any = useParams()
    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    const [name, setName] = useState("")
    const [points, setPoints] = useState(Array<number>())
    const [solutions, setSolutions] = useState(Array<object>())
    const [loaded, setLoaded] = useState(false)

    useEffect(() => {
        fetch(`/api/tasks/task-solutions/${params.id}`)
        .then(response => {
            return response.json()
        })
        .then(data => {
            if ('ok' in data) {
                if ('points' in data.ok) {
                    setName(data.ok.name)
                    setPoints(data.ok.points)
                    setSolutions(data.ok.solutions)
                    setLoaded(true)
                }
                else {
                    setName(data.ok.name)
                    showInfoBox('failure', "This task doesn't have any solutions")
                }
            }
            else {
                showInfoBox('failure', data.error)
            }
        })
    }, [])

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

            <h1>{name} solutions</h1>

            { loaded === true &&
                <table className="solutions-table">
                    <tbody>
                        <tr className="header">
                            <td>Username</td>
                            { points.map((point, index) => {
                                return (<td key={index}>{letters[index]}<span className="sol-points">{point}</span></td>)
                            })}
                            <td>Points</td>
                        </tr>
                        
                        { solutions.map((element: any) => {
                            return (
                                <tr>
                                    <td>{element.username}</td>
                                    { element.solutions.map((sol: any) => {
                                        return (
                                            <>
                                                { sol.checked === true && <td><div className="sol checked"></div></td> }
                                                { sol.checked === false && <td><div className="sol unchecked"></div></td> }
                                            </>
                                        )
                                    })}
                                    <td>{element.points}</td>
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
            }
        </>
    )
}

export default Solutions;