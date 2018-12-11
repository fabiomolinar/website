FROM python:3.6

RUN apt-get update && apt-get install nano

RUN mkdir -p /opt/services/website/src
WORKDIR /opt/services/website/src
COPY Pipfile Pipfile.lock /opt/services/website/src/

# install our two dependencies
RUN pip install --upgrade pip && \
  pip install pipenv && \
  pipenv install --system

# copy our project code
COPY . /opt/services/website/src
ARG CACHEBUST=2
RUN cd website && python manage.py collectstatic --no-input

# expose the port 8000
EXPOSE 8000

# define the default command to run when starting the container
CMD ["gunicorn", "--chdir", "website", "--bind", ":8000", "website.wsgi:application"]