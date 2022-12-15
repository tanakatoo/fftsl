# fftsl

API used in this capstone:
MapQuest Search Ahead API, MapQuest Geocoding API, MapQuest Directions API, MapQuest Static Map (not sure about this one) 

1. Make a db named fftsl_dev
2. To seed the database and create 2 users, copy and paste the following commands in psql fftsl_dev **replacing "youremail" and "anotheremail" for your own emails **:
\COPY cities (name) from 'seed/seed_cities.csv' DELIMITER ',' CSV;
\COPY provinces (name) from 'seed/seed_provinces.csv' DELIMITER ',' CSV;
\COPY cuisines (name) from 'seed/seed_cuisine.csv' DELIMITER ',' CSV;
\COPY recurring_days (day) from 'seed/seed_days.csv' DELIMITER ',' CSV;
insert into users(email, password, user_type, active) values('youremail','$2b$12$7UbAACYXos9lIQWkQJDCW.DSCSCMFQoz.3YoRSW8YxY.Molpxd6l6','provider',true);
insert into users(email, password, user_type, active) values('anotheremail','$2b$12$7UbAACYXos9lIQWkQJDCW.DSCSCMFQoz.3YoRSW8YxY.Molpxd6l6','school',true);
Insert into schools (name, user_id, active) values('Fake School',2, true);
