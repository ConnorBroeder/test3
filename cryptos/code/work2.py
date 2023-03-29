import openai
import speech_recognition as sr
import PySimpleGUI as sg
import subprocess
# Set up OpenAI API key
api_key = "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"
openai.api_key = api_key

# Function to send a message to the OpenAI chatbot model and return its response
def send_message(message_log):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        messages=message_log,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=3800,        # The maximum number of tokens (words or subwords) in the generated response
        stop=None,              # The stopping sequence for the generated response, if any (not used here)
        temperature=0.7,        # The "creativity" of the generated response (higher temperature = more creative)
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content


# Main function that runs the chatbot
def main():
    # Initialize the conversation history with a message from the chatbot
    message_log = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    # Use the default system microphone as audio source
    r = sr.Recognizer()

    # Start a loop that runs until the user types "quit"
    while True:
        # Get the user's input using speech recognition
        with sr.Microphone() as source:
            print("Press Enter to start recording audio...")
            input()  # press Enter to start recording
            print("Recording audio...")
            audio = r.listen(source, phrase_time_limit=5)  # stop recording after 5 seconds of silence

        try:
            recognized_text = r.recognize_google(audio)  # use Google Speech Recognition API
            print(f"Recognized speech: {recognized_text}")

            # Add the user's speech to the conversation history
            message_log.append({"role": "user", "content": recognized_text})

            # Send the conversation history to the chatbot and get its response
            response = send_message(message_log)

            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})
            print(f"AI assistant: {response}")

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

        # If the user types "quit", end the loop and print a goodbye message
        if recognized_text.lower() == "quit":
            print("Goodbye!")
            break


# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
    main()