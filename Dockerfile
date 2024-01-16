FROM python:3.8

ARG target_env="local"
ARG django_settings="web.config.settings"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TARGET_ENV=base
ENV DJANGO_SETTINGS_MODULE=$django_settings
ENV DJANGO_PORT=8000

# Crear el usuario docker
RUN useradd -m -s /bin/bash -u 1000 -U docker

# Crear directorios
RUN mkdir /backend /var/secrets

WORKDIR /backend

RUN apt-get update \
    && apt-get install -y python3-dev musl-dev

# Copiar requirements
COPY ./requirements/ /backend/requirements/

RUN pip install -r /backend/requirements/${TARGET_ENV}.txt

# Copiar proyecto
COPY . .

# Cambiar la propiedad del directorio a docker
RUN chown -R docker:docker /var/secrets /backend

USER docker
