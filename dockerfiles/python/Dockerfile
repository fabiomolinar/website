FROM ubuntu:18.04

LABEL maintainer="Fabio Thomaz Molinar"

# ensuring local python has preference
ENV PATH /usr/local/bin:$PATH

# Updating Ubuntu and adding python
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3 \
  python3-dev \
  python3-venv \
  python3-pip \
  nano