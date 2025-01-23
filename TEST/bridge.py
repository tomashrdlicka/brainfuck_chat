from bf_interpreter import BrainfuckInterpreter

def run_minimal_demo():
    # Load Brainfuck source files
    with open("server.bf", "r") as f:
        server_code = f.read()
    with open("client.bf", "r") as f:
        client_code = f.read()

    # Create Brainfuck interpreters
    server = BrainfuckInterpreter(server_code)
    client = BrainfuckInterpreter(client_code)

    # Run the client first to generate output
    client_output = client.run()  # No input needed for this minimal example
    print("Client output:", repr(client_output))  # For debugging

    # Run the server with the client's output as input
    server_output = server.run(client_output)
    print("Server echoed:", repr(server_output))  # For debugging

if __name__ == "__main__":
    run_minimal_demo()
