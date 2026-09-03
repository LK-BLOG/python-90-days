\"\"\"异步IO服务器（selectors）\"\"\"

import socket
import selectors
import types

sel = selectors.DefaultSelector()


def accept_connection(sock):
    conn, addr = sock.accept()
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b\"\", outb=b\"\")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def handle_connection(key, mask):
    conn = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = conn.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print(f\"Closing connection to {data.addr}\")
            sel.unregister(conn)
            conn.close()

    if mask & selectors.EVENT_WRITE and data.outb:
        sent = conn.send(data.outb)
        data.outb = data.outb[sent:]


def start_async_server(host: str = \"0.0.0.0\", port: int = 8081):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()
    server.setblocking(False)
    sel.register(server, selectors.EVENT_READ, data=None)
    print(f\"Async Server on {host}:{port}\")

    try:
        while True:
            events = sel.select(timeout=1)
            for key, mask in events:
                if key.data is None:
                    accept_connection(key.fileobj)
                else:
                    handle_connection(key, mask)
    except KeyboardInterrupt:
        print(\"\\nServer stopped\")
    finally:
        sel.close()
        server.close()


if __name__ == \"__main__\":
    start_async_server()
