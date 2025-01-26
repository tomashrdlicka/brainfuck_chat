from interp import BrainfuckInterpreter

# Define the Brainfuck server program
# The server opens a socket, accepts a client connection, and sends "Hi!"
brainfuck_code = """
+                     #init loop condition
[                     #start loop
|                     # Open server socket
\                     # Accept connection from Client 1 (set conn1)
\                     # Accept connection from Client 2 (set conn2)
*                     # Receive data sender
>                     # Move to receiver
*                     # Receive data receiver
>                     # Move to payload


*                     #receive payload
[                     #start loop
§                     #send payload
*                     #receive payload
]                     #end loop
§                     #send payload


    
<                     #move pointer to receiver cell
<                     #move pointer to sender cell
*                     #receive sender

>                     #move pointer to receiver cell
*                     #receive receiver
>                     #move pointer to payload cell
*                     #receive payload

[                     #start loop
§                     #send payload
*                     #receive payload
]                     #end loop
§                     #send payload



<                     #move pointer to receiver cell
<                     #move pointer to sender cell
/                     # Close the socket
+                     #init loop condition
]                     #end loop
"""


# Run the server
print("Starting Brainfuck server...")
interpreter = BrainfuckInterpreter(brainfuck_code)
interpreter.run()   