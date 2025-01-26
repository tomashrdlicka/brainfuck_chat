import socket

class DualBrainfuckInterpreter:
    def __init__(self, code):
        self.code = code
        self.cells = [0] * 30000  # Memory tape
        self.pointer = 0         # Memory pointer
        self.output = ""         # Collected output
        self.input = []          # Input buffer
        self.ip = 0              # Instruction pointer
        self.socket = None       # Socket object
        self.conn = None         # Connection object (server only)

    def run(self, input_data=""):
        valid_bf_commands = "><+-.,[]"  # Regular Brainfuck commands
        valid_custom_commands = "|~\\§*/"  # Unified custom commands

        # Filter the code to include only valid commands
        filtered_code = []
        i = 0
        
        while i < len(self.code):
            if self.code[i] in valid_bf_commands or self.code[i] in valid_custom_commands:
                filtered_code.append(self.code[i])
                i += 1
            else:
                # Ignore invalid characters, whitespace, or comments
                i += 1

        self.code = "".join(filtered_code)
        print(f"Filtered Brainfuck code: {self.code}")

        self.input = list(input_data)  # Convert input string into a list of characters
        self.output = ""
        self.ip = 0
        loop_stack = []

        while self.ip < len(self.code):
            cmd = self.code[self.ip]
            
            self.debug_print_state(cmd=cmd)

            # Socket management commands
            if cmd == "|":  # Open a socket
                print("Executing: Open socket")
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            elif cmd == "~":  # Connect to server (client-side)
                if self.socket:
                    print("Executing: Connect to server")
                    self.socket.connect(('localhost', 12345))
                    print("Connected to the server!")

            elif cmd == "\\":  # Accept a connection (server-side)
                if self.socket:
                    print("Executing: Accept connection")
                    self.socket.bind(('localhost', 12345))
                    self.socket.listen(1)
                    self.conn, addr = self.socket.accept()
                    print(f"Accepted connection from {addr}")

            elif cmd == "*":  # Receive data
                if self.conn:  # Use the connection object for receiving data
                    print("Executing: Receive data")
                    try:
                        received_data = self.conn.recv(1024)  # Buffer size is 1024 bytes
                        if received_data:
                            received_char = received_data.decode('utf-8')[0]
                            print(f"Received data: {received_char}")
                            self.cells[self.pointer] = ord(received_char)
                        else:
                            print("Connection closed by client.")
                            self.cells[self.pointer] = 0
                    except ConnectionResetError:
                        print("Connection reset by client.")
                        self.cells[self.pointer] = 0
                elif self.socket:  # Client-side receive
                    print("Executing: Receive data (client)")
                    try:
                        received_data = self.socket.recv(1024)
                        if received_data:
                            received_char = received_data.decode('utf-8')[0]
                            print(f"Received data: {received_char}")
                            self.cells[self.pointer] = ord(received_char)
                        else:
                            print("Connection closed by server.")
                            self.cells[self.pointer] = 0
                    except ConnectionResetError:
                        print("Connection reset by server.")
                        self.cells[self.pointer] = 0

            elif cmd == "§":  # Send data
                if self.conn:  # Server-side send
                    print("Executing: Send data (server)")
                    data_to_send = chr(self.cells[self.pointer])
                    self.conn.sendall(data_to_send.encode('utf-8'))
                    print(f"Sent data: {data_to_send} (ASCII {self.cells[self.pointer]})")
                elif self.socket:  # Client-side send
                    print("Executing: Send data (client)")
                    data_to_send = chr(self.cells[self.pointer])
                    self.socket.sendall(data_to_send.encode('utf-8'))
                    print(f"Sent data: {data_to_send} (ASCII {self.cells[self.pointer]})")

            elif cmd == "/":  # Close the socket
                if self.conn:
                    print("Executing: Close connection")
                    self.conn.close()
                    self.conn = None
                    print("Connection closed.")
                if self.socket:
                    print("Executing: Close socket")
                    self.socket.close()
                    self.socket = None
                    print("Socket closed.")

            # Standard Brainfuck commands
            elif cmd == ">":
                self.pointer += 1
                if self.pointer >= len(self.cells):
                    self.pointer = 0  # Wrap around

            elif cmd == "<":
                self.pointer -= 1
                if self.pointer < 0:
                    self.pointer = len(self.cells) - 1  # Wrap around

            elif cmd == "+":
                self.cells[self.pointer] = (self.cells[self.pointer] + 1) % 256

            elif cmd == "-":
                self.cells[self.pointer] = (self.cells[self.pointer] - 1) % 256

            elif cmd == ".":
                char = chr(self.cells[self.pointer])
                self.output += char
                print(f"Output: {char} (ASCII {self.cells[self.pointer]})")

            elif cmd == ",":
                if self.input:
                    self.cells[self.pointer] = ord(self.input.pop(0))
                    #print(self.input)
                else:
                    self.cells[self.pointer] = 0  # EOF simulation

            elif cmd == "[":
                if self.cells[self.pointer] == 0:
                    # Skip to the matching closing bracket
                    open_brackets = 1
                    while open_brackets > 0:
                        self.ip += 1
                        if self.ip >= len(self.code):
                            raise SyntaxError("Unmatched '[' encountered.")
                        if self.code[self.ip] == "[":
                            open_brackets += 1
                        elif self.code[self.ip] == "]":
                            open_brackets -= 1
                else:
                    loop_stack.append(self.ip)

            elif cmd == "]":
                if self.cells[self.pointer] != 0:
                    if not loop_stack:
                        raise SyntaxError("Unmatched ']' encountered.")
                    self.ip = loop_stack[-1]  # Jump back to matching "["
                else:
                    loop_stack.pop()

            #self.debug_print_state(cmd)
            self.ip += 1

        return self.output

    def debug_print_state(self, cmd):
        # Choose how many cells you want to see around the pointer
        debug_range = 5

        # Compute boundaries
        start = max(0, self.pointer - debug_range)
        end = min(len(self.cells), self.pointer + debug_range + 1)

        # Extract the slice
        cells_slice = self.cells[start:end]

        # Build debug output
        debug_info = (
            f"IP={self.ip}, CMD={cmd}, PTR={self.pointer}, "
            f"CELL={self.cells[self.pointer]}  |  "
            f"CELLS[{start}:{end}]={cells_slice}"
        )
        print(debug_info)