def python_to_brainfuck(python_code):
    brainfuck_code = ""
    variables = {}  # Map Python variables to Brainfuck memory cells
    pointer = 0     # Current pointer position on the Brainfuck tape
    loop_stack = []  # Track open loops

    for line in python_code.splitlines():
        line = line.strip()

        # Translate variable assignments (e.g., x = 65)
        if "=" in line and "+" not in line and "-" not in line:
            var, value = line.split("=")
            var = var.strip()
            value = int(value.strip())
            if var not in variables:
                variables[var] = pointer
                pointer += 1
            # Move to the variable's memory cell and set its value
            brainfuck_code += ">" * variables[var] + "+" * value + "<" * variables[var]

        # Handle arithmetic expressions (e.g., x = x + 1, x = x - 1)
        elif "=" in line and ("+" in line or "-" in line):
            var, expression = line.split("=")
            var = var.strip()
            expression = expression.strip()

            if "-" in expression:  # Decrement
                target_var, decrement = expression.split("-")
                target_var = target_var.strip()
                decrement = int(decrement.strip())
                brainfuck_code += ">" * variables[target_var] + "-" * decrement + "<" * variables[target_var]

            elif "+" in expression:  # Increment
                target_var, increment = expression.split("+")
                target_var = target_var.strip()
                increment = int(increment.strip())
                brainfuck_code += ">" * variables[target_var] + "+" * increment + "<" * variables[target_var]

        # Translate while loops (e.g., while x < 68)
        elif line.startswith("while"):
            var = line.split(" ")[1]  # Extract the variable name
            # Add the opening bracket for the loop
            brainfuck_code += ">" * variables[var] + "["

        # Close while loop (end of block)
        elif line == "" and loop_stack and loop_stack[-1] == "while":
            brainfuck_code += "]"  # Add the closing bracket
            loop_stack.pop()  # Pop from the loop stack

        # Translate print(x)
        elif line.startswith("print"):
            var = line.split("(")[1].split(")")[0].strip()
            brainfuck_code += ">" * variables[var] + "." + "<" * variables[var]

    return brainfuck_code

if __name__ == "__main__":
    python_code = """
    x = 65 
    while x < 68: 
        print(x)
        x = x + 1
    """
    brainfuck_code = (python_to_brainfuck(python_code))
    print(brainfuck_code)
    with open("output.bf", "w") as f:
        f.write(brainfuck_code)
    print("Brainfuck code generated and saved to output.bf")
