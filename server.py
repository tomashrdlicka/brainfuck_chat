import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 12345))
server.listen(1)
print("Server listening...")

conn, addr = server.accept()
print(f"Connection from {addr}")

while True:
    data = conn.recv(1024).decode()
    if not data or data.strip() == "exit":
        break
    print(f"Client: {data}")
    conn.send(f"Echo: {data}".encode())

conn.close()
server.close()
