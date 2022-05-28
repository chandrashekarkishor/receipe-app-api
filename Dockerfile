FROM python:3.9-alpine3.13
LABEL maintainer="chandrashekarkishor.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

#docker compose will override below line.
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser -D -H django-user
    # adds users if not used the user would have only root.with full permissions  \
    # -D is to do not use password, -H is not to add home directory

# setting environment file
ENV PATH="/py/bin:$PATH"

# uses this user for running.
USER django-user
