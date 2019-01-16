FROM python:3.6
# proxy settings
ARG PROXY
ENV http_proxy=${PROXY}
ENV PIP_PROXY=${PROXY}

RUN apt-get update && apt-get install -y \ 
  apt-utils \
  nano \
  gettext 

RUN mkdir -p /opt/services/website/src
WORKDIR /opt/services/website/src
COPY Pipfile Pipfile.lock /opt/services/website/src/

# install our dependencies
RUN pip install --upgrade pip && \
  pip install pipenv && \
  pipenv install --system

# copy our project code
COPY . /opt/services/website/src
ARG CACHEBUST=1
# collect static
RUN cd website && python manage.py collectstatic --no-input
# create translation
RUN cd website && python manage.py compilemessages

# expose the port 8000
EXPOSE 8000
WORKDIR /opt/services/website/src/website

# define the default command to run when starting the container
CMD ["gunicorn", "--bind", ":8000", "website.wsgi:application"]