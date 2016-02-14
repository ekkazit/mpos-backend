1. สร้าง virtual environment
$  mkdir c:\startup
$  cd c:\startup
$  virtualenv envs

$  cd c:\startup\envs
$  Script\activate

* ถ้าเป็น Ubuntu จะใช้ source bin\activate

2. ติดตั้ง Flask Libraries
(envs)$  pip install -r requirements.txt

3. ดึง source code ออกมาจาก github
(envs)$  mkdir c:\startup\envs\mpos
(envs)$  git init
(envs)$  git remote add origin https://github.com/ekkazit/mpos-backend.git
(envs)$  git pull origin master

4. สร้างเทเบิ้ลด้วยคำสั่ง
(envs)$  python manage.py migrate

5. สร้างข้อมูลจำลองด้วยคำสั่ง
(envs)$  python manage.py seed

6. จากนั้นสั่งให้โปรแกรมเว็บทำงาน
(envs)$  python manage.py runserver

7. เข้าใช้งานด้วยยูอาร์แอล http://localhost:5000/
username: admin
password: admin
