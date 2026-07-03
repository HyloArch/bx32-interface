from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
import shutil
from typing import Callable

class HTTPRequest:
    def __init__(self) -> None:
        pass

class HTTPResponse:
    def __init__(self, code: HTTPStatus, * , file = "") -> None:
        self.code = code
        self.file = file

def route(path: str, handler: Callable[[HTTPRequest], HTTPResponse]) -> tuple[str, Callable[[HTTPRequest], HTTPResponse]]:
    return (path, handler)


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if not isinstance(self.server, HTTPServerRunner):
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR)
            self.end_headers()
            return

        print(self.path)
        handler = self.server.router.get(self.path)
        if not handler:
            self.send_error(HTTPStatus.NOT_FOUND)
            self.end_headers()
            return
        res = handler(HTTPRequest())

        self.send_response(res.code)
        self.end_headers()

        if res.file:
            with open("pages/index.html", "rb") as f:
                shutil.copyfileobj(f, self.wfile)

class HTTPServerRunner(HTTPServer):
    def __init__(self, port: int):
        self.router: dict[str, Callable[[HTTPRequest], HTTPResponse]] = {}
        super().__init__(("", port), HTTPRequestHandler)

    def apply_router(self, router: dict[str, Callable[[HTTPRequest], HTTPResponse]]):
        self.router = router


class SimpleHTTPSever:
    def __init__(self, port: int):
        self.port = port
        self.runner = HTTPServerRunner(port)

    def serve(self):
        try:
            print(f"Started HTTP server on http://localhost:{self.port}")
            self.runner.serve_forever()
        except:
            print("Server shutting down!")

    def apply_router(self, router: list[tuple[str, Callable[[HTTPRequest], HTTPResponse]]]):
        self.runner.apply_router({path : handler for (path, handler) in router})