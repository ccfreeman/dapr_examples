FROM python:3.10-slim-buster

WORKDIR /app
COPY . . 

RUN apt-get update --fix-missing \
    && apt-get install -y \
        curl \
        libglib2.0-0\
        libxext6 \
        libsm6 \
        libxrender1 \
        build-essential \ 
        python-lxml \
        unixodbc-dev \
        dos2unix \
    && apt-get clean

RUN curl 'http://pki.coyote.com/trust/zscaler.cer' -o '/usr/local/share/ca-certificates/zscaler.crt'
RUN chmod 644 /usr/local/share/ca-certificates/zscaler.crt && update-ca-certificates
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# RUN wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
RUN curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | /bin/bash

# Install daprd
ARG DAPR_BUILD_DIR
COPY $DAPR_BUILD_DIR /opt/dapr
ENV PATH="/opt/dapr/:${PATH}"
# RUN dapr init 
RUN dapr init --slim

RUN pip install pipenv
RUN pipenv install

# ENTRYPOINT ["python"]
# CMD ["demo_actor_service.py"]

# ENTRYPOINT ["dapr"]
# CMD ["run", "--app-id", "invoke-receiver", "--app-protocol", "grpc", "--app-port", "50051", "--config" "src/services/config.yaml", "--", "pipenv", "run", "python", "-m", "src.services.server"]

# ENTRYPOINT ["dapr", "run", "--app-id", "invoke-receiver", "--app-protocol", "grpc", "--app-port", "50051", "--config" "src/services/config.yaml", "--", "pipenv", "run", "python", "-m", "src.services.server"]

RUN dos2unix /app/docker/docker-entrypoint.sh
RUN chmod +x /app/docker/docker-entrypoint.sh

WORKDIR /app
USER root
EXPOSE 50051
