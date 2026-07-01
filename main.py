from connection import Connection
from protocol import Message

conn = Connection("192.168.9.108", 10023)

message = Message("/test", 5, 1.3, "hello", b"hello")
conn.send_message(message)