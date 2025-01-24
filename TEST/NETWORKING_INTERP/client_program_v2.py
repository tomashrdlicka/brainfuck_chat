from bf_interpreter_net import DualBrainfuckInterpreter

# Example Brainfuck Client Code
brainfuck_client_code = """
,
|                     # Open a socket
~                     # Connect to the server
[                     # Loop until the cell at the pointer is 0
§                     # Send data
,
§
,
]                     # End of loop
/                     # Close the socket
"""

if __name__ == "__main__":
    print("Starting Brainfuck client... Type your message:")
    user_input = input()  # Take input from the terminal
    interpreter = DualBrainfuckInterpreter(brainfuck_client_code)
    interpreter.run(input_data=user_input)