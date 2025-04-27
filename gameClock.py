import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from SQL_CON import SQL

# Initialize the main window
connection = SQL()
root = tk.Tk()
root.geometry("600x300")
root.title("My Game Stop Clock")

games = connection.list_games()

# Global variables for time tracking
second = 0
minute = 0
hour = 0
clock_on = False

# Center frame
center_frame = ttk.Frame(root)
center_frame.place(relx=0.5, rely=0.5, anchor="center")  # <--- THIS centers it!

# select game 
ttk.Label(center_frame, text="GAME:").grid(row=0, column=0, padx=5, pady=10, sticky="e")
game_var = tk.StringVar()
game_dropdown = ttk.Combobox(center_frame, textvariable=game_var, values=[game[1] for game in games], width=40, state="readonly")
game_dropdown.grid(row=0, column=1, padx=5, pady=10, sticky="w")

# Function to update the clock
def update_clock():
    global second, minute, hour

    if clock_on:
        second += 1
        if second == 60:
            second = 0
            minute += 1
        if minute == 60:
            minute = 0
            hour += 1

        time_label.config(text=f"{hour:02}:{minute:02}:{second:02}")
        root.after(1000, update_clock)

# Label to display the time
time_label = ttk.Label(center_frame, text="000:00:00", font=("Helvetica", 48))
time_label.grid(row=1, column=0, columnspan=2, pady=20)

# Button to start/stop the clock
def toggle_clock():
    global clock_on

    if clock_on:
        clock_on = False
        start_stop_button.config(text="Start")
    else:
        clock_on = True
        update_clock()
        start_stop_button.config(text="Stop")

start_stop_button = ttk.Button(center_frame, text="Start", command=toggle_clock)
start_stop_button.grid(row=2, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()
