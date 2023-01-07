# fftsl

API used in this capstone:
MapQuest Search Ahead API, Edamam API

1. Make a db named fftsl_dev
2. To seed the database replace the following "youremail", "anotheremail", "thirdemail" for your own emails
3. Connect to database: psql fftsl_dev and copy and paste the following:
\COPY cities (name) from 'seed/seed_cities.csv' DELIMITER ',' CSV;
\COPY provinces (name) from 'seed/seed_provinces.csv' DELIMITER ',' CSV;
\COPY cuisines (name) from 'seed/seed_cuisine.csv' DELIMITER ',' CSV;
\COPY recurring_days (day) from 'seed/seed_days.csv' DELIMITER ',' CSV;
\COPY restrictions (name) from 'seed/seed_restrictions.csv' DELIMITER ',' CSV;
\COPY categories (name) from 'seed/seed_categories.csv' DELIMITER ',' CSV;
\COPY school_boards (name) from 'seed/seed_school_boards.csv' DELIMITER ',' CSV;
\COPY categories (name) from 'seed/seed_categories.csv' DELIMITER ',' CSV;

 insert into users(email, password, user_type, active) values('youremail','$2b$12$7UbAACYXos9lIQWkQJDCW.DSCSCMFQoz.3YoRSW8YxY.Molpxd6l6','provider',true);
 insert into users(email, password, user_type, active) values('anotheremail','$2b$12$7UbAACYXos9lIQWkQJDCW.DSCSCMFQoz.3YoRSW8YxY.Molpxd6l6','school',true);
Insert into schools (name, user_id, active) values('Fake School',2, true);
Insert into providers (name, city_id,province_id,user_id, submit_inspection,reviewed,display,active) values('Fake Cater',1,1,1,false,false,false, false);
insert into users(email, password, user_type, active) values('thirdemail','$2b$12$7UbAACYXos9lIQWkQJDCW.DSCSCMFQoz.3YoRSW8YxY.Molpxd6l6','admin',true);
