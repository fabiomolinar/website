# website
My personal website

## Running migrations

To run a migration and update the volume container, the following command can be used:

`sudo docker-compose run --rm website /bin/bash -c "cd website; ./manage.py migrate"`

## Managing the containers

- Building

`sudo docker-compose build`

- Running

`sudo docker-compose up`

## Technology stack

- Ubuntu
  - Docker
    - PostgreSQL
    - Django
    - Gunicorn

## References

- http://pawamoy.github.io/2018/02/01/docker-compose-django-postgres-nginx.html