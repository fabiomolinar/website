#!/bin/sh

# Installing PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

sudo adduser website
sudo service postgresql start

sudo -u postgres createuser -S -D -R website
sudo -u postgres createdb website
sudo -u postgres psql -f postgresql_first_config.sql