# Trckr 

Trckr is mobile-reactive web app designed to help track coaches and athletes manage their workouts. Using the app, coaches can create lifting and practice programs for their athletes. Athletes complete their assigned workouts in the app, and coaches can track the progress of their athletes. 

## Requirements 

Trckr requires [Python](https://www.python.org/downloads/) and [Node.js](https://nodejs.org/en)

## Installation


Open the terminal and clone this repo
```bash 
git clone https://github.com/aretter329/trckr-app.git
```

## Running Trckr Locally

Navigate to the project folder 
```bash 
cd trckr
```

### Set up the Backend 

Navigate to the backend folder 
```bash 
cd backend 
```

Create a virtual environment
```bash 
python -m venv venv 
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows
```

Install Python dependencies 
```bash 
pip install -r requirements.txt 
```

Set up the SQLite database
```bash 
python3 manage.py migrate
```

Start the backend server 
```bash
python3 manage.py runserver
```

### Set up the Frontend

In a new terminal window, navigate to the frontend folder 
```bash 
cd trckr
cd frontend
```

Install npm dependencies 
```bash 
npm install
```

Start the frontend development server
```bash 
npm run dev
```

### Access the App
Ensure that the backend and frontend are running using the steps above. 

Open the following URLs in a web browser: 
- Frontend: http://localhost:5173
- Backend: http://localhost:8000










