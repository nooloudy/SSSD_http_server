from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import traceback

HOST = "localhost"
PORT = 8080

# SECRET_KEY теперь берётся из переменной окружения
SECRET_KEY = os.getenv("SECRET_KEY", "default-fallback-secret")

class MyHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Логируем в консоль (сервер) без отправки лишней информации клиенту.
        print("%s - - [%s] %s" % (self.client_address[0], self.log_date_time_string(), format%args))

    def do_GET(self):
        try:
            if self.path == "/error":
                # Симуляция ошибки, но клиенту возвращаем общее сообщение
                raise ValueError("simulated error")
            elif self.path == "/deserialize":
                # Десериализация отключена — безопасный отказ
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"Deserialization disabled for security reasons.")
            else:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Hello from secure HTTP server")
        except Exception:
            # Общий ответ клиенту без внутренних деталей
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal server error. Please contact admin.")
            # Логируем стек трейc в консоль (не отправляем клиенту)
            traceback.print_exc()

if __name__ == "__main__":
    print(f"Running server on http://{HOST}:{PORT}")
    HTTPServer((HOST, PORT), MyHandler).serve_forever()
