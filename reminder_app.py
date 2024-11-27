import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import time
import threading
import pygame  # For cross-platform sound

# Initialize Pygame mixer for sound playback
pygame.mixer.init()

# Function to play sound
def play_sound():
    # You can replace 'sound.wav' with the path to your sound file
    pygame.mixer.music.load("Reminder/ding-sound-246413.mp3")  # Add a sound file in the project folder
    pygame.mixer.music.play()

class ReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Creative Reminder Application")
        self.root.geometry("500x400")
        self.root.configure(bg="#1e2a47")  # Dark blue background for the whole window

        # Reminder time and message variables
        self.reminder_time = None
        self.reminder_message = None

        # Label for Title
        self.title_label = tk.Label(root, text="Set Your Reminder", font=("Arial", 18, "bold"), fg="#ffffff", bg="#1e2a47")
        self.title_label.pack(pady=20)

        # Label and Entry for Reminder Time
        self.time_label = tk.Label(root, text="Enter time (HH:MM:SS):", font=("Arial", 12), fg="#ffffff", bg="#1e2a47")
        self.time_label.pack(pady=5)
        
        self.time_entry = tk.Entry(root, font=("Arial", 14), bd=5, relief="solid")
        self.time_entry.pack(pady=10)

        # Label and Entry for Reminder Message
        self.message_label = tk.Label(root, text="Enter reminder message:", font=("Arial", 12), fg="#ffffff", bg="#1e2a47")
        self.message_label.pack(pady=5)
        
        self.message_entry = tk.Entry(root, font=("Arial", 14), bd=5, relief="solid")
        self.message_entry.pack(pady=10)
        
        # Set Reminder Button (Styled with color)
        self.set_button = tk.Button(root, text="Set Reminder", command=self.set_reminder, font=("Arial", 14, "bold"),
                                     bg="#4CAF50", fg="black", relief="raised", bd=3, activebackground="#45a049")
        self.set_button.pack(pady=20)

        # Label for Countdown Timer
        self.countdown_label = tk.Label(root, text="Time remaining: 00:00:00", font=("Arial", 14, "bold"), fg="#ffffff", bg="#1e2a47")
        self.countdown_label.pack(pady=10)

    def set_reminder(self):
        """Set the reminder with the specified time and message"""
        reminder_time_str = self.time_entry.get()
        self.reminder_message = self.message_entry.get()
        
        try:
            self.reminder_time = datetime.strptime(reminder_time_str, "%H:%M:%S")
            current_time = datetime.now()
            reminder_time = current_time.replace(hour=self.reminder_time.hour, minute=self.reminder_time.minute, second=self.reminder_time.second)

            # If the reminder time is earlier than the current time, set it for the next day
            if reminder_time < current_time:
                reminder_time = reminder_time.replace(day=current_time.day + 1)

            # Calculate the time difference in seconds
            wait_time = (reminder_time - current_time).total_seconds()
            
            # Start the countdown thread
            threading.Thread(target=self.countdown_timer, args=(wait_time,)).start()
            
            messagebox.showinfo("Reminder Set", f"Reminder set for {reminder_time.strftime('%H:%M:%S')}")
        
        except ValueError:
            messagebox.showerror("Invalid Time Format", "Please enter time in HH:MM:SS format.")
    
    def countdown_timer(self, wait_time):
        """Update the countdown timer and show the reminder after the wait time"""
        while wait_time > 0:
            minutes, seconds = divmod(int(wait_time), 60)
            hours, minutes = divmod(minutes, 60)
            time_left = f"{hours:02}:{minutes:02}:{seconds:02}"
            self.update_countdown(time_left)  # Update the countdown on the UI
            time.sleep(1)
            wait_time -= 1

        # Once the countdown is over, show the reminder
        self.show_reminder()

    def update_countdown(self, time_left):
        """Update the countdown timer label in the UI"""
        self.countdown_label.config(text=f"Time remaining: {time_left}")
        self.root.update()  # Force the UI to update

    def show_reminder(self):
        """Display the reminder message and play sound"""
        play_sound()  # Play the sound when the reminder time is reached
        messagebox.showinfo("Reminder Alert", self.reminder_message)

# Run the application
def run_reminder_app():
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_reminder_app()
