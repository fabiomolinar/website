FROM fabiomolinar/python:0.1

SHELL ["/bin/bash", "-c"]

RUN python3 -m venv /home/app/env
RUN source /home/app/env/bin/activate && pip3 install gunicorn