import socket
import ssl
import os
import time
import threading
import signal

def create_tls_context(certfile, keyfile, cafile):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=cafile)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    return context

def tls_connect_and_send_periodically(host, port, context: ssl.SSLContext, message, interval):
    print(f"Connecting to {host} on port {port}...")
    with socket.create_connection((host, port), timeout=2) as raw_socket:
        print(f"Wrapping raw socket in TLS...")
        with context.wrap_socket(raw_socket, server_hostname=host) as secure_socket:
            print(f"TLS handshake complete, let's send some data!")
            while True:
                try:
                    secure_socket.sendall(message.encode())
                    print(f"Sent message to {host}:{port}")
                except Exception as e:
                    print(f"Error sending message: {e}")
                    break
                time.sleep(interval)  # Pause for 'interval' seconds
    print("Exiting for some reason")

def shutdown():
    exit(0)

def main():
    signal.signal(signal.SIGTERM, shutdown)
    CERTIFICATE_PATH = os.environ["CERTIFICATE_PATH"]
    KEY_PATH = os.environ["KEY_PATH"]
    CA_PATH = os.environ["CA_CERTIFICATE_PATH"]
    REMOTE_HOST = os.environ["REMOTE_HOST"]
    if not (CERTIFICATE_PATH and KEY_PATH and CA_PATH and REMOTE_HOST):
        print("ERROR: all required environment variables must be set.")
        print("CERTIFICATE_PATH = Path of the certificate used for TLS")
        print("KEY_PATH = Path of the CERTIFICATE_PATHs corresponding key")
        print("CA_PATH = Path of the CA certificate that signed the certificate at CERTIFICATE_PATH")
        print("REMOTE_HOST = The IP to connect to")
        exit(1)
        
    print(f"CERTIFICATE_PATH={CERTIFICATE_PATH}")
    print(f"KEY_PATH={KEY_PATH}")
    print(f"CA_PATH={CA_PATH}")
    print(f"REMOTE_HOST={REMOTE_HOST}")

    print("Creating TLS context..")
    tls_context = create_tls_context(CERTIFICATE_PATH, KEY_PATH, CA_PATH)

    server_host = REMOTE_HOST
    server_ports = [9000, 9001, 18510]

    print("Connecting on ports: " + ', '.join(str(port) for port in server_ports))
    for port in server_ports:
        threading.Thread(target=tls_connect_and_send_periodically, 
                         args=(server_host, port, tls_context, f"Sending some data on port {port}", 1000)).start()

if __name__ == "__main__":
    main()
    