export const getDateFromTimestamp = (timestamp: number) => {
    let datetime = new Date(timestamp)
    let day = datetime.getDate()
    let month = datetime.getMonth()
    let year = datetime.getFullYear()
    let hour = datetime.getHours()
    let minute = datetime.getMinutes()

    let day_string = day.toString()
    if (day < 10) day_string = `0${day}`
    let month_string = month.toString()
    if (month < 10) month_string = `0${month}`
    let hour_string = hour.toString()
    if (hour < 10) hour_string = `0${hour}`
    let minute_string = minute.toString()
    if (minute < 10) minute_string = `0${minute}`

    return `${day_string}.${month_string}.${year} ${hour_string}:${minute_string}`
}