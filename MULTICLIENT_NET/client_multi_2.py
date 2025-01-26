from interp_net_multi import DualBrainfuckInterpreter

# Example Brainfuck Client Code
brainfuck_client_code = """
++                     #set sender as client 2
>                     #move pointer to receiver cell
+                     #set receiver as client 1
>                     #move pointer to payload
|                     # Open a socket
~                     # Connect to the server
*                     #receive data
/                     # Close the socket
"""

if __name__ == "__main__":
    print("Starting Brainfuck client... Type your message:")
    user_input = input()  # Take input from the terminal
    interpreter = DualBrainfuckInterpreter(brainfuck_client_code)
    interpreter.run(input_data=user_input)