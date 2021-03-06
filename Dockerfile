FROM python:3.9-alpine

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBUG 0


# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

RUN apk add make automake gcc g++ subversion python3-dev

# Install Python requirements.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code.
COPY . .

# run gunicorn
#CMD gunicorn lib_project.wsgi:application --bind 0.0.0.0:$PORT
#CMD gunicorn lib_project.wsgi:application