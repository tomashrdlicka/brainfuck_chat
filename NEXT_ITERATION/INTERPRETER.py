import socket

class BrainfuckInterpreter:
    def __init__(self, code):
        self.code = code
        self.cells = [0] * 30000  # Memory tape
        self.pointer = 0         # Memory pointer
        self.output = ""         # Collected output
        self.input = []          # Input buffer
        self.ip = 0              # Instruction pointer
        self.socket = None       # Socket object
        self.conn1 = None         # Connection object (server only)
        self.conn2 = None         # Connection object (server only)
        self.current_connection = 1
        
    def run(self, input_data=""):
        valid_bf_commands = "><+-.,[]"  # Regular Brainfuck commands
        #valid_custom_commands = "|~\\§*/!"  # Unified custom commands

        # Filter the code to include only valid commands
        filtered_code = []
        i = 0
        
        while i < len(self.code):
            if self.code[i] in valid_bf_commands:
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
            
            #self.debug_print_state(cmd=cmd)

            #Brainfuck commands
            if cmd == ">":
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
                
            elif cmd == ".":
                char_code = self.cells[self.pointer]
                
                # Print the ASCII as usual
                self.output += chr(char_code)
                print(f"Output: {repr(chr(char_code))} (ASCII {char_code})")
                
                # Check if it's one of our custom command codes
                if char_code in (10, 11, 12):  
                    self.handle_special_command(char_code)

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
    
    def handle_special_command(self, code):
        # Socket management commands
        # Socket management commands
        if code == 10:  # Open a socket |
            print("Executing: Open socket")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

        elif code == 11:  # Connect to server (client-side) ~
            if self.socket:
                print("Executing: Connect to server")
                self.socket.connect(('localhost', 12345))
                print("Connected to the server!")
                    

        elif code == 12:  # Single BFS command to receive data (1 byte each time) *
                print("[Debug] BFS invoked '*' for receiving 1 byte of data.")
                # 1) Server-side receive from conn1 (if it exists)
                if self.current_connection == 1 and self.conn1:
                    print("[Debug] Processing conn1 (Client 1).")
                    try:
                        one_byte = self.conn1.recv(1)  # Read exactly 1 byte from conn1
                        if one_byte:
                            c = int(one_byte[0])
                            print(f"[Debug] Server (conn1) received one byte: {c} (chr={chr(c)!r})")
                            self.cells[self.pointer] = c
                            print(f"[Debug] Stored ASCII {c} at cell[{self.pointer}].")
                            if c == 0:
                                print("[Debug] Switching to conn2 (Client 2) as conn1 sent 0.")
                                self.current_connection = 2  # Switch to conn2
                        else:
                            print("[Debug] No data from conn1 (Client 1) - possibly closed.")
                            self.cells[self.pointer] = 0
                            return
                    except ConnectionResetError:
                        print("[Debug] Connection reset by Client 1.")
                        self.cells[self.pointer] = 0
                        return

                elif self.current_connection == 2 and self.conn2:
                    print("[Debug] Processing conn2 (Client 2).")
                    try:
                        one_byte = self.conn2.recv(1)  # Read exactly 1 byte from conn2
                        if one_byte:
                            c = int(one_byte[0])
                            print(f"[Debug] Server (conn2) received one byte: {c} (chr={chr(c)!r})")
                            self.cells[self.pointer] = c
                            print(f"[Debug] Stored ASCII {c} at cell[{self.pointer}].")
                            if c == 0:
                                print("[Debug] Switching to conn1 (Client 1) as conn2 sent 0.")
                                self.current_connection = 1  # Switch to conn1
                        else:
                            print("[Debug] No data from conn2 (Client 2) - possibly closed.")
                            self.cells[self.pointer] = 0
                            return
                    except ConnectionResetError:
                        print("[Debug] Connection reset by Client 2.")
                        self.cells[self.pointer] = 0
                        return

                # 3) Client-side receive using self.socket
                elif self.socket:
                    print("[Debug] Detected client-side receive (self.socket is not None).")
                    try:
                        one_byte = self.socket.recv(1)  # read exactly 1 byte
                        if one_byte:
                            c = int(one_byte[0])
                            print(f"[Debug] Client received one byte: {c} (chr={chr(c)!r})")
                            self.cells[self.pointer] = c
                            print(f"[Debug] Stored ASCII {c} at cell[{self.pointer}].")
                        else:
                            print("[Debug] No data received from the server (connection closed?).")
                            self.cells[self.pointer] = 0
                    except ConnectionResetError:
                        print("[Debug] Connection reset by server.")
                        self.cells[self.pointer] = 0

                else:
                    print("[Debug] No valid server or client socket available (conn1, conn2, or self.socket).")
                    self.cells[self.pointer] = 0




        #server side send data
        elif code == 13:  # Server-side send §
            sender = self.cells[0]  # Sender identifier
            receiver = self.cells[1]  # Receiver identifier
            payload = chr(self.cells[self.pointer-2])  # Data to send

            if receiver == 1:
                print(f"Debug: Sending '{payload}' from Client {sender} to Client {receiver}")
                self.conn1.sendall(payload.encode('utf-8'))
            elif receiver == 2:
                print(f"Debug: Sending '{payload}' from Client {sender} to Client {receiver}")
                self.conn2.sendall(payload.encode('utf-8'))
                        
        #client side send data
        elif code == 14:  # Client-side single cell send ! for sender
            print("Executing: Client-side single cell send")
            # Retrieve the payload from the current pointer
            payload = chr(self.cells[self.pointer-2])  # Data to send (single character) 
            # Ensure we have a valid socket to send data
            if self.socket:
                try:
                    # Debug: Show the payload being sent
                    print(f"[Debug] Sending single-cell data: '{payload}' (ASCII: {ord(payload)})")

                    # Send the single character payload
                    self.socket.sendall(payload.encode('utf-8'))

                    # Debug: Confirm the payload was sent
                    print(f"[Debug] Single-cell data successfully sent: '{payload}'")
                except BrokenPipeError:
                    # Handle case where the server is not available
                    print("[Debug] Failed to send data. Broken pipe (server might be down).")
                except Exception as e:
                    # Catch any unexpected errors
                    print(f"[Debug] Unexpected error during send: {e}")
            else:
                # Debug: No valid socket available
                print("[Debug] No valid client socket. Unable to send data.")
                
        elif code == 15:  # Client-side single cell send ! for receiver
            print("Executing: Client-side single cell send")
            # Retrieve the payload from the current pointer
            payload = chr(self.cells[self.pointer-1])  # Data to send (single character) 
            # Ensure we have a valid socket to send data
            if self.socket:
                try:
                    # Debug: Show the payload being sent
                    print(f"[Debug] Sending single-cell data: '{payload}' (ASCII: {ord(payload)})")

                    # Send the single character payload
                    self.socket.sendall(payload.encode('utf-8'))

                    # Debug: Confirm the payload was sent
                    print(f"[Debug] Single-cell data successfully sent: '{payload}'")
                except BrokenPipeError:
                    # Handle case where the server is not available
                    print("[Debug] Failed to send data. Broken pipe (server might be down).")
                except Exception as e:
                    # Catch any unexpected errors
                    print(f"[Debug] Unexpected error during send: {e}")
            else:
                # Debug: No valid socket available
                print("[Debug] No valid client socket. Unable to send data.")
                
        elif code == 16:  # Client-side single cell send ! for payload
            print("Executing: Client-side single cell send")
            # Retrieve the payload from the current pointer
            payload = chr(self.cells[self.pointer])  # Data to send (single character) 
            # Ensure we have a valid socket to send data
            if self.socket:
                try:
                    # Debug: Show the payload being sent
                    print(f"[Debug] Sending single-cell data: '{payload}' (ASCII: {ord(payload)})")

                    # Send the single character payload
                    self.socket.sendall(payload.encode('utf-8'))

                    # Debug: Confirm the payload was sent
                    print(f"[Debug] Single-cell data successfully sent: '{payload}'")
                except BrokenPipeError:
                    # Handle case where the server is not available
                    print("[Debug] Failed to send data. Broken pipe (server might be down).")
                except Exception as e:
                    # Catch any unexpected errors
                    print(f"[Debug] Unexpected error during send: {e}")
            else:
                # Debug: No valid socket available
                print("[Debug] No valid client socket. Unable to send data.")
                
                #server side accept connections
        elif code == 17:  # Accept connections (server-side) \
            if self.socket:
                if not self.conn1:  # Accept first client
                    print("Waiting for Client 1 to connect...")
                    self.socket.bind(('localhost', 12345))  # Bind server to port 12345
                    self.socket.listen(2)  # Allow up to 2 queued connections
                    self.conn1, addr1 = self.socket.accept()  # Accept the first client
                    print(f"Client 1 connected from {addr1}")
                elif not self.conn2:  # Accept second client
                    print("Waiting for Client 2 to connect...")
                    self.conn2, addr2 = self.socket.accept()  # Accept the second client
                    print(f"Client 2 connected from {addr2}")



        elif code == 18:  # Close the socket /
            if self.conn1:
                print("Closing connection with Client 1...")
                self.conn1.close()
                self.conn1 = None
            if self.conn2:
                print("Closing connection with Client 2...")
                self.conn2.close()
                self.conn2 = None
            if self.socket:
                print("Closing the server socket...")
                self.socket.close()
                self.socket = None

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