# main_window.py content
import customtkinter as ctk
from settings_window import SettingsWindow
from newPost import on_submit
import threading
import webbrowser
import time

def center_window(window, width, height):
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    # Calculate the x and y coordinates for the Tk root window
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    # Set the window's geometry 
    window.geometry(f'{width}x{height}+{x}+{y}')

class MainWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("AI Draft Post Creator")
        self.root.configure(bg="dark gray")
        self.root.tk_setPalette(background='dark gray')
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        self.root.geometry('400x350+50+50')  # Adjusted height from 300 to 350
        self.create_widgets()

    def create_widgets(self):
        # Settings Button with Gear Icon
        gear_icon = "⚙️"  # Unicode character for a gear icon
        settings_button = ctk.CTkButton(self.root, text=gear_icon, width=40, height=40, corner_radius=10,
                                        command=self.open_settings_window, fg_color="gray")
        settings_button.pack(side='top', anchor='ne', padx=10, pady=10)

        # Welcome label (moved to the top)
        welcome_label = ctk.CTkLabel(self.root, text="Welcome to AI Draft Post Creator", font=('Lato', 20, 'bold'))
        welcome_label.pack(side='top', pady=20)

        # Divider after welcome label
        divider1 = ctk.CTkFrame(self.root, height=2, fg_color="gray75")
        divider1.pack(side='top', fill='x', padx=10, pady=5)

        # App description label
        description_label = ctk.CTkLabel(self.root, text="This app helps you create draft posts for your blog with the power of AI. Simply enter the number of articles and let the AI do the rest.", font=("Lato", 10), wraplength=400)
        description_label.pack(side='top', padx=10, pady=5)

        # Divider after app description label
        divider2 = ctk.CTkFrame(self.root, height=2, fg_color="gray75")
        divider2.pack(side='top', fill='x', padx=10, pady=5)

        num_articles_frame = ctk.CTkFrame(self.root)
        num_articles_frame.pack(pady=10)
        num_articles_label = ctk.CTkLabel(num_articles_frame, text="Number of Articles:", font=("Lato", 10))
        num_articles_label.pack(side='left', padx=5)
        self.num_articles = 1
        self.counter = ctk.CTkEntry(num_articles_frame, width=3, font=("Lato", 10))
        self.counter.insert(0, self.num_articles)
        self.counter.pack(side='left')

        create_button = ctk.CTkButton(self.root, text="Create New Draft", command=self.create_new_draft, font=("Lato", 10))
        create_button.pack(pady=10)

        self.spinner_label = ctk.CTkLabel(self.root, text="")
        self.spinner_label.pack(side='top', fill='x', expand=True)

        # Instructional text label (moved to the bottom)
        instructions_label = ctk.CTkLabel(self.root, text="Please click the settings button in the top right corner to enter the required information before creating a new draft.", font=("Lato", 10), wraplength=400)
        instructions_label.pack(side='bottom', padx=10, pady=5)

    def open_settings_window(self):
        settings_window = SettingsWindow()
        settings_window.show()

    def create_new_draft(self):
        num_articles = self.counter.get()
        if num_articles.isdigit() and int(num_articles) > 0:
            # Initialize the timer
            self.start_time = time.time()
            # Show loading indicator and start the timer
            self.spinner_label.configure(text="Loading... 0 seconds")
            # Start the update_timer method and store the reference
            self.timer_job = self.update_timer()
            # Call the on_submit function with the number of articles in a separate thread
            threading.Thread(target=self.on_submit_thread, args=(self.spinner_label, num_articles, 1)).start()
        else:
            # Show an error message if the input is not a positive integer
            ctk.messagebox.showerror("Error", "Please enter a valid number of articles.")

    def update_timer(self):
        # Calculate the elapsed time
        elapsed_time = int(time.time() - self.start_time)
        # Update the spinner label with the elapsed time
        self.spinner_label.configure(text=f"Loading... {elapsed_time} seconds")
        # Schedule the update_timer method to be called after 1 second and store the reference
        self.timer_job = self.root.after(1000, self.update_timer)

    def on_submit_thread(self, spinner_label, num_articles, num_paragraphs):
        # Call the on_submit function and get the URL of the new draft post
        post_url = on_submit(spinner_label, num_articles, num_paragraphs)
        # Stop the timer by canceling the scheduled update_timer method
        self.root.after_cancel(self.timer_job)
        # Update the spinner label to display the URL as a clickable link
        spinner_label.configure(text=post_url, cursor="hand2")
        spinner_label.bind("<Button-1>", lambda e: webbrowser.open_new(post_url))

    def show(self):
        center_window(self.root, 600, 350)  # Adjusted height from 300 to 350
        self.root.mainloop()