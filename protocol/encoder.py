import struct
from typing import Literal

def encode_int(val: int, endian: Literal['little', 'big'] = 'little') -> bytes:
    return val.to_bytes(4, endian, signed=True)

def encode_float(val: float, endian: Literal['little', 'big'] = 'little') -> bytes:
    return struct.pack('>f' if endian == 'big' else '<f', val)


class _Encoder:
    def init(self) -> None:
        self.buffer = bytearray(256)
        self.buffer_index = 0

    def put_byte(self, val: str | int) -> None:
        byte = ord(val) if isinstance(val, str) else val
        self.buffer[self.buffer_index] = byte
        self.buffer_index += 1

    def put_bytes(self, val: bytes) -> None:
        length = len(val)
        self.buffer[self.buffer_index:self.buffer_index + length] = val
        self.buffer_index += length

    def put_int(self, val: int) -> None:
        self.put_bytes(encode_int(val, 'big'))

    def put_float(self, val: float) -> None:
        self.put_bytes(encode_float(val, 'big'))

    def put_str(self, val: str) -> None:
        self.put_bytes(val.encode('utf-8'))
        encoder.align_buffer()
    
    def align_buffer(self, force_padding = True) -> None:
        self.buffer_index = ((self.buffer_index - (0 if force_padding else 1)) & ~0b11) + 4
    
    def get_bytes(self) -> bytes:
        if self.buffer[self.buffer_index - 1] != 0x00:
            self.align_buffer
        return bytes(self.buffer[:self.buffer_index])
    

encoder = _Encoder()

def encode_osc(address: str, *params) -> bytes:
    global encoder

    encoder.init()

    encoder.put_bytes(address.encode())
    encoder.align_buffer()

    encoder.put_byte(",")
    for param in params:
        if isinstance(param, int):
            encoder.put_byte('i')
        elif isinstance(param, float):
            encoder.put_byte('f')
        elif isinstance(param, str): 
            encoder.put_byte('s')
        elif isinstance(param, bytes):
            encoder.put_byte('b')

    encoder.align_buffer()
    
    for param in params:
        if isinstance(param, int):
            encoder.put_int(param)
        elif isinstance(param, float):
            encoder.put_float(param)
        elif isinstance(param, str): 
            encoder.put_str(param)
        elif isinstance(param, bytes):
            encoder.put_int(len(param))
            encoder.put_bytes(param)
            encoder.align_buffer(False)
    
    return encoder.get_bytes()
