import socket
import random
import json

host = ""
port = 7777
banner = """
=== Guessing Game ===
Choose difficulty level:
a - Easy (1-50)
b - Medium (1-100)
c - Hard (1-500)
Enter the letter then press 'enter' two times:"""

def generate_random_int(difficulty):
    if difficulty == 'a':
        return random.randint(1, 50)
    elif difficulty == 'b':
        return random.randint(1, 100)
    elif difficulty == 'c':
        return random.randint(1, 500)
    
def update_leaderboard(name, score, difficulty, leaderboard):
    leaderboard.append({"name": name, "score": score, "difficulty": difficulty})
    leaderboard.sort(key=lambda x: x["score"])
    return leaderboard[:10]

def save_leaderboard(leaderboard):
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f)

def load_leaderboard():
    try:
        with open("leaderboard.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Initialize the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print(f"The server is listening on port {port}")
guessme = 0
conn = None
leaderboard = load_leaderboard()

while True:
    if conn is None:
        print("Waiting for Connection..")
        conn, addr = s.accept()
        print(f"New Client: {addr[0]}")
        conn.sendall(banner.encode())
        
    else:
        try:
            client_input = conn.recv(1024).decode().strip()
        except ConnectionResetError:
            print("Client disconnected unexpectedly.")
            conn.close()
            conn = None
            
        if client_input in ['a', 'b', 'c']:
            difficulty = client_input
            guessme = generate_random_int(difficulty)
            conn.sendall(b"Enter your guess:")
            tries = 0
        elif client_input.isdigit():
            guess = int(client_input)
            print(f"User guess attempt: {guess}")
            tries += 1

            if guess == guessme:
                conn.sendall(b"Correct Answer!")
                name = conn.recv(1024).decode().strip()
                score = tries
                leaderboard = update_leaderboard(name, score, difficulty, leaderboard)
                save_leaderboard(leaderboard)
                conn.sendall(json.dumps(leaderboard).encode())  # Send leaderboard data
            elif guess > guessme:
                conn.sendall(b"Guess Lower!\nEnter guess: ")
            elif guess < guessme:
                conn.sendall(b"Guess Higher!\nEnter guess:")
        else:
            
            try:
               conn.sendall(b"Unknown difficulty level\nChoose the right difficulty level:")
            except BrokenPipeError:
             print("Client disconnected unexpectedly.")
            conn.close()
            conn = None


