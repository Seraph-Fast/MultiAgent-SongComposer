import autogen
import os

#global variables for agents
data_assistant = None
assistant_original_poem = None
assistant_composer = None
user_proxy = None

def initialize_agents(MODEL_NAME, BASE_URL):
    global data_assistant, assistant_original_poem, assistant_composer, user_proxy

    # Configuration for the LLM
    config_list = [
        {
            "model": MODEL_NAME,
            "base_url": BASE_URL,
            "api_key": "ollama",
        }
    ]

    llm_config = {
        "config_list": config_list,
        # "cache_seed" : 0,
        # "temperature": 0,
        # "timeout": 120,
    }

    # agents
    data_assistant = autogen.AssistantAgent(
        name="data_assistant",
        system_message="You are an assistant agent who provides an original poem from the specified poet. Return 'TERMINATE' when the task is done.",
        llm_config=llm_config,
        max_consecutive_auto_reply=1
    )

    assistant_original_poem = autogen.AssistantAgent(
        name="assistant_original",
        system_message="You are an assistant agent who writes an original poem in your own style. Return 'TERMINATE' when the task is done.",
        llm_config=llm_config,
        max_consecutive_auto_reply=1
    )

    assistant_composer = autogen.AssistantAgent(
        name="composer",
        system_message="You are a composer agent who creates a new composition in the specified poet's style by combining elements from the original and the unique poem. Return 'TERMINATE' when the task is done.",
        llm_config=llm_config,
        max_consecutive_auto_reply=1
    )

    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        code_execution_config=False
    )

def initiate_agents(user_prompt: str):
    # Sequential communication of the agents
    autogen.runtime_logging.start(config={"dbname": "logs.db"})
    responses = user_proxy.initiate_chats(
        [
            {
                "recipient": data_assistant,
                "message": f"Provide a composition in the style of {user_prompt}. Give Only 2 stanza of the poem",
                #"clear_history": True,
                "silent": False,
                #"summary_method": "reflection_with_llm"
            },
            {
                "recipient": assistant_original_poem,
                "message": "Write an original poem in your own style. Give only 2 stanza of original poem",
                #"clear_history": True,
                "silent": False,
                #"summary_method": "reflection_with_llm"
            },
            {
                "recipient": assistant_composer,
                "message": f"Give 2 stanza using the {user_prompt} composition and the original poem, create a new composition in the style of {user_prompt}.",
                #"clear_history": True,
                "silent": False,
                #"summary_method": "reflection_with_llm"
            }
        ]
    )
    autogen.runtime_logging.stop()

    return responses

__all__ = ["initialize_agents", "initiate_agents"]
