import pygame
import sys
import math
import time
import openai
import pygame_textinput
from gtts import gTTS
from io import BytesIO
from pygame import mixer

#(Add your OpenAI API key here)
openai.api_key = "YOUR_OPENAI_API_KEY"
# Initialize Pygame
pygame.init()
mixer.init()

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

# Set up a flag to track whether the microphone button is being displayed
show_microphone_button = False

# Add the text input field
text_input = pygame_textinput.TextInput(font_family="Arial", font_size=24, antialias=True)

# Add a flag to track the text input mode
text_input_mode = False

# Add a variable to store the GPT-3 response
gpt_response = None

while True: 
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
            # Switch between clock and menu on click/touch
            if display_clock:
                display_clock = False
            else:
                mouse_pos = pygame.mouse.get_pos()
                for icon, icon_pos in app_icons:
                    distance = math.sqrt((mouse_pos[0] - icon_pos[0] - icon_size // 2) ** 2 + (mouse_pos[1] - icon_pos[1] - icon_size // 2) ** 2)
                    if distance <= icon_size // 2:
                        # Perform action for clicked icon
                        if icon == settings_icon:
                            # Display microphone button
                            show_microphone_button = True

        elif event.type == pygame.KEYDOWN:
            # Go back to the clock on Num5 press
            if event.key == pygame.K_KP5:
                display_clock = True
                show_microphone_button = False

    screen.fill(background_color)

    if display_clock:
        current_time = time.strftime("%H:%M")
        text = font.render(current_time, True, text_color)
        text_rect = text.get_rect(center=clock_center)
        pygame.draw.circle(screen, text_color, clock_center, clock_radius, 5)
        screen.blit(text, text_rect)
    else:
        # Draw the circular menu background
        pygame.draw.circle(screen, text_color, clock_center, clock_radius, 5)

        if show_microphone_button:
            # Display microphone button
            microphone_button_pos = (width // 2 - icon_size // 2, height // 2 - icon_size // 2)
            screen.blit(microphone_icon, microphone_button_pos)
        else:
            # Draw the app icons
            for icon, icon_pos in app_icons:
                screen.blit(icon, icon_pos)

        if event.type == pygame.KEYDOWN:
            # Go back to the clock on Escape press
            if event.key == pygame.K_ESCAPE:
                display_clock = True
                show_microphone_button = False
                text_input_mode = False
   
   
   
    if text_input_mode:
        # Update and draw the text input field
        text_input.update(pygame.event.get())
        screen.blit(text_input.get_surface(), (50, height - 50))

        # Check if the user pressed Enter
        if text_input.get_enter_pressed():
            # Send the question to GPT-3.5 Turbo API
            question = text_input.get_text()
            prompt = f"{question}{{response}}"
            response = openai.Completion.create(
                engine="gpt-3.5-turbo",
                prompt=prompt,
                max_tokens=64,
                n=1,
                stop="{response}",
                temperature=0.5,
            )

            # Get and display the response
            gpt_response = response.choices[0].text.strip()
            print(f"Question: {question}")
            print(f"Answer: {gpt_response}")

            # Convert the response to speech
            tts = gTTS(text=gpt_response, lang="en")
            with BytesIO() as f:
                tts.save(f)
                f.seek(0)
                mixer.music.load(f)
                mixer.music.play()

            # Clear the text input field
            text_input.clear_text()
            text_input.set_enter_pressed(False)

    pygame.display.flip()