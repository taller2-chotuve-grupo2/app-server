FROM python:3.8.1-slim

# install netcat
RUN apt-get update \
  && apt-get -y install netcat \
  && apt-get clean

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements
COPY ./app/requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt


# add app
COPY ./app /usr/src/app
COPY ./services /usr/src/services
COPY ./entrypoint.sh /usr/src/entrypoint.sh
COPY ./run.py /usr/src/run.py

WORKDIR /usr/src
RUN cd '/usr/src'

# run server
CMD ["./entrypoint.sh"]
