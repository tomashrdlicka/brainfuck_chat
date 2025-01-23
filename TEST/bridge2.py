import socket
import threading
from bf_interpreter import BrainfuckInterpreter

def handle_client_input(client, client_id, bf_server, other_client):
    """
    Handles input from a single client.
    - Reads the client's input.
    - Passes it to the BF server.
    - Sends the server's output to the other client.
    """
    while True:
        try:
            # Receive message from the client
            data = client.recv(1024).decode()
            if not data:
                break

            # Prefix the message with the sender ID
            bf_input = f"{client_id}{data}"

            # Process the message through the BF server
            server_output = bf_server.run(bf_input)

            # Send the server's output to the other client
            other_client.sendall(server_output.encode())

        except ConnectionResetError:
            print(f"Client {client_id} disconnected.")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

def main():
    # Load the Brainfuck server code
    with open("server.bf", "r") as f:
        server_code = f.read()

    # Create a Brainfuck interpreter for the server
    bf_server = BrainfuckInterpreter(server_code)

    # Set up the TCP server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 3000))
    server_socket.listen(2)
    print("Waiting for two clients to connect...")

    # Accept connections from two clients
    client1, addr1 = server_socket.accept()
    print(f"Client 1 connected: {addr1}")
    client2, addr2 = server_socket.accept()
    print(f"Client 2 connected: {addr2}")

    # Create threads to handle each client's input
    threading.Thread(target=handle_client_input, args=(client1, "1", bf_server, client2)).start()
    threading.Thread(target=handle_client_input, args=(client2, "2", bf_server, client1)).start()

if __name__ == "__main__":
    main()
