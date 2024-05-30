import socket
import threading
import time
# Questions and Answers
questions_file = "questions.txt"
answers_file = "answers.txt"
options_file = "options.txt"

questions = []
answers = []
options = []

score = 0

# Read questions
with open(questions_file, "r") as file:
    for line in file:
        if line == '\n':
            continue
        questions.append(line.strip())  # Remove leading/trailing whitespace

# Read answers
with open(answers_file, "r") as file:
    for line in file:
        if line == '\n':
            continue
        answers.append(line.strip())  # Remove leading/trailing whitespace

with open(options_file, "r") as file:
    for line in file:
        if line == '\n':
            continue
        options.append(line.strip().split(','))

# Server configuration
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Listen for incoming connections
server_socket.listen(1)  # Allow only one client connection

print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")


# Function to handle client connections
def handle_client(client_socket):
    global score
    try:
        for i, question in enumerate(questions):
            question_with_index = f"{i+1}. {question}"  # Add the index before the question
            for option in options[i]:
                question_with_index += "#" + option
            client_socket.send(question_with_index.encode())
            # Simulate waiting time for answering the question
            time.sleep(20)  # Wait 30 seconds for answer

            # Receive answer from the client
            client_answer = client_socket.recv(1024).decode()
            if client_answer.lower() == answers[i].lower():
                feedback = "Correct! ✅"
                score += 1
            elif client_answer.lower() == "xyz":
                feedback = "Time's up!"
            else:
                feedback = "Wrong! ❌"

            # Send feedback to the client
            client_socket.send(feedback.encode())

            # Simulate waiting time for showing feedback and next question
            time.sleep(5)  # Wait 5 seconds before next question

        # Send final score
            
        client_socket.send(f"Your final score is: {score}/{len(questions)}".encode())
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

# Accept incoming connections
while True:
    client_socket, client_address = server_socket.accept()
    print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")

    # Create a thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
