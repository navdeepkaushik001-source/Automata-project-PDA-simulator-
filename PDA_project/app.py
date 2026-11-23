#!/usr/bin/env python3
"""
Web Server and REST API for Pushdown Automata Simulator
Course: CSET302 - Automata Theory and Computability
Topic: Pushdown Automata Simulator (#12)

Zero-dependency standard library implementation using http.server.
Serves static web files and provides REST endpoints for simulation.
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import sys

# Ensure src is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

from pda_engine import PushdownAutomaton, AcceptanceMode

PORT = 8080

class PDAServerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        if self.path == "/api/presets":
            self.handle_get_presets()
        elif self.path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok", "app": "CSET302 Pushdown Automata Simulator"}')
        else:
            # Fallback to standard static file serving
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/simulate":
            self.handle_post_simulate()
        else:
            self.send_error(404, "Endpoint not found")

    def handle_get_presets(self):
        presets_dir = os.path.join(BASE_DIR, "presets")
        results = {}
        if os.path.exists(presets_dir):
            for fname in os.listdir(presets_dir):
                if fname.endswith(".json"):
                    fpath = os.path.join(presets_dir, fname)
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        key = os.path.splitext(fname)[0]
                        results[key] = data

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(results, indent=2).encode("utf-8"))

    def handle_post_simulate(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)

            pda_config = data.get("pda")
            input_string = data.get("input_string", "")

            pda = PushdownAutomaton.from_dict(pda_config)
            result = pda.simulate(input_string)

            response_data = result.to_dict()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response_data, indent=2).encode("utf-8"))
        except Exception as e:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

def run(port=PORT):
    server_address = ("", port)
    httpd = HTTPServer(server_address, PDAServerHandler)
    print("=" * 65)
    print(" CSET302: Pushdown Automata Simulator Web Server")
    print("=" * 65)
    print(f"Server running at: http://localhost:{port}/")
    print(f"Open http://localhost:{port}/ in your web browser.")
    print("Press Ctrl+C to stop the server.")
    print("=" * 65)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()

if __name__ == "__main__":
    port = PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run(port)
