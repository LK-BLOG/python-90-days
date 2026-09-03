# Day 53 课程：网络编程基础

## 第一部分：Socket编程

### 1.1 TCP Socket
`python
import socket

# TCP服务器
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 8080))
server.listen(5)

while True:
    conn, addr = server.accept()
    data = conn.recv(1024)
    conn.sendall(b"Echo: " + data)
    conn.close()

# TCP客户端
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 8080))
client.sendall(b"Hello, Server!")
response = client.recv(1024)
client.close()
`

### 1.2 UDP Socket
`python
# UDP服务器
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("0.0.0.0", 9090))

while True:
    data, addr = server.recvfrom(1024)
    server.sendto(b"Echo: " + data, addr)
`

---

## 第二部分：HTTP服务器原理

### 2.1 HTTP请求/响应
`
GET /index.html HTTP/1.1\r\n
Host: localhost:8080\r\n
\r\n

→ 响应:
HTTP/1.1 200 OK\r\n
Content-Type: text/html\r\n
Content-Length: 13\r\n
\r\n
<h1>Hello</h1>
`

### 2.2 简单HTTP服务器
`python
import socket

def handle_request(client_socket):
    request = client_socket.recv(4096).decode()
    lines = request.split("\r\n")
    method, path, _ = lines[0].split(" ", 2)

    if path == "/":
        body = "<h1>Hello World</h1>"
        status = "200 OK"
    else:
        body = "Not Found"
        status = "404 Not Found"

    response = f"HTTP/1.1 {status}\r\nContent-Length: {len(body)}\r\n\r\n{body}"
    client_socket.sendall(response.encode())
    client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 8080))
server.listen(5)
print("Server running on port 8080")

while True:
    client, addr = server.accept()
    handle_request(client)
`

---

## 第三部分：异步IO模型

### 3.1 阻塞IO
`python
# 同步阻塞：一个请求一个线程
def handle_client(conn):
    data = conn.recv(1024)  # 阻塞等待
    conn.sendall(b"Response")
    conn.close()

while True:
    conn, addr = server.accept()  # 阻塞等待
    thread = threading.Thread(target=handle_client, args=(conn,))
    thread.start()
`

### 3.2 select
`python
import select

sockets = [server]
while True:
    readable, _, _ = select.select(sockets, [], [], 1.0)
    for s in readable:
        if s is server:
            conn, addr = server.accept()
            sockets.append(conn)
        else:
            data = s.recv(1024)
            if data:
                s.sendall(b"Echo: " + data)
            else:
                s.close()
                sockets.remove(s)
`

### 3.3 epoll（Linux高性能）
`python
import selectors

sel = selectors.DefaultSelector()  # 自动选择epoll/kqueue/select

def accept(sock):
    conn, addr = sock.accept()
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn):
    data = conn.recv(1024)
    if data:
        conn.sendall(b"Echo: " + data)
    else:
        sel.unregister(conn)
        conn.close()

server.setblocking(False)
sel.register(server, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj)
`

### 3.4 性能对比
| 模型 | 并发能力 | 复杂度 | 适用场景 |
|------|---------|--------|---------|
| 阻塞+多线程 | 1000+ | 低 | 简单应用 |
| select | 1024 | 中 | 跨平台 |
| poll | 无限制 | 中 | Linux |
| epoll | 100K+ | 高 | 高性能 |
| asyncio | 100K+ | 中 | Python首选 |

---

## 本课总结

| 概念 | 说明 |
|------|------|
| TCP | 可靠连接，适合HTTP |
| UDP | 不可靠，适合DNS/视频 |
| select | 跨平台，有fd限制 |
| epoll | Linux高性能，事件驱动 |
| asyncio | Python协程，最实用 |
