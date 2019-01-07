# website
My personal website

This is just a bunch of notes I take in order not to forget things in the future. :)

## Environments

- Fast test environment (dev machine)
- Container test environment (docker runing on dev machine)
- Staging enviroment (temporary droplet on digitalocean)
- Production enviroment (droplet on digitalocean)

## Running migrations

It's not a good practice (nor a good idea) to run migrations while creating Docker images. One of the reasons being that the DB service may not even be running.

- Dev environment

`python manage.py migrate --settings=website.settings_test`

- Container environments

To run a migration and update the volume container, the following command can be used:

`sudo docker-compose run --rm website /bin/bash -c "python manage.py migrate"`

- Migrations for a specific app

While migrating tables only for a app on a different database, use the following command:

`python manage.py migrate <app name> --database=<database name>`

Additionally, if we don't want the migrations for a certain model to be ran on a certain DB, we need to **update the `allow_migrate()` method from its DB router (`routers.py`) correctly**.

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

## DB

### Installing postgresql on Linux

```bash
$ sudo apt-get update
#The packages below are necessary only to get Django working with postgresql
$ sudo apt-get install libpq-dev python-dev
#Install postgresql
$ sudo apt-get install postgresql postgresql-contrib
#Changing to the postgres user
$ sudo -i -u postgres
#Accessing the postgresql prompt
$ psql
#To exit the prompt, type \q
postgres=# \q
#Instead of changing users, we could use the sudo command:
$ sudo -u postgres psql
```

By default, Postgres uses a concept called "roles" to handle in authentication and authorization. These are, in some ways, similar to regular Unix-style accounts, but Postgres does not distinguish between users and groups and instead prefers the more flexible term "role".

Upon installation Postgres is set up to use **ident authentication**, which means that it associates Postgres roles with a matching Unix/Linux system account. If a role exists within Postgres, a Unix/Linux username with the same name will be able to sign in as that role.

The installation procedure created a user account called `postgres` that is associated with the default Postgres role. In order to use Postgres, we can log into that account.

```bash
#Creating a postgresql user with the same name of the DB we want in order to use the ident authentication
#commands as postgres user
postgres@server:~$ createuser --interactive
#The same command above could be done using sudo
$ sudo -u postgres createuser --interactive
#The command will prompt for information regarding the new postgresql user. *Fill it*.
#Now, create the DB with the same name as the newly created postgresql user.
postgres@server:~$ createdb mysite
#Next step, let's create the system USER with the same name as the DB and the ROLE
$ sudo adduser mysite
$ sudo -i -u mysite
$ psql
#You will be logged in automatically assuming that all of the components have been properly configured.
```

If we have created different postgresql users and we want to grant them access to our DB, we can use the following command inside the postgresql prompt

```bash
$ psql
postgres=# GRANT ALL PRIVILEGES ON DATABASE <DB name> TO <postgresql user name>;
```

And if we need to change a user's password:

```bash
postgres=# ALTER USER <user name> WITH PASSWORD '<new password>';
```

### Configuring Django to run with postgresql

```python
pip install psycopg2
```

Then, edit the settings.py file to:

```python
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'mysite',
            'USER': 'mysite',
            'PASSWORD': 'mysite',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
```

The, from the project directory, run:

```python
python manage.py syncdb
```

If problems with the password are detected, we can change the postgresql user password with the following commands:

```bash
$ sudo -u mysite psql mysite
mysite=> ALTER USER mysite WITH PASSWORD '<new password here>';
mysite=> \q
```

## Celery

Broker: RabbitMQ
Results backend: django-db
Scheduler: Celery beat

### Starting the server

`celery -A <project name> worker --loglevel=info`, e.g.:

`celery -A website worker --loglevel=info` (ran from the same folder that contains `manage.py`).

If we want to start it on the background, sufices to use `--detach`.

### Starting the beat service

`celery -A <project name> beat`, or using the `worker` command:

`celery -A <project name> worker -B`. This option is convenient if **never running more than one worker node**, but it’s not recommended for production use.

To start it on the background, use `--detach`.

### Changing timezone

If changing timezone settings, we need to update the scheduled tasks. To do that:

```bash
python manage.py shell
>>> from django_celery_beat.models import PeriodicTask
>>> PeriodicTask.objects.update(last_run_at=None)
```

## Digital Ocean

### SSH

(Reference)[https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-1804]

### Initial Server Setup

(Reference)[https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04]

Always good to create a new user other than root to do daily tasks on the server. E.g.: fabio.

### Nginx, Gunicorn and Django Settings

(Reference)[https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04]

### SSL Certification

(Reference)[https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04]
(Nginx configuration and certbot workflow)[https://miki725.com/docker/crypto/2017/01/29/docker+nginx+letsencrypt.html]
Amazing tuto/explanation: (Nginx configuration and certbot workflow 2)[https://www.humankode.com/ssl/how-to-set-up-free-ssl-certificates-from-lets-encrypt-using-docker-and-nginx]

To get the certificate for the first time, we need to:

- Update nginx config to set the ACME challenge path
- Run a certbot container to run the challenge
  - E.g.: `sudo docker run -it --rm --name certbot -v "website_certs:/etc/letsencrypt" -v "website_certs_data:/var/www/certbot" certbot/certbot:v0.30.0 certonly --webroot --webroot-path /var/www/certbot -d fabiomolinar.com -d www.fabiomolinar.com`

### DNS

(Reference)[https://www.digitalocean.com/docs/networking/dns/]