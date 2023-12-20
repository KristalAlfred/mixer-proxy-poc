import socket
import threading

def start_tcp_listener(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as recv:
        recv.bind((ip, port))
        recv.listen()
        
        while True:
            remote, address = recv.accept()

            with remote:
                print(f"Incoming connection from {address}")
                while True:
                    data = remote.recv(1024)
                    if not data:
                        break
                    print(f"Received data block from {address}. Discarding it.")

def start_udp_listener(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as recv:
        recv.bind((ip, port))

        while True:
            _, address = recv.recvfrom(1024)
            print(f"Received UDP data block from {address}. Discarding it.")


def start_listeners(ip, tcp_ports, udp_ports):
    for port in tcp_ports:
        threading.Thread(target=start_tcp_listener, args=(ip, port)).start()
    for port in udp_ports:
        threading.Thread(target=start_udp_listener, args=(ip, port)).start()

tcp_ports = [9000, 9001, 18510]
udp_ports = [18511]
start_listeners("0.0.0.0", tcp_ports, udp_ports)