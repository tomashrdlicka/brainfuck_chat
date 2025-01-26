from interp_net_multi import DualBrainfuckInterpreter

# Define the Brainfuck server program
# The server opens a socket, accepts a client connection, and sends "Hi!"
brainfuck_code = """
+
[
|                     # Open server socket
\                     # Accept connection from Client 1 (set conn1)
\                     # Accept connection from Client 2 (set conn2)
*                     # Receive data sender
>                     # Move to receiver
*                     # Receive data receiver
>                     # Move to payload


*
[
§
*
]
§


    
<
<
*
>
*
>
*
[
§
*
§
]
<
<
/                     # Close the socket
+
]
"""


# Run the server
print("Starting Brainfuck server...")
interpreter = DualBrainfuckInterpreter(brainfuck_code)
interpreter.run()