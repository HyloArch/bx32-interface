import socket, struct
from protocol import encode_osc, decode_osc, Message, print_encoded_message, decode

class Connection:

    def __init__(self, host: str, port: int) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server = (host, port)
    
    def __delete__(self, instance) -> None:
        self.socket.close()

    def send_message(self, message: Message) -> None:
        data = message.encode()
        # self.socket.sendto(message, self.server)

        # display = " ".join(map(lambda b: '~' if b == 0 else chr(b) if chr(b).isprintable() else str(b), message))
        # print(len(message), display)
        # print(len(message), message.hex())

        print_encoded_message(data)

        test = decode_osc(data)
        print(test)


