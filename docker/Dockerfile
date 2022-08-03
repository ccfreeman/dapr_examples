FROM python:3.9-slim-buster

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

RUN pip install pipenv
RUN pipenv install

ENTRYPOINT ["python"]
CMD ["demo_actor_service.py"]
