FROM python:alpine

RUN mkdir /app
RUN pip install -U pip
RUN pip uninstall werkzeug
RUN pip install flask werkzeug==2.3.0 flask-login flask-sqlalchemy markdown