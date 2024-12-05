# W3-Assignment-Django-Database
## Project Setup
**Clone The Git Repo**
```
git clone https://github.com/Chy-Zaber-Bin-Zahid/W3-Assignment-Django-Database.git
```
**Change Directory To `W3-Assignment-Django-Database`**
```
cd W3-Assignment-Django-Database
```
**Create An Venv**
```
python3 -m venv env
```
**Activate THe Venv**
```
source env/bin/activate
```
**Change Directory To `Inventory_Management`**
```
cd Inventory_Management
```
**Shut Down If Any Previous Containers Are Running In Your Docker**
```
docker-compose down
```
**Build And Run The Docker**
```
docker-compose up --build
```
**Update The Model Using The Below Commands**
```
docker exec -it inventory_management python manage.py makemigrations
```
```
docker exec -it inventory_management python manage.py migrate
```
**Create Super User**
```
docker exec -it inventory_management python manage.py createsuperuser
```

## Property Owners Creation
Go to django admin dashboard and login as admin. Click on `Groups` table and create a `Property Owners` group and gave this four permission showing in the image below and click the save option.

![alt text](image.png)


