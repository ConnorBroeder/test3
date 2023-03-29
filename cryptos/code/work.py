import pygame
import sys
import math
import time
import PySimpleGUI as sg
import openai
import speech_recognition as sr

# Initialize Pygame
pygame.init()

# Set up the circular display
size = width, height = 400, 400
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("AI Smartwatch Tst")
font = pygame.font.Font(None, 100)
background_color = (30, 30, 30)
text_color = (255, 255, 255)

# Load menu icons
app_clock_icon = pygame.image.load("clock_icon.png").convert_alpha()
app_settings_icon = pygame.image.load("settings_icon.png").convert_alpha()
microphone_icon = pygame.image.load("microphone.png").convert_alpha()
icon_size = 80
clock_icon = pygame.transform.scale(app_clock_icon, (icon_size, icon_size))
settings_icon = pygame.transform.scale(app_settings_icon, (icon_size, icon_size))
microphone_icon = pygame.transform.scale(microphone_icon, (icon_size, icon_size))

clock_icon_pos = (width // 2 - icon_size - 10, height // 2 - icon_size - 10)
settings_icon_pos = (width // 2 + 10, height // 2 - icon_size - 10)

# Set up the clock loop
display_clock = True
clock_radius = 190
clock_center = (width // 2, height // 2)

# Define the list of app icons and their positions
app_icons = [(clock_icon, clock_icon_pos), (settings_icon, settings_icon_pos)]

# Set up a flag to track whether the microphone button is being displayed and if it is currently listening
show_microphone_button = False
listening = False

# Set up OpenAI API key
api_key = "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"
openai.api_key = api_key

# Function to send a message to the OpenAI chatbot model and return its response
def send_message(message_log):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.Completion.create(
        engine="davinci",
        prompt=message_log,
        max_tokens=3800,
        temperature=0.7,
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].text

# Main function that runs the chatbot
def main():
    # Initialize the conversation history with a message from the chatbot
    message_log = "You are a helpful assistant."

    # Use the default system microphone as audio source
    r = sr.Recognizer()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN: 
    #Switch between Ctrl+C or clicks/taps the "x" button to close the window
                while True: 
                    try: 
                        with sr.Microphone() as source:
                            r.adjust_for_ambient_noise(source) 
                            sg.popup_quick_message("Listening...")
                            audio = r.listen(source)
                            ser_message = r.recognize_google(audio)
                            # Add the user's message to the conversation history
                            message_log.append({"role": "user", "content": user_message})
                            # Send the user's message to the chatbot and add its response to the conversation history
                            chatbot_message = send_message(message_log)
                            message_log.append({"role": "system", "content": chatbot_message})
                            # Display the chatbot's response in the terminal
                            print("AI: " + chatbot_message)
                            # Handle Ctrl+C and window close events
                    except (KeyboardInterrupt, SystemExit, pygame.QUIT): 
                        break
                        pygame.quit()
                        sys.exit()
                        if name == "main":
                            main()
