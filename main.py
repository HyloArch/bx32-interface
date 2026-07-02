from connection import Connection
from protocol import Message

conn = Connection("192.168.9.108", 10023)
conn.start()

conn.send_message(Message('/info'))
conn.send_message(Message('info'))
conn.send_message(Message("/xremote"))

conn.join(10)