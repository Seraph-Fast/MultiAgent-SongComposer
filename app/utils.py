def extract_responses(responses):
    data_assistant_response = ""
    original_poet_response = ""
    composer_response = ""

    # Helper function to find content by role
    def find_content_by_name(chat_history, name):
        for message in chat_history:
            if message.get('name') == name and message.get('content'):
                return message['content']
        return ""  # Return empty string if content not found

    for result in responses:
        chat_history = result.chat_history
        
        if not data_assistant_response:
            data_assistant_response = find_content_by_name(chat_history, "data_assistant")
        
        if not original_poet_response:
            original_poet_response = find_content_by_name(chat_history, "assistant_original")
        
        if not composer_response:
            composer_response = find_content_by_name(chat_history, "composer")

    # Return the extracted responses with default fallbacks
    return {
        "data_assistant_response": data_assistant_response or "No data assistant response found.",
        "original_poet_response": original_poet_response or "No original poet response found.",
        "composer_response": composer_response or "No composer response found."
    }
