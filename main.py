import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 8000

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind((UDP_IP, UDP_PORT))
    print(f"Listening for UDP packets on port {UDP_PORT}...")

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Recieved message from {addr}: {data.decode('utf-8')}")