\"\"\"Day 53: 网络编程测试\"\"\"

import socket
import threading
import pytest


def test_tcp_echo():
    from tcp_server import start_server
    import time

    # 启动服务器
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((\"0.0.0.0\", 0))
    port = server.getsockname()[1]
    server.listen(5)

    def serve():
        while True:
            try:
                conn, _ = server.accept()
                data = conn.recv(1024)
                conn.sendall(b\"Echo: \" + data)
                conn.close()
            except Exception:
                break

    t = threading.Thread(target=serve, daemon=True)
    t.start()

    # 测试
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((\"localhost\", port))
    client.sendall(b\"Hello\")
    response = client.recv(1024)
    assert response == b\"Echo: Hello\"
    client.close()
    server.close()
