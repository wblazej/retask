# retask
This is a system for schooling that allowas teachers check how many of students got well with given task. Teacher creates a task for group of students and students mark if it is done or not on their accounts. The teacher can see results live on his account.

## Run
Server:
```
cd api
python api.py
```
Client:
```
yarn install
yarn start # or npm instead
```

This small web app uses SQLite database, which creates by itself while the app is starting if the database does not exists yet.
