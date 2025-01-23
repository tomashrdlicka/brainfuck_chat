class BrainfuckInterpreter:
    def __init__(self, code):
        self.code = code
        self.cells = [0] * 30000  # Memory tape
        self.pointer = 0  # Memory pointer
        self.output = ""  # Collected output
        self.input = []  # Input buffer
        self.ip = 0  # Instruction pointer

    def run(self, input_data=""):
        self.input = list(input_data)  # Convert input string into a list of characters
        self.output = ""
        self.ip = 0
        print(f"Starting Brainfuck interpreter with code: {self.code}")
        loop_stack = []
        while self.ip < len(self.code):
            cmd = self.code[self.ip]
            if cmd == ">":
                self.pointer += 1
            elif cmd == "<":
                self.pointer -= 1
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
                    print(f"Read input: {chr(self.cells[self.pointer])} (ASCII {self.cells[self.pointer]})")
                else:
                    self.cells[self.pointer] = 0  # EOF simulation
                    print("No input provided. Setting current cell to 0.")
            elif cmd == "[":
                if self.cells[self.pointer] == 0:
                    # Skip to the matching closing bracket
                    open_brackets = 1
                    while open_brackets > 0:
                        self.ip += 1
                        if self.code[self.ip] == "[":
                            open_brackets += 1
                        elif self.code[self.ip] == "]":
                            open_brackets -= 1
                else:
                    loop_stack.append(self.ip)
            elif cmd == "]":
                if self.cells[self.pointer] != 0:
                    self.ip = loop_stack[-1] - 1  # Jump back to matching "["
                else:
                    loop_stack.pop()
            self.ip += 1
            print(f"Cmd: {cmd}, Pointer: {self.pointer}, Cell: {self.cells[self.pointer]}, Output: {self.output}")
        return self.output




# Define the Brainfuck code
#THIS COMMAND WILL PRINT LETTER SEQUENCES OF VARIABLE LENGTH
brainfuck_code = "+[,.]"

# Create an instance of the BrainfuckInterpreter
interpreter = BrainfuckInterpreter(brainfuck_code)

# Run the interpreter with some input
input_data = "ABCD EFGH"  
output = interpreter.run(input_data)

# Print the output
print(f"Final Output: {output}")