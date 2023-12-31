# settings_window.py content
import customtkinter as ctk
import tkinter.messagebox as msgbox  # Correct import for messagebox
from utils import is_valid_api_key, is_valid_url, load_settings, save_settings
import webbrowser

class SettingsWindow:
    def __init__(self):
        self.settings_root = ctk.CTkToplevel()
        self.settings_root.title("Settings")
        self.settings_root.geometry('500x400')  # Adjust the size as needed
        self.create_widgets()

    def create_widgets(self):
        # Instructional text with link to OpenAI API keys page
        instructional_text = "To use this application, you need an OpenAI API key. You can obtain one from "
        link_text = "OpenAI API keys page"
        instructional_label = ctk.CTkLabel(self.settings_root, text=instructional_text, font=("Lato", 10))
        instructional_label.pack(pady=(10, 0))
        link_label = ctk.CTkLabel(self.settings_root, text=link_text, font=("Lato", 10, 'underline'), text_color="blue", cursor="hand2")
        link_label.pack(pady=(0, 10))
        link_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://platform.openai.com/api-keys"))

        # OpenAI API Settings
        openai_api_label = ctk.CTkLabel(self.settings_root, text="Enter your OpenAI API key (required):", font=("Lato", 10))
        openai_api_label.pack(pady=(10, 0))
        self.openai_api_entry = ctk.CTkEntry(self.settings_root, width=300, placeholder_text="Enter your OpenAI API key here. You can obtain it from your OpenAI account.", font=("Lato", 10))
        self.openai_api_entry.pack(pady=(0, 10))

        # WordPress Settings
        wordpress_url_label = ctk.CTkLabel(self.settings_root, text="Enter your WordPress site URL (required):", font=("Lato", 10))
        wordpress_url_label.pack(pady=(10, 0))
        self.wordpress_url_entry = ctk.CTkEntry(self.settings_root, width=300, placeholder_text="Enter the URL of your WordPress site here.", font=("Lato", 10))
        self.wordpress_url_entry.pack(pady=(0, 10))

        wordpress_username_label = ctk.CTkLabel(self.settings_root, text="Enter your WordPress username (required):", font=("Lato", 10))
        wordpress_username_label.pack(pady=(10, 0))
        self.wordpress_username_entry = ctk.CTkEntry(self.settings_root, width=300, placeholder_text="Enter your WordPress username here.", font=("Lato", 10))
        self.wordpress_username_entry.pack(pady=(0, 10))

        wordpress_password_label = ctk.CTkLabel(self.settings_root, text="Enter your WordPress password (required):", font=("Lato", 10))
        wordpress_password_label.pack(pady=(10, 0))
        self.wordpress_password_entry = ctk.CTkEntry(self.settings_root, width=300, show="*", placeholder_text="Enter your WordPress password here.", font=("Lato", 10))
        self.wordpress_password_entry.pack(pady=(0, 10))

        # Article Preview Feature Checkbox
        self.article_preview_checkbox = ctk.CTkCheckBox(self.settings_root, text="Enable article preview and feedback", font=("Lato", 10))
        self.article_preview_checkbox.pack(pady=(0, 10))

        # Load existing settings and populate the fields
        existing_settings = load_settings()
        if existing_settings:
            self.openai_api_entry.insert(0, existing_settings.get('OPENAI_API_KEY', ''))
            self.wordpress_url_entry.insert(0, existing_settings.get('WORDPRESS_URL', ''))
            self.wordpress_username_entry.insert(0, existing_settings.get('WORDPRESS_USERNAME', ''))
            self.wordpress_password_entry.insert(0, existing_settings.get('WORDPRESS_PASSWORD', ''))
            if existing_settings.get('ARTICLE_PREVIEW', False):
                self.article_preview_checkbox.select()
            else:
                self.article_preview_checkbox.deselect()

        # Save Settings Button
        save_button = ctk.CTkButton(self.settings_root, text="Save Settings", command=self.save_settings, corner_radius=10, fg_color="#00A2FF", hover_color="#007ACC", font=("Lato", 10))
        save_button.pack(pady=10)

    def save_settings(self):
        openai_api_key = self.openai_api_entry.get()
        wordpress_url = self.wordpress_url_entry.get()
        wordpress_username = self.wordpress_username_entry.get()
        wordpress_password = self.wordpress_password_entry.get()
        article_preview = self.article_preview_checkbox.get()
        try:
            # Call the save_settings function from utils.py
            save_settings(openai_api_key, wordpress_url, wordpress_username, wordpress_password, article_preview)
            # Show a confirmation message using standard tkinter messagebox
            msgbox.showinfo("Settings Saved", "Your settings have been saved successfully.")
        except Exception as e:
            # Show an error message using standard tkinter messagebox
            msgbox.showerror("Error", f"An error occurred while saving settings: {e}")

    def center_window(self, width=500, height=500):  # Adjust the size as needed
        # Get screen width and height
        screen_width = self.settings_root.winfo_screenwidth()
        screen_height = self.settings_root.winfo_screenheight()
        # Calculate position coordinates
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.settings_root.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def show(self):
        self.center_window()
        self.settings_root.attributes('-topmost', True)
        self.settings_root.update()
        self.settings_root.attributes('-topmost', False)
        self.settings_root.mainloop()