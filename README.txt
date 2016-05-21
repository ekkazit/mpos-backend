1. Create new virtual environment
$  mkdir c:\startup
$  cd c:\startup
$  virtualenv envs

$  cd c:\startup\envs
$  Script\activate

* If Ubuntu we will create by using command: source bin\activate

2. Install Flask Libraries
(envs)$  pip install -r requirements.txt

3. Pull the source code from GitHub
(envs)$  mkdir c:\startup\envs\mpos
(envs)$  git init
(envs)$  git remote add origin https://github.com/ekkazit/mpos-backend.git
(envs)$  git pull origin master

4. Create table migration by using command
(envs)$  python manage.py migrate

5. Prepopulate data
(envs)$  python manage.py seed

6.Run server
(envs)$  python manage.py runserver

7. Open the browser with http://localhost:5000/
username: admin
password: admin
