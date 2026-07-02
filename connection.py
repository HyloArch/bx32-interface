import socket, struct
from threading import Thread
from typing import Callable
import os

from protocol import Message, format_encoded_message

class Connection(Thread):

    def __init__(self, host: str, port: int) -> None:
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server = (host, port)
        self.socket.bind(("127.0.0.1", 10024))
        self.handlers: list[Callable[[Message], None]] = []
    
    def __delete__(self, instance) -> None:
        self.socket.close()

    def add_handler(self, handler: Callable[[Message], None]):
        self.handlers.append(handler)

    def run(self):
        while True:
            data, addr = self.socket.recvfrom(512)
            if not data:
                return
            print("X ->  ", format_encoded_message(data))

    def send_message(self, message: Message) -> None:
        data = message.encode()
        self.socket.sendto(data, self.server)

        print("  -> X", format_encoded_message(data))
