from connection import Connection
from protocol import Message
from http_server import SimpleHTTPSever, HTTPRequest, HTTPResponse, route
from http import HTTPStatus

# conn = Connection("192.168.9.108", 10023)
# conn.start()

# conn.send_message(Message('/info'))
# conn.send_message(Message('/status'))
# conn.send_message(Message("/xremote"))

# conn.join(10)


def index(req: HTTPRequest) -> HTTPResponse:
    return HTTPResponse(HTTPStatus.OK, file="pages/index.html")

routes = [
    route('/', index)
]

PORT = 8000

server = SimpleHTTPSever(PORT)
server.apply_router(routes)
server.serve()