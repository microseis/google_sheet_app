FROM python:3.9-alpine

MAINTAINER Alexey Stepanov <stepanov.geo@ya.ru>

ENV PATH="/scripts:${PATH}"

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
RUN pip install psycopg2-binary
COPY kanalservis/requirements.txt requirements.txt
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers libffi-dev libpq-dev python3-dev libpq gfortran musl-dev
RUN pip3 install -r requirements.txt

RUN apk del .tmp
RUN mkdir "/app"
COPY kanalservis /app
WORKDIR /app
COPY ./scripts /scripts

RUN chmod +x /scripts*

RUN mkdir -p "/vol/web/media"
RUN mkdir -p "/vol/web/static"
RUN mkdir -p "/vol/web/db"

RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
USER user

CMD ["entrypoint.sh"]

