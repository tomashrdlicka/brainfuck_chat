
    

from FINAL_FUNCTIONAL.interp import DualBrainfuckInterpreter

if __name__ == "__main__":
    print("Starting Brainfuck client...")

    # Define the infinite loop for continuous input
    while True:
        user_input = input("Type your message (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Exiting the client.")
            break  # Exit the loop and terminate the program

        brainfuck_client_code = """
        ++                     #set sender as client 2
        >                     #move pointer to receiver cell
        +                     #set receiver as client 1
        >                     #move pointer to payload
        |                     # Open a socket
        ~                     # Connect to the server


        +                     #init loop condition
        [                     #start loop
        *                     #receive data
        .                     #read payload
        ]                     #end loop

        <                     #move pointer to receiver cell
        <                     #move pointer to sender cell
        !                     #send sender
        >                     #move pointer to receiver cell
        !                     #send receiver
        >                     #move pointer to payload cell
        ,                     #read payload from input

        [                     #start loop
        !                     #send payload
        ,                     #read payload from input
        ]                     #end loop
        !                     #send payload

        /                     # Close the socket
        /
        """

        # Run the interpreter with the user's input
        interpreter = DualBrainfuckInterpreter(brainfuck_client_code)
        interpreter.run(input_data=user_input)

        print("Message sent. Waiting for further input...")