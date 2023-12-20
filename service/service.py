import socket
import ssl
import os
import threading

def start_listener(ip, port, cert_path, key_path, ca_path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as recv:
        recv.bind((ip, port))
        recv.listen()

        tls_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        tls_context.verify_mode = ssl.CERT_REQUIRED
        tls_context.load_cert_chain(certfile=cert_path, keyfile=key_path)
        tls_context.load_verify_locations(cafile=ca_path)
        
        while True:
            raw_socket, address = recv.accept()
            remote = tls_context.wrap_socket(raw_socket, server_side=True)

            with remote:
                print(f"Incoming connection from {address}")
                while True:
                    data = remote.recv(1024)
                    if not data:
                        break
                    print(f"Received data block from {address}. Discarding it.")

def start_tcp_listeners(ip, ports, cert_path, key_path, ca_path):
    for port in ports:
        thread = threading.Thread(target=start_listener, args=(ip, port, cert_path, key_path, ca_path))
        thread.start()


# Make sure certificate paths have been passed
CERTIFICATE_PATH = os.environ["CERTIFICATE_PATH"]
KEY_PATH = os.environ["KEY_PATH"]
CA_PATH = os.environ["CA_PATH"]

if not (CERTIFICATE_PATH and KEY_PATH and CA_PATH):
    print("All environment variables must be set.")
    print("CERTIFICATE_PATH = Path for the certificate file for this container")
    print("KEY_PATH = Path for the certificates corresponding key file")
    print("CA_PATH = Path for the CA certificate that signed the certificate at CERTIFICATE_PATH")
    exit(1)
    
tcp_ports = [9000, 9001, 18510]
start_tcp_listeners("0.0.0.0", tcp_ports, CERTIFICATE_PATH, KEY_PATH, CA_PATH)

## DTLS doesn't seem to be supported in the SSL package.
# udp_ports = [18511]