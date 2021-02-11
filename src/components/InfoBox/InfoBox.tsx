import React from 'react';
import './infoBox.css'

type Props = {
    type: string,
    message: string
}

const InfoBox: React.FunctionComponent<Props> = ({ type, message }) => {
    const classes = () => {
        return `box ${type}`
    }

    return (
        <div className={classes()}>{message}</div>
    )
}

export default InfoBox;