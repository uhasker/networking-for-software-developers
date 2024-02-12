# TCP

## Basics

TCP is:

- connection-oriented
- ensures reliable data transfer
- has error checking and correction
- flow control + congestion control
- full-duplex communication
- ordered data transfer
- graceful termination

## Stream Sockets

Stream Sockets

Socket = abstract representation for endpoint for network communication, identified by (IP, port)

Functions:

- socket() to create new socket (identified by an integer) and allocate system resources
- bind() to associate socket with socket address structure (IP + port)
- listen() to enter listening state
- connect() to assign free port number to socket
- accept() to accept received incoming attempt to create TCP connection & create new socket
- send(), recv() to send/recv data
- close() to release resources and terminate connection

View all sockets:

```sh
ss -tp
```

## Three-Way Handshake

Handshake:

- client sends SYN to server with sequence number (Seq) set to A
- server replies with SYN-ACK with acknowledgment number (Ack) to set to A+1 and Seq set to B
- client sends back ACK to server with SEQ=A+1, ACK=B+1

## Terminating a Connection

Regular connection termination:

- endpoint that wants to stop connection → transmits FIN packet which is acknowledged with FIN-ACK
- other endpoints does the same

Terminating connection with RST:

- send a packet with RST flag set

## Example

Server:

```python
import socket


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))  # Bind to localhost and port 12345
    server_socket.listen()

    print("Server is waiting for a connection...")
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    while True:
        data = conn.recv(1024)  # Receive data from the client
        if not data:
            break
        print(f"Received from client: {data.decode()}")
        conn.sendall(data)  # Echo back the received data

    conn.close()


if __name__ == "__main__":
    start_server()
```

Client:

```python
import socket


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))  # Connect to server at localhost and port 12345

    while True:
        message = input("Enter a message: ")
        if message == 'quit':
            break
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        print(f"Received from server: {data.decode()}")

    client_socket.close()


if __name__ == "__main__":
    start_client()
```
