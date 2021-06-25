---

<p align="center">
  <b>Semester final project from Python on WSIZ</b><br><br>
  <img src="https://www.wsi.edu.pl/wp-content/uploads/2019/05/Niebieski-logotyp_new.png">
</p>

----


# retask

This is a system for schooling that allowas teachers check how many of students got well with given task. Teacher creates a task for group of students and students mark if it is done or not on their accounts. The teacher can see results live on his account.

## Run
Server:
```
cd api
mkdir secret
echo "your secret key" > secret/secret-key
python api.py
```
Secret key can be a random string and it allows to store user session data in cookies.


Client:
```
yarn install
yarn start # or npm instead
```

This small web app uses SQLite database, which creates by itself while the app is starting if the database does not exists yet.
