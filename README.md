## Installation

1. Install postgresql (`sudo apt-get install postgresql postgresql-contrib`)
2. Install postgis (`sudo apt-get install postgresql-9.5-postgis-2.1`)
<!-- ```
sudo pg_dropcluster 9.5 main --stop
sudo pg_upgradecluster 9.3 main
sudo pg_dropcluster 9.3 main
``` -->
4. Create user 'road_data_user' with password 'pass@123' in psql, create database 'road_data_db' with postgis extension in it, grant superuser permission to 'road_data_user'
commands to be executed in order
   1. `sudo -i -u postgres`
   2. `psql`
   3. `create user road_data_user with password 'pass@123'`
   4. `create database road_data_db;`
   5. `\c road_data_db;`
   6. `create extension postgis;`
   7. `grant all privileges on database road_data_db to road_data_user;`
   8. `alter user road_data_user with superuser;`
<!-- 4. Install libpq-dev and python dev (`sudo apt-get install libpq-dev python-dev`) -->
5. Install pip3
6. Install virtualenv (`pip install virtualenv`)
7. Create the virtual environment and activate it
8. Install requirements using pip (`pip install -r requirements.txt`)
12. Create super user (`python manage.py createsuperuser`)
13. Run server (`python manage.py runserver`)