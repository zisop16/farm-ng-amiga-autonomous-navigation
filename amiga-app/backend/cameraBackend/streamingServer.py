import depthai as dai
from multiprocessing import Queue

import time
from http.server import BaseHTTPRequestHandler, HTTPServer

def startStreamingServer(server_stream_queue: Queue, STREAM_FPS, camera_ip, stream_port):
    delay = 1 / STREAM_FPS

    class HTTPHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/rgb":
                try:
                    self.send_response(200)
                    self.send_header(
                        "Content-type",
                        "multipart/x-mixed-replace; boundary=--jpgboundary",
                    )
                    self.end_headers()
                    while True:
                        frame_data = server_stream_queue.get()

                        self.wfile.write("--jpgboundary".encode())
                        self.wfile.write(bytes([13, 10]))
                        self.send_header("Content-type", "image/jpeg")
                        # self.send_header("Content-length", str(len(frame.getData())))
                        self.send_header("Content-length", str(len(frame_data)))
                        self.end_headers()
                        # self.wfile.write(frame.getData())
                        self.wfile.write(frame_data)
                        self.end_headers()
                        time.sleep(delay)

                except Exception as ex:
                    print("Client disconnected")

    class ThreadingSimpleServer(HTTPServer):
        pass

    with ThreadingSimpleServer(("", stream_port), HTTPHandler) as httpd:
        print(
            f"Serving RGB MJPEG stream at {camera_ip}:{stream_port}/rgb"
        )
        httpd.serve_forever(poll_interval=1)
