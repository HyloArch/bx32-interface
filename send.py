import socket

TARGET_IP = "192.168.8.194"
TARGET_PORT = 8000

MESSAGE = b"Hello, world!"

print(f"Sending packets to {TARGET_IP}:{TARGET_PORT}")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    message = input()
    while message != "exit":
        sock.sendto(message.encode(), (TARGET_IP, TARGET_PORT))
        message = input()