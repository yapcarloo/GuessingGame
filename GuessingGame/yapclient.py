import socket

host = "localhost"
port = 7777

while True:
    s = socket.socket()
    s.connect((host, port))

    try:
        data = s.recv(1024)
        if not data:
            print("Server disconnected.")
            break
        print(data.decode().strip())
    except ConnectionResetError:
        print("Server disconnected unexpectedly.")
        break

    print(data.decode().strip())
    difficulty_choice = input("")

    s.sendall(difficulty_choice.encode())

    while True:
        user_input = input("").strip()
        s.sendall(user_input.encode())
        reply = s.recv(1024).decode().strip()
        print(reply)
        if "Correct" in reply:
            name = input("Enter Your Name: ")
            s.sendall(name.encode())
            break

    # Receive the leaderboard from the server
    leaderboard_data = s.recv(1024).decode().strip()
    print(leaderboard_data)

    # Ask the user if they want to play again
    play_again = input("Do you want to play again? (y/n): ")
    s.sendall(play_again.encode())
    if play_again.lower() != 'y':
        s.close()
        break
