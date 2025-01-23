from bf_interpreter_net import DualBrainfuckInterpreter

# Example Brainfuck Client Code
brainfuck_client_code = """
|                     # Open a socket
~                     # Connect to the server
*                     # Receive data (H)
*                     # Receive data (i)
*                     # Receive data (!)
/                     # Close the socket
"""

if __name__ == "__main__":
    # Create an instance of the BrainfuckClientInterpreter
    client_interpreter = DualBrainfuckInterpreter(brainfuck_client_code)

    # Run the client program
    client_interpreter.run()