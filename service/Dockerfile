FROM python:3.12.1-bookworm
WORKDIR /app

RUN apt-get update && apt-get install -y iputils-ping dnsutils

# Manage certificates
RUN mkdir /usr/local/share/ca-certificates/poc
COPY ../certs/CA.crt /usr/local/share/ca-certificates/poc/
RUN update-ca-certificates

RUN mkdir -p /etc/ssl/certs/poc
COPY ./service/service_cert.pem /etc/ssl/certs/poc/
COPY ./service/service_cert.key /etc/ssl/certs/poc/

# Set environment variables 
# TODO(alfred): Maybe set these in the compose file instead?
ENV CERTIFICATE_PATH="/etc/ssl/certs/poc/service_cert.pem"
ENV KEY_PATH="/etc/ssl/certs/poc/service_cert.key"
ENV CA_CERTIFICATE_PATH="/usr/local/share/ca-certificates/poc/CA.crt"

# Copy the python script and run it
COPY ./service/service.py service.py

CMD ["python", "./service.py"]