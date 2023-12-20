# Use a base image with the Go runtime
FROM golang:1.19-bullseye as builder

# Set the working directory inside the container
WORKDIR /app

# Copy the Go source file(s) into the container
COPY ./service/*.go ./

# Download any dependencies
RUN go mod init service
RUN go mod tidy

# Build the Go application
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o service .

# Use a smaller base image for the final stage
FROM debian:bullseye-slim

WORKDIR /app

# Install utilities like ping and DNS utils
RUN apt-get update && \
    apt-get install -y iputils-ping dnsutils ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Manage certificates
RUN mkdir -p /usr/local/share/ca-certificates/poc
COPY --from=builder /app/service /app/service
COPY ../certs/CA.crt /usr/local/share/ca-certificates/poc/
RUN update-ca-certificates

RUN mkdir -p /etc/ssl/certs/poc
COPY ./service/service_cert.pem /etc/ssl/certs/poc/
COPY ./service/service_cert.key /etc/ssl/certs/poc/

# Set environment variables 
ENV CERTIFICATE_PATH="/etc/ssl/certs/poc/service_cert.pem"
ENV KEY_PATH="/etc/ssl/certs/poc/service_cert.key"
ENV CA_CERTIFICATE_PATH="/usr/local/share/ca-certificates/poc/CA.crt"

# Run the Go application
CMD ["/app/service"]
