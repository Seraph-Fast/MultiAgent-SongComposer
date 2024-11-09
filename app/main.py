from fastapi import FastAPI, Query, Depends, Form
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from typing import Dict
from datetime import datetime
from app.agents import initialize_agents, initiate_agents
from app.config import Settings
from app.logging import log_interaction, get_logs  
from app.utils import extract_responses

# Initialize FastAPI
app = FastAPI()
settings = Settings()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Initialize agents at startup
@app.on_event("startup")
def startup_event():
    initialize_agents(settings.MODEL_NAME, settings.BASE_URL)

# Home page route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Log page route to view logs
@app.get("/logs", response_class=HTMLResponse)
async def view_logs(request: Request):
    logs = get_logs()  # Fetch logs from the database using get_logs
    return templates.TemplateResponse("logs.html", {"request": request, "logs": logs})

# Generate poem route (handles both web form and API requests)
@app.post("/generate_poem")
async def generate_poem(
    request: Request, 
    poet: str = Form(..., description="The name of the poet whose style you want the poem to be in")
):
    try:
        # Record start time
        start_datetime = datetime.now()

        # Run the main query using the agents
        responses = initiate_agents(poet)
        #print("responses: \n",responses)
        # Record end time
        end_datetime = datetime.now()

        # Calculate query time
        start_time = start_datetime.time()
        end_time = end_datetime.time()
        query_time = end_datetime - start_datetime

        extracted_responses = extract_responses(responses)
        
        # Extract responses from each agent
        data_assistant_response = extracted_responses["data_assistant_response"]
        original_poet_response = extracted_responses["original_poet_response"]
        composer_response = extracted_responses["composer_response"]
        
        # Log interaction in the database
        log_interaction(
            date=start_datetime.date(),
            start_time=start_time,
            end_time=end_time,
            query_time=query_time,
            user_proxy_response=poet,
            data_assistant_response=data_assistant_response,
            original_poet_response=original_poet_response,
            composer_response=composer_response
        )

        # Return JSON response for AJAX requests
        if request.headers.get("accept") == "application/json":
            return JSONResponse({
                "poet": poet,
                "data_response": data_assistant_response,
                "original_response": original_poet_response,
                "final_composition": composer_response
            })
        
        # Otherwise, return the HTML template (for browser form submission)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "poet": poet,
            "data_response": data_assistant_response,
            "original_response": original_poet_response,
            "final_composition": composer_response
        })
     
    except Exception as e:
        print(str(e))
        return {"error": str(e)}
