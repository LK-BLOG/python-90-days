\"\"\"TCP客户端\"\"\"

import socket


def start_client(host: str = \"localhost\", port: int = 8080):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print(f\"Connected to {host}:{port}\")
    print(\"Type messages (Ctrl+C to quit):\")

    try:
        while True:
            message = input(\"> \")
            if not message:
                continue
            client.sendall(message.encode(\"utf-8\"))
            response = client.recv(4096).decode(\"utf-8\")
            print(f\"Server: {response}\")
    except KeyboardInterrupt:
        print(\"\\nDisconnecting...\")
    finally:
        client.close()


if __name__ == \"__main__\":
    start_client()
