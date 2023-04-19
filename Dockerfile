FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

# install psycopg2 dependencies
# RUN apt update \
#     && apt install postgresql-dev gcc python3-dev musl-dev

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./core /app

RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["sh", "/app/entrypoint.sh"]