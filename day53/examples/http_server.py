\"\"\"简单HTTP服务器\"\"\"

import socket
import os
from pathlib import Path
from urllib.parse import unquote


MIME_TYPES = {
    \".html\": \"text/html\",
    \".css\": \"text/css\",
    \".js\": \"application/javascript\",
    \".json\": \"application/json\",
    \".png\": \"image/png\",
    \".jpg\": \"image/jpeg\",
    \".txt\": \"text/plain\",
}


def parse_request(request: str) -> tuple[str, str, dict]:
    lines = request.split(\"\\r\\n\")
    method, path, version = lines[0].split(\" \", 2)

    headers = {}
    for line in lines[1:]:
        if \":\" in line:
            key, value = line.split(\":\", 1)
            headers[key.strip()] = value.strip()

    return method, path, headers


def handle_client(conn: socket.socket, static_dir: str = \"./static\"):
    try:
        data = conn.recv(4096).decode(\"utf-8\")
        if not data:
            return

        method, path, headers = parse_request(data)
        print(f\"{method} {path}\")

        if path == \"/\":
            body = b\"<html><body><h1>Hello World!</h1><p>Simple HTTP Server</p></body></html>\"
            content_type = \"text/html\"
            status = \"200 OK\"
        elif path == \"/health\":
            body = b'{\"status\": \"ok\"}'
            content_type = \"application/json\"
            status = \"200 OK\"
        else:
            # 静态文件
            file_path = Path(static_dir) / unquote(path.lstrip(\"/\"))
            if file_path.is_file():
                body = file_path.read_bytes()
                content_type = MIME_TYPES.get(file_path.suffix, \"application/octet-stream\")
                status = \"200 OK\"
            else:
                body = b\"404 Not Found\"
                content_type = \"text/plain\"
                status = \"404 Not Found\"

        response = (
            f\"HTTP/1.1 {status}\\r\\n\"
            f\"Content-Type: {content_type}\\r\\n\"
            f\"Content-Length: {len(body)}\\r\\n\"
            f\"Connection: close\\r\\n\"
            f\"\\r\\n\"
        ).encode(\"utf-8\") + body

        conn.sendall(response)
    finally:
        conn.close()


def start_http_server(host: str = \"0.0.0.0\", port: int = 8000, static_dir: str = \"./static\"):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f\"HTTP Server on http://{host}:{port}\")

    # 创建静态文件目录
    os.makedirs(static_dir, exist_ok=True)
    (Path(static_dir) / \"index.html\").write_text(\"<h1>Static Page</h1>\")

    try:
        while True:
            conn, addr = server.accept()
            handle_client(conn, static_dir)
    except KeyboardInterrupt:
        print(\"\\nServer stopped\")
    finally:
        server.close()


if __name__ == \"__main__\":
    start_http_server()
