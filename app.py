import os
from http.server import BaseHTTPRequestHandler, HTTPServer


MENSAJE = os.getenv(
    "MENSAJE",
    "Hola desde Docker — versión 2.0 (actualizada)",
)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(MENSAJE.encode("utf-8"))

    def log_message(self, format, *args):
        print(f"[Solicitud] {args[0]} {args[1]}")


if __name__ == "__main__":
    print("Servidor iniciado en puerto 8080")
    print(f"Mensaje: {MENSAJE}")
    HTTPServer(("", 8080), Handler).serve_forever()
