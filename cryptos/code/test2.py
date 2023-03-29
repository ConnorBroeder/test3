import pygame
import sys
import math
import time

pygame.init()

# Settings
size = width, height = 400, 400
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("AI Smartwatch Tst")
font = pygame.font.Font(None, 100)
background_color = (30, 30, 30)
text_color = (255, 255, 255)

# App class
class App:
    def __init__(self, icon, action=None):
        self.icon = icon
        if action is None:
            self.action = lambda: None  # Default action that does nothing
        else:
            self.action = action

    def execute_action(self):
        self.action()
        
# Menu class
class Menu:
    def __init__(self, apps):
        self.apps = apps
        self.display_microphone_button = False
        self.microphone_pressed = False

    def draw(self, screen):
        if self.display_microphone_button:
            # Display microphone button
            microphone_icon_size = 80
            microphone_icon_pos = (width // 2 - microphone_icon_size // 2, height // 2 - microphone_icon_size // 2)
            microphone_icon_rect = pygame.Rect(microphone_icon_pos, (microphone_icon_size, microphone_icon_size))
            microphone_icon.set_alpha(128)  # Set transparency to 50%
            screen.blit(microphone_icon, microphone_icon_pos)

            # Display microphone indicator if button is pressed
            if self.microphone_pressed:
                microphone_indicator_size = 20
                microphone_indicator_pos = (microphone_icon_pos[0] + microphone_icon_size - microphone_indicator_size // 2, microphone_icon_pos[1] - microphone_indicator_size // 2)
                microphone_indicator_rect = pygame.Rect(microphone_indicator_pos, (microphone_indicator_size, microphone_indicator_size))
                pygame.draw.circle(screen, (255, 0, 0), microphone_indicator_pos, microphone_indicator_size // 2)
        else:
            # Draw the app icons
            for app, icon_pos in self.apps:
                screen.blit(app.icon, icon_pos)

    def handle_click(self, mouse_pos):
        if self.display_microphone_button:
            # Check if mouse click is inside the microphone button
            microphone_icon_size = 80
            microphone_icon_pos = (width // 2 - microphone_icon_size // 2, height // 2 - microphone_icon_size // 2)
            microphone_icon_rect = pygame.Rect(microphone_icon_pos, (microphone_icon_size, microphone_icon_size))
            if microphone_icon_rect.collidepoint(mouse_pos):
                print("Microphone pressed")
                self.microphone_pressed = True
                # Perform functionality code when microphone button is pressed
                answer = "42"  # Replace with your functionality code
                text = font.render(answer, True, text_color)
                text_rect = text.get_rect(center=(width // 2, height // 2))
                screen.blit(text, text_rect)
        else:
            # Check if mouse click is inside an app icon
            for app, icon_pos in self.apps:
                distance = math.sqrt((mouse_pos[0] - icon_pos[0] - icon_size // 2) ** 2 + (mouse_pos[1] - icon_pos[1] - icon_size // 2) ** 2)
                if distance <= icon_size // 2:
                    app.execute_action()

    def handle_release(self, mouse_pos):
        if self.microphone_pressed:
            self.microphone_pressed = False
            
            
# Clock class
class Clock:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def draw(self, screen):
        current_time = time.strftime("%H:%M")
        text = font.render(current_time, True, text_color)
        text_rect = text.get_rect(center=self.center)
        pygame.draw.circle(screen, text_color, self.center, self.radius, 5)
        screen.blit(text, text_rect)

# SmartwatchDisplay class
class SmartwatchDisplay:
    def __init__(self, screen, clock, menu):
        self.screen = screen
        self.clock = clock
        self.menu = menu
        self.display_clock = True

    def draw(self):
        self.screen.fill(background_color)
        if self.display_clock:
            self.clock.draw(self.screen)
        else:
            self.menu.draw(self.screen)
        pygame.display.flip()

    def handle_click(self, mouse_pos):
        if self.display_clock:
            self.display_clock = False
        else:
            self.menu.handle_click(mouse_pos)

# Functions
def settings_action():
    if menu.display_microphone_button:
        print("Microphone pressed")
    menu.display_microphone_button = True


def settings_action():
    if menu.display_microphone_button:
        print("Microphone pressed")
    menu.display_microphone_button = True

    # Connect to WLAN functionality
    ssid = input("Enter WLAN SSID: ")
    password = input("Enter WLAN password: ")

    # Execute shell command to configure wireless network
    subprocess.run(["nmcli", "dev", "wifi", "connect", ssid, "password", password])

# Load menu icons
app_timer_icon = pygame.image.load("timer_icon.png").convert_alpha()
app_settings_icon = pygame.image.load("settings_icon.png").convert_alpha()
app_music_icon = pygame.image.load("music_icon.png").convert_alpha()  # New app icon
microphone_icon = pygame.image.load("microphone.png").convert_alpha()
icon_size = 80
timer_icon = pygame.transform.scale(app_timer_icon, (icon_size, icon_size))
settings_icon = pygame.transform.scale(app_settings_icon, (icon_size, icon_size))
music_icon = pygame.transform.scale(app_music_icon, (icon_size, icon_size))  # New app icon
microphone_icon = pygame.transform.scale(microphone_icon, (icon_size, icon_size))

timer_icon_pos = (width // 2 - icon_size - 10, height // 2 - icon_size - 10)
settings_icon_pos = (width // 2 + 10, height // 2 - icon_size - 10)
music_icon_pos = (width // 2 - icon_size - 10, height // 2 + 10)  # New app icon position

# Create apps, menu, clock, and display
app_settings = App(settings_icon, settings_action)
app_timer = App(timer_icon)
app_music = App(music_icon)  # New app without function
apps = [(app_settings, settings_icon_pos), (app_music, music_icon_pos), (app_timer, timer_icon_pos)]  # Add new app to the list

menu = Menu(apps)
clock = Clock((width // 2, height // 2), 190)
display = SmartwatchDisplay(screen, clock, menu)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
            mouse_pos = pygame.mouse.get_pos()
            display.handle_click(mouse_pos)

        elif event.type == pygame.KEYDOWN:
            # Go back to the clock on Num5 press
            if event.key == pygame.K_KP5:
                display.display_clock = True
                menu.display_microphone_button = False

    display.draw()