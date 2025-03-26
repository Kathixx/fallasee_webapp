## Backend

### 1. Delete virtuell environment!
### 2. Check Node & NPM versions
```bash
node -v # v23.7.0
npm -v # 11.2.0

npm install -g npm@11.2.0
```

### 3. Install Vue CLI globally
```bash
npm install -g @vue/cli
```

### 4. Create and activate virtuell environment 
```bash
pyenv local 3.11.3
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements_dev.txt
```

### 5. Install flask
**check if already installed via requirements!**
```bash
pip list
```

**only if not found**
```bash
pip install Flask
pip install flask-cors
```
**The most import script is now the `app.py` script!**

### 6. Run Backend
```bash
python app.py
```
In the Port http://127.0.0.1:5000 you should now see _"Hello from Flask!"_


**Keep the flask Server running!**

---
## Ruff

in a new terminal tab, direct into the backend folder and run the Ruff-watcher
```bash
ruff check --watch
```

**more helpful commands from ruff:**
- `ruff rule F821`: more detailed explanation about the error message
- `ruff check --fix`: fix all errors, whith a fix-flag [*]
- `ruff format`: format the files
___
## MLFlow

in a new terminal tab, direct into the backend folder
to run the mlflow:
```bash
mlflow ui --port 5001
```
_we will use a different port here, because in our initial one (5000), our flask app is already running_
_to not get into trouble, change the port number in the .mlflow.uri file also to 5001_ 

---

## Frontend

**maybe only installing bootstrap is necessary?**

### Create vue app
in your project main directory:

```bash
npm create vue@latest
```

- (type `y`to continue (press enter))
- type `frontend`as project name (press enter)
- click the following by navigating with arrows down and to toggle press space: `Router`, `ESLint`, `Prettier` (press enter)
- `No`for Install OXlint (press enter)

switch to the frontend directory
```bash
cd frontend
npm install
npm run format
npm run dev
```
with `control`+ `c` you can end running vue

### Run vue app

```bash
npm run dev
```

### Installing Bootstrap
```bash
npm install bootstrap bootstrap-vue
````


