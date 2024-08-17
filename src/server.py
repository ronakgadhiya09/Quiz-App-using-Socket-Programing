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
server_socket.listen(5)  # Allow multiple clients to connect

print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")

# Class to handle each client
class QuizClientHandler(threading.Thread):
    def __init__(self, client_socket, client_address):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address
        self.score = 0

    def run(self):
        try:
            for i, question in enumerate(questions):
                question_with_index = f"{i+1}. {question}"  # Add the index before the question
                for option in options[i]:
                    question_with_index += "#" + option
                self.client_socket.send(question_with_index.encode())

                # Simulate waiting time for answering the question
                time.sleep(20)  # Wait 20 seconds for the answer

                # Receive answer from the client
                client_answer = self.client_socket.recv(1024).decode()
                if client_answer.lower() == answers[i].lower():
                    feedback = "Correct! ✅"
                    self.score += 1
                elif client_answer.lower() == "xyz":
                    feedback = "Time's up!"
                else:
                    feedback = "Wrong! ❌"

                # Send feedback to the client
                self.client_socket.send(feedback.encode())

                # Simulate waiting time for showing feedback and next question
                time.sleep(5)  # Wait 5 seconds before next question

            # Send final score
            self.client_socket.send(f"Your final score is: {self.score}/{len(questions)}".encode())

        except Exception as e:
            print(f"Error with {self.client_address}: {e}")
        finally:
            self.client_socket.close()

# Accept incoming connections
while True:
    client_socket, client_address = server_socket.accept()
    print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")

    # Create a thread to handle the client
    client_handler = QuizClientHandler(client_socket, client_address)
    client_handler.start()
