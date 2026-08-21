from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

metrics_data = ""

class MetricsHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        global metrics_data
        length = int(self.headers.get("Content-Length", 0))
        metrics_data = self.rfile.read(length).decode("utf-8")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def do_GET(self):
        if self.path != "/metrics":
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; version=0.0.4")
        self.end_headers()
        self.wfile.write(metrics_data.encode("utf-8"))

    def log_message(self, format, *args):
        return

httpd = HTTPServer(("0.0.0.0", 9443), MetricsHandler)
print("Receiver listening on http://0.0.0.0:9443")
httpd.serve_forever()
