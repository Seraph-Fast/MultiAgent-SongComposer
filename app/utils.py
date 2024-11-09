import re

def extract_responses(responses):
    data_assistant_response = None
    original_poet_response = None
    composer_response = None

    for chat_result in responses:
        chat_history = chat_result.chat_history
        agent_name = None
        agent_response = ''

        for message in chat_history:
            if message['role'] == 'user':
                agent_name = message['name']
                content = message['content']
                # Extract content between <BEGIN_POEM> and <END_POEM>
                match = re.search(r'<BEGIN_POEM>(.*?)<END_POEM>', content, re.DOTALL)
                if match:
                    agent_response = match.group(1).strip()
                else:
                    agent_response = content.strip()
                break  

        if agent_name == 'data_assistant':
            data_assistant_response = agent_response
        elif agent_name == 'assistant_original':
            original_poet_response = agent_response
        elif agent_name == 'composer':
            composer_response = agent_response

    return {
        "data_assistant_response": data_assistant_response or "No data assistant response found.",
        "original_poet_response": original_poet_response or "No original poet response found.",
        "composer_response": composer_response or "No composer response found."
    }
