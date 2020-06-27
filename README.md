## Installation

1. Install postgresql (`sudo apt-get install postgresql postgresql-contrib`)
2. Install postgis (`sudo apt-get install postgresql-9.5-postgis-2.1`)
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
12. Make migrations (`python manage.py makemigrations`)
12. Migrate (`python manage.py migrate`)
12. Run all data populating scripts if this is your first time running the code (Below)
13. Run server (`python manage.py runserver`)

## Populating data scripts

Populate data using osm file placed in tmp folder
1. Run OSM parser (`python manage.py runscript osm-handle`)
2. Break road data into 10m chunks (`python manage.py runscript add-intermediate-points`)
3. If you want to limit the road data to a particular region edit the file and run (`python manage.py runscript bounded-10m-points`)
4. To get pothole data from a **predictions_dump.txt** dump edit and run (`python manage.py runscript get_last_7_days_pothole_data`)
5. Now fill in road data in postgis enbaled postgres database (`python manage.py runscript fill-osm-roaddata-in-db`)
6. Fill in reference points for nearest road API (`python manage.py runscript fill-base-roaddata-for-snaptoroad`)
7. Fill the raw pothole data in DB (Last 7 days) (`python manage.py runscript fill-pothole-data-in-db`)
8. Finally snap all these points to nearest road coordinates and fill in the DB (`python manage.py runscript snap-potholes-to-road-segments`)
