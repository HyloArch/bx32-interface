from .encoder import encode_osc
from .decoder import decode_osc

class Message:

    def __init__(self, address: str, *params) -> None:
        self.address = address
        self.params = params
    
    def __repr__(self) -> str:
        return super().__repr__()
    
    def encode(self) -> bytes:
        return encode_osc(self.address, *self.params)
    

def decode(message: bytes) -> Message:
    decoded = decode_osc(message)
    return Message(decoded[0], *decoded[1])

def _format_str(s: str):
    out = " " + " ".join(s)
    index = len(out)
    out += " ~"
    while index % 4 != 0:
        out += " ~"
        index += 1
    return out

def _format_bytes(bs: bytes):
    out = ""
    for byte in bs:
        out += str(hex(byte))[2:].zfill(2)

    index = len(out) // 2
    while index % 4 != 0:
        out += " ~"
        index += 1
    return out
    
def print_encoded_message(message: bytes) -> None:
    decoded = decode(message)
    display = _format_str(decoded.address)

    display += " ,"
    for param in decoded.params:
        match param:
            case int():
                display += " i"
            case float():
                display += " f"
            case str():
                display += " s"
            case bytes():
                display += " b"

    index = len(decoded.params) + 2
    display += " ~"
    while index % 4 != 0:
        display += " ~"
        index += 1
    
    for param in decoded.params:
        match param:
            case int():
                display += f"[{param:>6}]"
            case float():
                display += f"[{str(param)[:6]:>6}]"
            case str():
                display += _format_str(param)
            case bytes():
                display += f"[{len(param):>6}]"
                display += _format_bytes(param)

    print(len(message), display)
    print(len(message), message.hex())