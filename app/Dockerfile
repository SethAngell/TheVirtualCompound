FROM python:3.10.9-slim-buster

# Set working directory for all following in container commands
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DB_ENGINE django.db.backends.postgresql_psycopg2
ENV DB_NAME postgres
ENV DB_USER postgres
ENV DB_PASS bad_password
ENV DB_HOST "db"
ENV DB_PORT 5432

RUN apt-get update \
  && apt-get -y install gcc postgresql libpq-dev vim wkhtmltopdf \
  && apt-get clean


# Handle all necessary dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Install App
COPY . .

ENTRYPOINT ( python manage.py collectstatic --noinput && python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000)

#ENTRYPOINT (python manage.py runserver 0.0.0.0:8000)