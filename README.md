# Hackathon - HackHarvard

---

## Project Structure

This project is divided into three main parts:

| Part         | Stack                                | Folder             |
|--------------|--------------------------------------|--------------------|
|  Frontend  | React NextJs                           | `frontend`     |
|  Backend   | FastAPI                                 | `backend` |


---

## 🚀 Getting Started

### 🔹 Frontend (React App)

To start the frontend development server:

```bash
cd frontend
npm install       # Install dependencies
npm run dev       # Start dev server
```

App runs on localhost:3000

### For backend you need to make virtual env

### Setting UP Virtual Env[Windows]

```bash
py -3.12 -m venv .venv
source .venv/Scripts/activate # Activate env

```

###  Backend(Fast Api)
```bash
cd backend
pip install -r requirement.txt
uvicorn app.main:app --reload


```
API runs at http://127.0.0.1:8000/docs


### Requirement.txt File 
In python requirement.txt file is to list the packages/library installed
It is similiar to package.json in node app.
```bash
pip freeze # See the version of the installed package in terminal
pip freeze > requirement.txt # Creates a file called requirement.txt with installed packages
```