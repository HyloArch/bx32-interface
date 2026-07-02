from typing import Literal
import struct

def decode_int(val: bytes, endian: Literal['little', 'big'] = 'little') -> int:
    return int.from_bytes(val, endian, signed=True)

def decode_float(val: bytes, endian: Literal['little', 'big'] = 'little') -> float:
    return struct.unpack('>f' if endian == 'big' else '<f', val)[0]


class _Decoder:
    def init(self, message: bytes) -> None:
        self.message = message
        self.message_index = 0

    def align_index(self, force_padding = True) -> None:
        self.message_index = (self.message_index - (0 if force_padding else 1) & ~0b11) + 4

    def get_byte(self) -> int:
        val = self.message[self.message_index]
        self.message_index += 1
        return val

    def get_bytes(self, length = 4) -> bytes:
        val = self.message[self.message_index:self.message_index + length]
        self.message_index += length
        return val
    
    def get_int(self) -> int:
        return decode_int(self.get_bytes(), 'big')

    def get_float(self) -> float:
        return decode_float(self.get_bytes(), 'big')

    def get_str(self) -> str:
        length = self.message.find(0x00, self.message_index) - self.message_index
        return self.get_bytes(length).decode('utf-8')
    
    def read_byte(self, val: str | int) -> bool:
        byte = ord(val) if isinstance(val, str) else val
        return byte == self.get_byte()
    
    def end_of_message(self) -> bool:
        return len(self.message) <= self.message_index


decoder = _Decoder()

def decode_osc(message: bytes) -> tuple[str, list]:
    global decoder

    decoder.init(message)

    address = decoder.get_str()
    decoder.align_index()

    if decoder.end_of_message():
        return (address, [])
    
    assert decoder.read_byte(",")

    types = []
    curr_type = decoder.get_byte()
    while curr_type != 0x00:
        types.append(chr(curr_type))
        curr_type = decoder.get_byte()
    decoder.align_index()

    params = []
    for t in types:
        if t == 'i':
            params.append(decoder.get_int())
        elif 'f':
            params.append(decoder.get_float())
        elif 's':
            params.append(decoder.get_str())
            decoder.align_index()
        elif 'b':
            length = decoder.get_int()
            params.append(decoder.get_bytes(length))
            decoder.align_index(False)

    return (address, params)