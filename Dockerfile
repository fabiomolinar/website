FROM python:3.6

RUN mkdir -p /opt/services/website/src
WORKDIR /opt/services/website/src

# install our two dependencies
RUN pip install --upgrade pip && \
  pip install gunicorn django

# copy our project code
COPY . /opt/services/website/src

# expose the port 8000
EXPOSE 8000

# define the default command to run when starting the container
CMD ["gunicorn", "--chdir", "website", "--bind", ":8000", "website.wsgi:application"]