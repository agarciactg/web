FROM python:3.8
MAINTAINER AGARCIA <cedesarrolloandres@gmail.com>

ARG target_env="local"
ARG django_settings="web.config.settings"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TARGET_ENV=base
ENV DJANGO_SETTINGS_MODULE=$django_settings
ENV DJANGO_PORT=8000

RUN mkdir /backend /var/secrets
WORKDIR /backend

RUN apt-get update \
    && apt-get install -y python3-dev musl-dev

# Copia requirements
COPY ./requirements/ /backend/requirements/

RUN pip install -r /backend/requirements/${TARGET_ENV}.txt

# Copia proyecto
COPY . .

# Descomentar estas líneas si necesitas ejecutar comandos personalizados
# COPY build.sh /backend/build.sh
# RUN chmod +x /backend/build.sh
# RUN /backend/build.sh

# Comprobar si el grupo docker ya existe antes de intentar crearlo
RUN getent group docker || groupadd -g 1000 docker

# Comprobar si el usuario docker ya existe antes de intentar crearlo
RUN id -u docker &>/dev/null || useradd -g 1000 -u 1000 --no-create-home --quiet docker

# Cambiar la propiedad del directorio a docker
RUN chown -R docker:docker /var/secrets /backend

USER docker
