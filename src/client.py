import tkinter as tk
from tkinter import ttk  # Import themed tkinter
import socket
import threading
import time

# Server IP address and port
SERVER_HOST = '172.31.2.157'
SERVER_PORT = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create a Tkinter window
root = tk.Tk()
root.title("Quiz Client")
root.geometry('360x640')
root.configure(bg='#f8f9fb')

label = tk.Label(root, text='QuBic', fg='#70e000', bg='#f8f9fb', font=('Arial', 20, 'bold'))
label.pack(side='top')

# Global variables
time_left = 20  # Initial time (in seconds) for each question
timer_running = False  # Flag to track if the timer is running
questions_answered = 0
number_of_questions = 3


# Function to update the countdown timer label
def update_timer():
    global time_left, timer_running
    if time_left > 0 and timer_running:
        time_left -= 1
        timer_label.config(text=f"Time Left: {time_left} seconds")
        root.after(1000, update_timer)  # Schedule the next update after 1 second
    elif time_left <= 1:
        send_answer()
    else:
        timer_running = False
        radio_button1.config(state=tk.DISABLED)
        radio_button2.config(state=tk.DISABLED)
        radio_button3.config(state=tk.DISABLED)
        radio_button4.config(state=tk.DISABLED)

def deselect_radio_buttons():
    var.set("")  # Set the radiobutton variable to an empty string to deselect all radiobuttons

def receive_question():
    global time_left, timer_running, questions_answered, number_of_questions
    try:
        # Connect to the server
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        while True:
            # Receive questions from the server
            data = client_socket.recv(1024).decode()
            if not data:
                break

            data = data.split("#")
            question = data[0]
            question_label.config(text=question)
            if len(data) == 5:
                radio_button1.config(text=data[1])
                radio_button1.config(value=data[1])
                radio_button2.config(text=data[2])
                radio_button2.config(value=data[2])
                radio_button3.config(text=data[3])
                radio_button3.config(value=data[3])
                radio_button4.config(text=data[4])
                radio_button4.config(value=data[4])

            time_left = 20
            timer_running = True
            if questions_answered < number_of_questions:
                update_timer()

            elif questions_answered == number_of_questions:
                timer_label.destroy()
                radio_button1.destroy()
                radio_button2.destroy()
                radio_button3.destroy()
                radio_button4.destroy()
                A.destroy()
                B.destroy()
                C.destroy()
                D.destroy()

            feedback_label.config(text="")
            deselect_radio_buttons()

            radio_button1.config(state=tk.NORMAL)
            radio_button2.config(state=tk.NORMAL)
            radio_button3.config(state=tk.NORMAL)
            radio_button4.config(state=tk.NORMAL)
            root.update()

            time.sleep(20)
            radio_button1.config(state=tk.DISABLED)
            radio_button2.config(state=tk.DISABLED)
            radio_button3.config(state=tk.DISABLED)
            radio_button4.config(state=tk.DISABLED)

            questions_answered += 1

            time.sleep(5)

        feedback_label.config(text="")
        deselect_radio_buttons()
        final_score = client_socket.recv(1024).decode()
        feedback_label.config(text=final_score)

    except Exception as e:
        print(f"Error: {e}")


def get_selected_answer():
    return var.get()


def send_answer():
    global timer_running, time_left
    try:
        answer = get_selected_answer()
        deselect_radio_buttons()
        if answer == '':
            answer = 'xyz'
        client_socket.send(answer.encode())

        feedback = client_socket.recv(1024).decode()
        feedback_label.config(text=feedback)
        timer_running = False

    except Exception as e:
        print(f"Error: {e}")


question_label = tk.Label(root, text="", font=('Arial', 14), bg='#f8f9fb', wraplength=300)
question_label.place(relx=0.5, rely=0.2, anchor='center')

# Create a style for themed widgets
style = ttk.Style()
style.configure('TRadiobutton', background='#f8f9fb', font=('Arial', 12))

style.map('TRadiobutton',
          background=[('active', '#70e000')],  # hover background color
          foreground=[('active', '#ffffff')])  

# Use themed radiobuttons
var = tk.StringVar()
radio_button1 = ttk.Radiobutton(root, text="Option 1", value="Option 1", variable=var, style='TRadiobutton')
radio_button1.place(x=50, y=200)
A = tk.Label(root, text='A', fg='#70e000', bg='#f8f9fb', font=('Arial', 14, 'bold'))
A.place(x=25, y=200)

radio_button2 = ttk.Radiobutton(root, text="Option 2", value="Option 2", variable=var,style='TRadiobutton')
radio_button2.place(x=50, y=250)
B = tk.Label(root, text='B', fg='#70e000', bg='#f8f9fb', font=('Arial', 14, 'bold'))
B.place(x=25, y=250)

radio_button3 = ttk.Radiobutton(root, text="Option 3", value="Option 3", variable=var, style='TRadiobutton')
radio_button3.place(x=50, y=300)
C = tk.Label(root, text='C', fg='#70e000', bg='#f8f9fb', font=('Arial', 14, 'bold'))
C.place(x=25, y=300)

radio_button4 = ttk.Radiobutton(root, text="Option 4", value="Option 4", variable=var, style='TRadiobutton')
radio_button4.place(x=50, y=350)
D = tk.Label(root, text='D', fg='#70e000', bg='#f8f9fb', font=('Arial', 14, 'bold'))
D.place(x=25, y=350)

timer_label = tk.Label(root, text="", font=('Arial', 12), bg='#f8f9fb')
timer_label.place(relx=0.5, rely=0.1, anchor='center')

feedback_label = tk.Label(root, text="", font=('Arial', 12), bg='#f8f9fb')
feedback_label.place(relx=0.5, rely=0.7, anchor='center')

threading.Thread(target=receive_question).start()

root.mainloop()

client_socket.close()
