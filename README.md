# website
My personal website

## Running migrations

It's not a good practice (nor a good idea) to run migrations while creating Docker images. One of the reasons being that the DB service may not even be running.

- Dev environment

`python manage.py migrate --settings=website.settings_test`

- Container environments

To run a migration and update the volume container, the following command can be used:

`sudo docker-compose run --rm website /bin/bash -c "python manage.py migrate"`

## Managing the containers

- Building

```bash
# with docker
sudo docker build -t website .
# with compose
sudo docker-compose build
```

or,  **if behind a proxy**:

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

## Internationalization

1. Go inside the app folder and type `django-admin makemessages -l <language>`
2. Update the *.po files
3. From the same directory, run `django-admin compilemessages`

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

## Development vs Production

At the beginning my intention was to get a running Docker container ready for production. Therefore, the Dockerfile and docker-compose.yml of this project were made to reflect this. They start a project running Django with Gunicorn and Nginx. On top of that, static file collection is done from the project folder and store within a specified folder for Nginx. But that is not good for development as everytime I need to change a file, I need to run `./manage.py collecstatic` command. Therefore, I have created a separated `settings_test.py` configuration file to be ran with `./manage.py runserver --settings=website.settings_test` that spins up a Django server connected to a PostgreSQL DB running on the dev computer, instead of relying on the PostgreSQL container that is used for production. 

Before uploading the project to the cloud, first it's necessary to substitute some files (containing credential information, keys information and others) with their related `**.*.dev` files which are not pushed to the repository. 