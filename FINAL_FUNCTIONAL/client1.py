from interp import BrainfuckInterpreter

if __name__ == "__main__":
    print("Starting Brainfuck client...")

    # Define the infinite loop for continuous input
    while True:
        user_input = input("Type your message (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Exiting the client.")
            break  # Exit the loop and terminate the program

        brainfuck_client_code = """
        +                    #set sender as client 2
        >                     #move pointer to receiver cell
        ++                     #set receiver as client 1
        >                     #move pointer to payload
        |                     # Open a socket
        ~                     # Connect to the server
        ,                     #read payload
        <<                     #move to sender
        !                     #send data
        >                     #move to receiver
        !                     #send data
        >                     #move to payload


        [
        !
        ,
        ]

        >
        !
        <


        +
        [
        .
        *
        ]


        /                     # Close the socket
        """

        # Run the interpreter with the user's input
        interpreter = BrainfuckInterpreter(brainfuck_client_code)
        interpreter.run(input_data=user_input)

        print("Message sent. Waiting for further input...")