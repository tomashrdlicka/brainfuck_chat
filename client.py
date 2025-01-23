import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

while True:
    msg = input("You: ")
    if msg.strip() == "exit":
        break
    client.send(msg.encode())
    print(client.recv(1024).decode())

client.close()
