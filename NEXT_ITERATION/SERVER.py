from INTERPRETER import BrainfuckInterpreter

# Define the Brainfuck server program
# The server opens a socket, accepts a client connection, and sends "Hi!"
brainfuck_code = """
+
[
|                     # Open server socket >>>>++++++++++. 10
\                     # Accept connection from Client 1 (set conn1) +++++++. 17
\                     # Accept connection from Client 2 (set conn2) . 17
[-]
*                     # Receive data sender <<<<++++++++++++.12
>                     # Move to receiver
[-]
*                     # Receive data receiver ++++++++++++. 12
>                     # Move to payload


*                     # Receive payload ++++++++++++. 12
[
§                     # Send payload >>----.<< 13
[-]
*                     # receive payload ++++++++++++. 12
]
§                     # Send payload >>.<< 
<
<
/                     # Close the socket >>+++++. 18

    
<
<
[-]
*                     # receive payload ++++++++++++. 12
>
[-]
*                     # receive payload ++++++++++++. 12
>
[-]
*                     # receive payload ++++++++++++. 12
[
§                     # Send payload >>-----.<< 13
[-]
*                     # receive payload ++++++++++++. 12
§                     # Send payload >>.<< 13
]
<
<
/                     # Close the socket >>+++++. 18
[-]
                        <<<< go to sender cell
]
"""


# Run the server
print("Starting Brainfuck server...")
interpreter = BrainfuckInterpreter(brainfuck_code)
interpreter.run()