from multiprocessing import Queue
import signal
import time
from http.server import BaseHTTPRequestHandler, HTTPServer


def startStreamingServer(server_stream_queue: Queue, STREAM_FPS, stream_port: int):
    print(f"Starting RGB MJPEG stream at 127.0.0.1:{stream_port}...")
    delay = 1 / STREAM_FPS

    class MJPEGHandler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def setup(self):
            super().setup()
            # self.request.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            # self.wfile = self.request.makefile('wb', buffering=0)

        def do_GET(self):
            if self.path != "/rgb":
                return self.send_error(404)

            self.send_response(200)
            self.send_header("Content-Type", 
                             "multipart/x-mixed-replace; boundary=jpgboundary")
            self.send_header("Connection", "keep-alive")
            self.send_header("Transfer-Encoding", "chunked")

            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            self.end_headers()

            boundary = b"--jpgboundary\r\n"
            trailer = b"\r\n"

            try:
                while True:
                    frame = server_stream_queue.get()
                    part = (
                        boundary +
                        b"Content-Type: image/jpeg\r\n" +
                        f"Content-Length: {len(frame)}\r\n\r\n".encode() +
                        frame +
                        trailer
                    )
                    chunk_header = f"{len(part):X}\r\n".encode()
                    self.wfile.write(chunk_header)
                    self.wfile.write(part)
                    self.wfile.write(b"\r\n")
                    self.wfile.flush()
                    time.sleep(delay)
            except (BrokenPipeError, ConnectionResetError):
                return

            # if self.path == "/rgb":
            #     try:
            #         self.send_response(200)
            #         self.send_header(
            #             "Content-type",
            #             "multipart/x-mixed-replace; boundary=--jpgboundary",
            #         )
            #         self.end_headers()
            #         while True:
            #             frame_data = server_stream_queue.get()
            #
            #             self.wfile.write("--jpgboundary".encode())
            #             self.wfile.write(bytes([13, 10]))
            #             self.send_header("Content-type", "image/jpeg")
            #             # self.send_header("Content-length", str(len(frame.getData())))
            #             self.send_header("Content-length", str(len(frame_data)))
            #             self.end_headers()
            #             # self.wfile.write(frame.getData())
            #             self.wfile.write(frame_data)
            #             self.end_headers()
            #             self.wfile.flush()
            #             time.sleep(delay)
            #
            #     except Exception as ex:
            #         print("Client disconnected")

    # class ThreadingSimpleServer(HTTPServer):
    #     pass
    #
    # with ThreadingSimpleServer(("127.0.0.1", stream_port), HTTPHandler) as httpd:
    #
    #     def handle_sigterm(signum, frame):
    #         print(
    #             f"Received SIGTERM, stopping camera stream server for 127.0.0.1:{stream_port}"
    #         )
    #         sys.exit(0)
    #
    #     signal.signal(signal.SIGTERM, handle_sigterm)
    #
    #     print(f"Serving RGB MJPEG stream at 127.0.0.1:{stream_port}/rgb")
    #     httpd.serve_forever(poll_interval=1)

    class ThreadingSimpleServer(HTTPServer):
        pass

    server = ThreadingSimpleServer(("127.0.0.1", stream_port), MJPEGHandler)

    def handle_sigterm(signum, frame):
        print(f"Received SIGTERM, stopping camera stream server on port {stream_port}")
        server.shutdown()

    signal.signal(signal.SIGTERM, handle_sigterm)

    print(f"Serving RGB MJPEG stream at http://127.0.0.1:{stream_port}/rgb")
    server.serve_forever(poll_interval=1)
