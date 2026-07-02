import builtins

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

def _add_spacing(s: str, with_spacing: bool) -> str:
    return " " + s if with_spacing else s

def _null_spacing(with_spacing: bool) -> str:
    return " ~" if with_spacing else "~"

def _format_str(s: str, with_spacing: bool) -> str:
    out = _add_spacing(" ".join(s) if with_spacing else s, with_spacing)
    index = len(out) + 1
    out += _null_spacing(with_spacing)
    while index % 4 != 0:
        out += _null_spacing(with_spacing)
        index += 1
    return out

def _format_bytes(bs: bytes, with_spacing: bool) -> str:
    out = ""
    for byte in bs:
        out += str(hex(byte))[2:].zfill(2)

    index = len(out) // 2
    while index % 4 != 0:
        out += _null_spacing(with_spacing)
        index += 1
    return out
    
def format_encoded_message(message: bytes, with_spacing = False) -> str:
    decoded = decode(message)
    display = _format_str(decoded.address, with_spacing)

    display += _add_spacing(",", with_spacing)
    for param in decoded.params:
        match type(param):
            case builtins.int:
                display += _add_spacing("i", with_spacing)
            case builtins.float:
                display += _add_spacing("f", with_spacing)
            case builtins.str:
                display += _add_spacing("s", with_spacing)
            case builtins.bytes:
                display += _add_spacing("b", with_spacing)

    index = len(decoded.params) + 2
    display += _null_spacing(with_spacing)
    while index % 4 != 0:
        display += _null_spacing(with_spacing)
        index += 1
    
    for param in decoded.params:
        match type(param):
            case builtins.int:
                display += f"[{param:>6}]"
            case builtins.float:
                display += f"[{str(param)[:6]:>6}]"
            case builtins.str:
                display += _format_str(param, with_spacing)
            case builtins.bytes:
                display += f"[{len(param):>6}]"
                display += _format_bytes(param, with_spacing)

    return display