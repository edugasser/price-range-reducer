# Dockerfile
FROM python:3.8

# Create app directory
RUN mkdir -p /app
WORKDIR /app

# Install pipenv
RUN pip3 install pipenv

# Install app dependencies
COPY req.txt /app/

RUN pip3 install -r req.txt

COPY . /app

# TODO: to change
CMD [ "python", "app.py" ]
