FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# install psycopg2 dependencies
# RUN sh -c "apt-get -y update && apt-get install postgresql-dev gcc python3-dev musl-dev"

# set up the psycopg2
# First RUN Statement: to install postgresql dependency
RUN apt-get update && apt-get install -y libpq-dev  \
    gcc \
    postgresql-client
# Second RUN Statement: Install postgresql driver for django
RUN pip install psycopg2==2.8.3
# Third RUN Statement: Remove the gcc compier after install the driver
RUN apt-get autoremove -y gcc

COPY ./core /app

# RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["sh", "/app/entrypoint.sh"]