FROM nginx:1.25.3

# Manage certificates
RUN mkdir /usr/local/share/ca-certificates/poc
COPY ../certs/CA.crt /usr/local/share/ca-certificates/poc/
RUN update-ca-certificates

RUN mkdir -p /etc/ssl/certs/poc
COPY ./proxy/proxy_cert.crt /etc/ssl/certs/poc/
COPY ./proxy/proxy_cert.key /etc/ssl/certs/poc/

# Set environment variables 
# TODO(alfred): Maybe set these in the compose file instead?
ENV CERTIFICATE_PATH="/etc/ssl/certs/poc/proxy_cert.crt"
ENV KEY_PATH="/etc/ssl/certs/poc/proxy_cert.key"
ENV CA_CERTIFICATE_PATH="/usr/local/share/ca-certificates/poc/CA.crt"

# Copy the python script and run it
COPY ./proxy/nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]