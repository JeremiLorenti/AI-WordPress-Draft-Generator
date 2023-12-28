# AI Draft Post Creator

## *VERY MUCH A WORK IN PROGRESS*

AI Draft Post Creator is a desktop application designed to streamline the process of creating draft posts for your WordPress blog using the power of AI. The application provides a user-friendly interface to generate draft posts based on the number of articles and paragraphs specified by the user.

## Features

- **Generate Draft Posts**: Easily create draft posts for your WordPress blog with AI assistance.
- **WordPress Integration**: Directly connect to your WordPress site to manage categories and create drafts.
- **Customizable Settings**: Configure your OpenAI and WordPress settings through a dedicated settings window.
- **User-Friendly Interface**: Simple and intuitive interface for seamless operation.

## Installation

To install AI Draft Post Creator, follow these steps:

1. Ensure you have Python installed on your system.
2. Clone the repository or download the source code.
3. Install the required dependencies by running `pip install -r requirements.txt` in the project directory.
4. Launch the application by running `python app.py`.

## Usage

Upon launching AI Draft Post Creator, you will be greeted with the main window where you can:

- Access the settings window to enter your OpenAI API key and WordPress credentials.
- Specify the number of articles you wish to generate.
- Click the "Create New Draft" button to initiate the draft post creation process.

The application will then communicate with the OpenAI API to generate content and create a draft post on your WordPress site.

## Configuration

Before using the application to create draft posts, you must configure your OpenAI and WordPress settings:

1. Click the settings button (gear icon) in the top right corner of the main window.
2. Enter your OpenAI API key and WordPress site URL, username, and password.
3. Save your settings.

## Dependencies

- `customtkinter`: For creating the custom user interface.
- `requests`: For making HTTP requests to the WordPress API.
- `base64`: For encoding authentication credentials.
- `json`: For parsing and saving settings.
- `tkinter`: For standard GUI elements and message boxes.
- `threading`: For running tasks in separate threads to keep the UI responsive.
- `webbrowser`: For opening URLs in the default web browser.

## Contributing

Contributions to AI Draft Post Creator are welcome. Please feel free to fork the repository, make changes, and submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the GPT models used to generate content.
- The WordPress REST API for enabling programmatic access to WordPress site management.

## Contact

For any inquiries or issues, please open an issue on the GitHub repository issue tracker.

---

Enjoy creating draft posts with ease using AI Draft Post Creator!