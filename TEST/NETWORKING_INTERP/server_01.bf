@socket_open          # Open a socket
@socket_accept        # Accept a client connection
-[------->+<]>-.         # Load ASCII value for 'H' (72)
@socket_send          # Send 'H'
+[----->+++<]>++.         # Load ASCII value for 'i' (105)
@socket_send          # Send 'i'
++++[->++++++++<]>+.          # Load ASCII value for '!' (33)
@socket_send          # Send '!'