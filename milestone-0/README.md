# How to load and run the sample app

Run commands from the project root: ...\CS348\milestone-0>

1) Create & activate a virtual environment
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1 #Windows PowerShell
source .venv/bin/activate  #MacOS
```

2) Install dependencies
```bash
pip install -r requirements.txt
```

3) Start a MySQL server through Docker (Desktop Docker app needed)
```bash
docker run --name m0-mysql -d -p 3306:3306 `
  -e MYSQL_ROOT_PASSWORD=root `
  -e MYSQL_DATABASE=app_db `
  -e MYSQL_USER=app_user `
  -e MYSQL_PASSWORD=app_password `
  mysql:8
```

4) Configure environment
```bash
copy .env.example .env
```

5) Initialize schema + example rows
```bash
python -m src.manage init
```

6) Prove DB connectivity 
```bash
python -m src.manage ping
or
python -m src.manage list
```

7) Run the web app
```bash
python -m src.app
```

And open:

http://localhost:3000/health/db
 → {"db":"ok"}

http://localhost:3000/students
 → JSON array of rows

