from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import pickle  # опасная библиотека для примера десериализации

HOST = "localhost"
PORT = 8080

SECRET_KEY = "hardcoded_secret_123"  # ⚠️ уязвимость: захардкоженный секрет

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/error":
            try:
                1 / 0  # искусственная ошибка
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Internal error: {e}".encode())  # ⚠️ утечка внутренней информации
        elif self.path == "/deserialize":
            data = b"cos\nsystem\n(S'ls'\ntR."
            obj = pickle.loads(data)  # ⚠️ уязвимость: опасная десериализация
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Deserialization complete")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Hello from vulnerable HTTP server")

if __name__ == "__main__":
    print(f"Running server on http://{HOST}:{PORT}")
    HTTPServer((HOST, PORT), MyHandler).serve_forever()
