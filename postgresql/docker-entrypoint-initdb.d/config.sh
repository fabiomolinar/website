#!/bin/bash

set -e

psql --username=postgres -c "CREATE ROLE website WITH LOGIN CREATEDB PASSWORD '"${WEBSITE_POSTGRES_WEBSITE_PASSWORD}"';"
psql --username=postgres -c "CREATE DATABASE website OWNER website;"
psql --username=postgres -c "GRANT ALL PRIVILEGES ON DATABASE website TO website;"
psql --username=postgres -c "CREATE ROLE ali WITH LOGIN CREATEDB PASSWORD '"${WEBSITE_POSTGRES_ALI_PASSWORD}"';"
psql --username=postgres -c "CREATE DATABASE ali OWNER ali;"
psql --username=postgres -c "GRANT ALL PRIVILEGES ON DATABASE ali TO ali;"