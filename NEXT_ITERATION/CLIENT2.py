
    

from INTERPRETER import BrainfuckInterpreter

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
        |                     # Open a socket >>++++++++++. 10
        ~                     # Connect to the server +.<< 11


        +
        [
        [-]
        *                     #receive data ++++++++++++. 12
        .
        ]

        <
        <
        !                     #send sender >>>>+++.<<<< 14
        >
        !                     #send receiver >>>+.<<< 15
        >
        ,
        [
        !                     #send payload >>+.<< 16
        ,
        ]
        !                     #send payload >.< 16
        

        /                     # Close the socket >>++. 18                      
        """

        # Run the interpreter with the user's input
        interpreter = BrainfuckInterpreter(brainfuck_client_code)
        interpreter.run(input_data=user_input)

        print("Message sent. Waiting for further input...")