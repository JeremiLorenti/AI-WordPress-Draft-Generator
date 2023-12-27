# main_window.py content
import customtkinter as ctk
from settings_window import SettingsWindow
from newPost import on_submit
import threading

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
        self.root.geometry('400x300+50+50')
        self.create_widgets()

    def create_widgets(self):
        # Settings Button with Gear Icon
        gear_icon = "⚙️"  # Unicode character for a gear icon
        settings_button = ctk.CTkButton(self.root, text=gear_icon, width=40, height=40, corner_radius=10,
                                        command=self.open_settings_window, fg_color="gray")
        settings_button.pack(side='top', anchor='ne', padx=10, pady=10)

        label = ctk.CTkLabel(self.root, text="Welcome to AI Draft Post Creator", font=('Lato', 20, 'bold'))
        label.pack(pady=20)

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
        self.spinner_label.pack(side='left', pady=10, padx=10)

    def open_settings_window(self):
        settings_window = SettingsWindow()
        settings_window.show()

    def create_new_draft(self):
        num_articles = self.counter.get()
        if num_articles.isdigit() and int(num_articles) > 0:
            # Show loading indicator
            self.spinner_label.configure(text="Loading...")
            # Call the on_submit function with the number of articles in a separate thread
            threading.Thread(target=on_submit, args=(self.spinner_label, num_articles, 1)).start()
        else:
            # Show an error message if the input is not a positive integer
            ctk.messagebox.showerror("Error", "Please enter a valid number of articles.")

    def show(self):
        center_window(self.root, 600, 300)  # Assuming the window size is 400x300
        self.root.mainloop()