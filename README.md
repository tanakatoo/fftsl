# fftsl

API used in this capstone:
MapQuest Search Ahead API, MapQuest Geocoding API, MapQuest Directions API, MapQuest Static Map (not sure about this one) 

#Make a db named fftsl_dev
To create a user, go into psql fftsl_dev
execute the following statement:
insert into users(email, password, user_type, active) values('youremail','$2b$12$7UbAACYXos9lIQWkQJDCW.DSCSCMFQoz.3YoRSW8YxY.Molpxd6l6','provider',true);
It will make you a username using your email and password will be 12345678

#To seed the database, run the following commands in psql fftsl_dev:
\COPY cities (name) from 'seed/seed_cities.csv' DELIMITER ',' CSV;
\COPY provinces (name) from 'seed/seed_provinces.csv' DELIMITER ',' CSV;
\COPY cuisines (name) from 'seed/seed_cuisine.csv' DELIMITER ',' CSV;
\COPY recurring_days (day) from 'seed/seed_days.csv' DELIMITER ',' CSV;!
