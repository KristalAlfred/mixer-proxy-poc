# mixer-proxy-poc

This is a small PoC to test the idea of an nginx mTLS (and possibly DTLS) termination proxy in front of the mixercores to ensure encrypted traffic between them and any peers.  

The PoC consists of:
- Two networks:
  - Studio -- Represents the local environment between which is shared by the mixer and the proxy
  - Outside -- Represents the untrusted environment where all other services live
- Three containers:
  - Mixer -- A TCP server that accepts incoming TCP connection attempts on certain ports. Currently these are:
    - `9000`
    - `9001`
    - `18510`
  - Service -- An entity that acts as a client towards the mixer. This entity connects to the proxy using mTLS to communicate with the mixer.
  - Proxy -- An nginx instance that terminates mTLS and forwards traffic to the mixer on certain ports.
  
## Build & Run
To build the docker images, it should be enough to just run:

```
docker compose build
``` 

Similarly, to start the PoC just run:

```
docker compose up
```

## Certificates
To properly encrypt the connections between the proxy and service, we need some certificates. In this project we just use a self-signed CA that we trust in both proxy and service. This self-signed CA also issues the certificates these two containers use. Below are the commands to generate the certificates. We'll use `openssl` which is shipped with git and usually found in `C:\Program Files\Git\usr\bin` on Windows.

### Certificate Authority (CA)
First generate the CA private key:
```
openssl ecparam -out CA.key -name prime256v1 -genkey
```

Then generate a Certificate Signing Request (CSR). You'll be prompted for some information when running the command:
```
openssl req -new -sha256 -key CA.key -out CA.csr
```

Sign your own CSR:
```
openssl x509 -req -sha256 -days 365 -in CA.csr -signkey CA.key -out CA.crt
```

(Optional) And convert it to PEM format:

```
openssl x509 -in CA.crt -out CA.pem -outform PEM
```

### Individual certificates
After creating the CA we create a certificate for each container, service and proxy in this case. Each folder (`service` & `proxy`) contains a `san.conf` file. This is used to include Subject Alternative Name parameters in the certificate, which are necessary for at least the Go client to work correctly.

To generate a certificate, first generate a key:
```
openssl genrsa -out proxy_cert.key 2048
```

Then create a CSR. This assumes that you are in the correct folder already, adjust the paths otherwise:
```
openssl req -new -out proxy_cert.csr -newkey rsa:2048 -nodes -keyout .\proxy_cert.key -config san.conf
```

Then sign the CSR with the CA. Again, mind the paths:
```
openssl x509 -req -in proxy_cert.csr -CA ..\certs\CA.crt -CAkey ..\certs\CA.key -CAcreateserial -out proxy_cert.crt -days 365 -sha256 -extfile san.conf -extensions req_ext
```



