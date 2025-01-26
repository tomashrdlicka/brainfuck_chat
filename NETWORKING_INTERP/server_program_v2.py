from bf_interpreter_net import DualBrainfuckInterpreter

# Define the Brainfuck server program
# The server opens a socket, accepts a client connection, and sends "Hi!"
brainfuck_code = """
|                     # Open a socket
\                     # Accept a client connection (client 1)
*                     # Receive data
.                     # Print the received data
[                     # Loop until the cell at the pointer is 0
*                     # Receive data
.                     # Print the received data
]                     # End of loop
/                     # Close the socket
"""


# Run the server
print("Starting Brainfuck server...")
interpreter = DualBrainfuckInterpreter(brainfuck_code)
interpreter.run()