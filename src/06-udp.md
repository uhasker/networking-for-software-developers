# UDP

## Example

Server:

```python
import socket


def start_udp_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    print(f"UDP server up and listening at {ip}:{port}")

    while True:
        data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
        print(f"Received message: {data.decode()} from {addr}")
        sock.sendto(data, addr)


start_udp_server("127.0.0.1", 12345)
```

Client:

```python
import socket


def start_udp_client(server_ip, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        message = input("Enter message to send: ")
        if message.lower() == 'exit':
            break
        sock.sendto(message.encode(), (server_ip, server_port))
        data, _ = sock.recvfrom(1024)
        print(f"Received echo: {data.decode()}")

    sock.close()


start_udp_client("127.0.0.1", 12345)
```
