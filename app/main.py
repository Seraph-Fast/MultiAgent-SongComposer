# main.py
from fastapi import Depends, FastAPI, Query
from typing import Dict
from datetime import datetime
from app.agents import initialize_agents, initiate_agents
from app.config import Settings
from app.logging import log_interaction  # Import the logging function

# Initialize FastAPI
app = FastAPI()
settings = Settings()

# Initialize agents at startup
@app.on_event("startup")
def startup_event():
    initialize_agents(settings.MODEL_NAME, settings.BASE_URL)

@app.get("/generate_poem")
async def generate_poem(
    poet: str = Query(..., description="The name of the poet whose style you want the poem to be in")
) -> Dict:
    """
    Generate a poem in the specified poet's style using the agents.
    
    Args:
    - poet (str): The poet's name to use as a style reference.
    
    Returns:
    - Dict: A dictionary containing the generated compositions.
    """
    try:
        # Record start time
        start_datetime = datetime.now()
        
        # Run the main query
        responses = initiate_agents(poet)
        print("responses: \n", responses)
        # Record end time
        end_datetime = datetime.now()
        
        # Calculate query time
        start_time = start_datetime.time()
        end_time = end_datetime.time()
        query_time = end_datetime - start_datetime
        
        # Extract responses from each agent
        data_assistant_response = responses[0].chat_history[-1]["content"]
        original_poet_response = responses[1].chat_history[-1]["content"]
        composer_response = responses[2].chat_history[-1]["content"]
        
        # Log interaction in the database
        log_interaction(
            date=start_datetime.date(),
            start_time=start_time,
            end_time=end_time,
            query_time=query_time,
            user_proxy_response=poet,  # Assuming user input as "user_proxy_response"
            data_assistant_response=data_assistant_response,
            original_poet_response=original_poet_response,
            composer_response=composer_response
        )
        
        # Return formatted results
        return {
            "poet": poet,
            "data_response": responses[0],
            "original_response": responses[1],
            "final_composition": responses[2]
        }
    except Exception as e:
        return {"error": str(e)}
