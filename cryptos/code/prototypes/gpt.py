import openai
import keyboard

# Set up the OpenAI API key and model ID
openai.api_key = "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"
model_id = "text-davinci-003"

# Function to send a prompt to the GPT-3 API and get a response
def generate_response(prompt):
    response = openai.Completion.create(
        engine=model_id,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0,
    )
    return response.choices[0].text.strip()

# Function to listen for a key press and get user input
def listen_for_input():
    input_text = ""
    while True:
        event = keyboard.read_event()
        if event.event_type == "down" and event.name == "enter":
            break
        elif event.event_type == "down" and event.name == "backspace":
            input_text = input_text[:-1]
        elif event.event_type == "down" and len(event.name) == 1:
            input_text += event.name
        print("\r>> " + input_text + "_"*10, end="")
    return input_text.strip()

# Main program loop
while True:
    print("\nPress Enter to ask a question, or Ctrl+C to quit.")
    try:
        keyboard.wait("enter")
        print("You asked:")
        prompt = listen_for_input()
        response = generate_response(prompt)
        print("\nChatGPT says:")
        print(response)
    except KeyboardInterrupt:
        break
