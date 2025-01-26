from bf_interpreter_net import DualBrainfuckInterpreter

# Define the Brainfuck server program
# The server opens a socket, accepts a client connection, and sends "Hi!"
brainfuck_code = """
|                     # Open a socket
\                     # Accept a client connection
-[------->+<]>-     # Load ASCII value for 'H' (72)
§                     # Send 'H'
+[----->+++<]>++.       # Load ASCII value for 'i' (105)
§                     # Send 'i'
++++[->++++++++<]>+        # Load ASCII value for '!' (33)
§                     # Send '!'
/                     # Close the socket
"""


# Run the server
print("Starting Brainfuck server...")
interpreter = DualBrainfuckInterpreter(brainfuck_code)
interpreter.run()