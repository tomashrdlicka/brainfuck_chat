from bf_interpreter import BrainfuckInterpreter

# Example Brainfuck program
code = "-[------->+<]>."  # Outputs 'A'
interpreter = BrainfuckInterpreter(code)
output = interpreter.run()
print(output)  # Should print 'A'
