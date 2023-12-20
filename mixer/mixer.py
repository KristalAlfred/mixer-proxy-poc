import socket
import threading
import signal

def start_tcp_listener(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as recv:
        recv.bind((ip, port))
        recv.listen()
        
        while True:
            remote, address = recv.accept()

            with remote:
                print(f"Incoming connection from {address}")
                while True:
                    data = remote.recv(64)
                    if not data:
                        break
                    print(f"Received data block from {address}. Sending it back.")
                    remote.sendall(data)

def start_udp_listener(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as recv:
        recv.bind((ip, port))

        while True:
            _, address = recv.recvfrom(1024)
            print(f"Received UDP data block from {address}. Discarding it.")


def start_listeners(ip, tcp_ports, udp_ports):
    print("Starting listeners")
    print("\tTCP ports: " + ", ".join(str(port) for port in tcp_ports))
    print("\tUDP ports: " + ", ".join(str(port) for port in udp_ports))
    for port in tcp_ports:
        threading.Thread(target=start_tcp_listener, args=(ip, port)).start()
    for port in udp_ports:
        threading.Thread(target=start_udp_listener, args=(ip, port)).start()

def shutdown():
    exit(0)

signal.signal(signal.SIGTERM, shutdown)
tcp_ports = [9000, 9001, 18510]
udp_ports = [18511]
start_listeners("0.0.0.0", tcp_ports, udp_ports)
