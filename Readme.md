# QuBic Quiz Application

## Description
This is a socket programing based quiz application that allows clients to connect to a server, answer quiz questions within a time limit, receive feedback on their answers, and get their final scores.

## Features
- **Quiz Questions:** Server sends quiz questions to clients one by one.
- **Multiple-Choice Options:** Questions include multiple-choice options.
- **Timer:** Each question has a timer (20 seconds) for answering.
- **Answer Submission:** Clients can submit answers within the time limit.
- **Feedback:** Clients receive feedback on their answers (Correct, Wrong, or Time's Up).
- **Scoring:** Server keeps track of client scores based on correct answers.
- **Final Score:** Clients receive their final scores at the end of the quiz.
- **Multi-threading:** Server handles multiple client connections concurrently using threads.
- **Themed GUI:** Client application has a themed GUI using Tkinter with radio buttons for options.
- **Responsive GUI:** Client GUI updates dynamically based on server interactions.
- **Timeout Handling:** Server handles cases where clients do not respond within the given time.
- **Configurability:** Quiz content (questions, answers, options) can be easily modified via text files.

## File Structure
- **client.py:** Client-side code for the quiz application.
- **server.py:** Server-side code for handling quiz questions and scoring.
- **questions.txt:** File containing quiz questions.Any changes in the questions can be done here.
- **answers.txt:** File containing correct answers corresponding to questions.Changes in the answers can be done through this file.
- **options.txt:** File containing multiple-choice options for questions.Xhanges in the options can be done here.

## How to Run
1. Start the server by running 'server.py' using following command

```bash
python server.py
```

2. Clients need to connect to the server by first writing host's ip address in ```SERVER_HOST``` in client.py and then by running 'client.py'using command.

```bash
python client.py
```

3. After that App GUI will pop up where questions of the quiz will be displayed.
4. Answer quiz questions within the time limit and receive feedback.
5. After answering all questions, receive the final score.

## Requirements
- Python 3.x
- tkinter library (for GUI)
- ThemedTk (for themed GUI)
- socket library (for network communication)
- threading library (for multi-threading)

## Contributors
- [Ronak Gadhiya](https://github.com/ronakgadhiya09)
- [Aatif Ahmad](https://github.com/aatifahmad123)

## License
This project is licensed under the [MIT License](LICENSE).
