# HackHarvard - Textify

**Textify** is a project dedicated to enhancing the understanding of human culture and history through digital humanities. Our goal is to rethink how ancient literature from centuries ago can be processed, analyzed, and read in the modern era. Currently, we support the digitalization of manuscripts in Old English, Latin, Greek, and Sanskrit.

Using Google Cloud Vision, we perform OCR on these manuscripts, and with advanced computer vision techniques, we process and structure the documents. Leveraging the Gemini Flash 1.5 model, we have achieved text accuracy rates of approximately 90–95% for certain manuscripts.

These manuscripts are further analyzed using the Classical Language Toolkit (CLTK) for lexical categorization. Additionally, Google Cloud Text-to-Speech enables live English audio renderings, translating the original manuscript’s language into spoken English.

The idea for this project arose from recognizing the challenges faced by scholars and archaeologists, for whom transcription of ancient texts can take years. Textify aims to streamline this process, making the knowledge embedded in historical manuscripts more accessible and usable.

---

## Project Structure

This project is divided into three main parts:

| Part         | Stack                                | Folder             |
|--------------|--------------------------------------|--------------------|
|  Frontend  | React NextJs                           | `frontend`     |
|  Backend   | FastAPI                                 | `backend` |


---
### System Architecture
[![Screenshot-2025-10-04-at-8-30-49-PM.png](https://i.postimg.cc/43y4bkLF/Screenshot-2025-10-04-at-8-30-49-PM.png)](https://postimg.cc/Mck8q48y)

---

## Getting Started

###  Frontend (React App)

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
.venv/Scripts/Activate # Activate env

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
pip freeze # See the version of the installed package in the terminal
pip freeze > requirement.txt # Creates a file called requirement.txt with installed packages
```
### Gemini is now replaced by ollama models for text cleanup
**Requirements for Ollama**
- Download Ollama
[Download for Windows](https://ollama.com/download/windows)
[Download for Mac](https://ollama.com/download/mac)

- Run the following command to install the models
```bash
ollama pull llama3.1
ollama pull qwen2.5
```

