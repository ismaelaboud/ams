## Swahilipot Hub | AMS

Asset Management system for Swahilipot Hub Foundation
clone the repo

### Backend

navigate to backend folder to run the backend
install requiements
on windows pc activate virtual enviroment using this command

```
backend/env/Scripts/activate
```
linux virtual enviroment activation
```
source bin/activate
```

if no virtual environment, create one using this command

```
python3 venv myvenv
```

***make  sure you activate virtual enviroment before installing requirements***


```
pip3 install -r requirements.txt
```

make migrations and migrate
```
python3 manage.py makemigratins && python3 manage.py migrate
```

then run the server
```
python3 manage.py runserver
```

### Frontend

navigate to frontend folder to run th frontend development server
make sure you have nodeJs and npm installed on your machine

run ```npm install``` to install dependancies 

then run ```npm run dev``` to run the development server


Read full documentation [here](https://www.dropbox.com/scl/fi/zrrf4dw7iekl5qzvvc3e6/Swahilipot-Hub-Asset-Management-System-Documentation.paper?rlkey=8ck6tq0uzoiti3997jzruv9p6&dl=0)