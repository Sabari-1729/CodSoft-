def simple_chatbot(user_input):
    """A simple chatbot that responds based on predefined rules."""

    user_input = user_input.lower()  # Convert to lowercase for easier matching

    if "hello" in user_input or "hi" in user_input or "hey" in user_input:
        return "Hello! How can I help you today?"

    elif "how are you" in user_input:
        return "I'm doing well, thank you! How about you?"

    elif "what is your name" in user_input:
        return "I'm a simple chatbot."

    elif "bye" in user_input or "goodbye" in user_input:
        return "Goodbye! Have a great day!"

    elif "help" in user_input:
        return "I can respond to greetings, questions about my name, and basic pleasantries."

    elif "weather" in user_input:
        return "I'm sorry, I cannot provide real-time weather information."

    elif "time" in user_input:
        return "I'm sorry, I cannot provide the current time."

    elif "thank you" in user_input or "thanks" in user_input:
        return "You're welcome!"

    else:
        return "I'm not sure I understand. Could you please rephrase your question?"

# Example usage
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break
    response = simple_chatbot(user_input)
    print("Chatbot:", response)