# website
My personal website

## Running migrations

- Dev environment

`python manage.py migrate --settings=website.settings_test`

- Container environments

To run a migration and update the volume container, the following command can be used:

`sudo docker-compose run --rm website /bin/bash -c "cd website; ./manage.py migrate"`

## Managing the containers

- Building

```bash
# with docker
sudo docker build -t website .
# with compose
sudo docker-compose build
```

or,  if behind a proxy:

```bash
# with docker
sudo docker build -t website --build-arg PROXY="http://user:password@proxyserver:port" .
# with compose
sudo docker-compose build --build-arg PROXY="http://user:password@proxyserver:port" .
```

- Running

`sudo docker-compose up`

- Debugging

`sudo docker exec -it <container> /bin/bash`

## Runing tests

- Dev environment

These tests are run on my computer, and not on the containers. Therefore, to start this server, it's necessary to use:

`python manage.py runserver --settings=website.settings_test`

Then, to run the tests:

`python manage.py test base.tests --settings=website.settings_test`

## Style

- Timeline

Reference: https://bootsnipp.com/snippets/featured/timeline-responsive

## Technology stack

- Ubuntu
  - Docker
    - PostgreSQL
    - Django
    - Gunicorn

## References

- http://pawamoy.github.io/2018/02/01/docker-compose-django-postgres-nginx.html