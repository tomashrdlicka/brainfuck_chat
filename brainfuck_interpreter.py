def brainfuck_interpreter(code, input_string=""):
    cells = [0] * 30000
    pointer = 0
    input_pointer = 0
    output = ""
    code_pointer = 0
    stack = []

    while code_pointer < len(code):
        cmd = code[code_pointer]

        if cmd == ">":
            pointer += 1
        elif cmd == "<":
            pointer -= 1
        elif cmd == "+":
            cells[pointer] = (cells[pointer] + 1) % 256
        elif cmd == "-":
            cells[pointer] = (cells[pointer] - 1) % 256
        elif cmd == ".":
            output += chr(cells[pointer])
            debug_print_state(
                cmd=cmd,
                code=code,
                code_pointer=code_pointer,
                pointer=pointer,
                cells=cells,
                input_pointer=input_pointer,
                output=output,
                stack=stack,
                debug_range=5  # Adjust for how many cells around the pointer you want to see
            )

        elif cmd == ",":
            if input_pointer < len(input_string):
                cells[pointer] = ord(input_string[input_pointer])
                input_pointer += 1
            else:
                cells[pointer] = 0
        elif cmd == "[":
            if cells[pointer] == 0:
                loop = 1
                while loop > 0:
                    code_pointer += 1
                    if code[code_pointer] == "[":
                        loop += 1
                    elif code[code_pointer] == "]":
                        loop -= 1
            else:
                stack.append(code_pointer)
        elif cmd == "]":
            if cells[pointer] != 0:
                code_pointer = stack[-1]
            else:
                stack.pop()
                
        
        code_pointer += 1

    return output

def debug_print_state(cmd, code, code_pointer, pointer, cells, input_pointer, output, stack, debug_range=5):
    """
    Prints a debug statement showing the state of the Brainfuck interpreter after executing one command.
    """
    # Compute the slice of memory to display
    start = max(0, pointer - debug_range)
    end = min(len(cells), pointer + debug_range + 1)
    cells_slice = cells[start:end]

    debug_info = (
        f"\n=== DEBUG STATE ===\n"
        f"Command: {repr(cmd)} | code_pointer: {code_pointer}\n"
        f"Pointer: {pointer}, Cell Value: {cells[pointer]}\n"
        f"Memory[{start}:{end}]: {cells_slice}\n"
        f"Input Pointer: {input_pointer}\n"
        f"Output so far: {repr(output)}\n"
        f"Loop Stack: {stack}\n"
        f"=== END DEBUG STATE ===\n"
    )
    print(debug_info)

if __name__ == "__main__":
    # Paste your Brainfuck code here
    brainfuck_code = "-[------->+<]>-."

    input_string = "Optional input here"  # Add input if your code uses `,`

    # Run the interpreter
    output = brainfuck_interpreter(brainfuck_code, input_string)
    print("Output:", output)