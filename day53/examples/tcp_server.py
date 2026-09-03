\"\"\"TCP Echo服务器（多线程）\"\"\"

import socket
import threading


def handle_client(conn: socket.socket, addr):
    print(f\"New connection from {addr}\")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode(\"utf-8\")
            print(f\"[{addr}] {message}\")
            conn.sendall(f\"Echo: {message}\".encode(\"utf-8\"))
    except ConnectionResetError:
        pass
    finally:
        conn.close()
        print(f\"Disconnected: {addr}\")


def start_server(host: str = \"0.0.0.0\", port: int = 8080):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f\"TCP Server listening on {host}:{port}\")

    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print(\"\\nServer stopped\")
    finally:
        server.close()


if __name__ == \"__main__\":
    start_server()
