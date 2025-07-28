from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
import requests
import json
from typing import TypedDict, Dict, Any, List

app = FastAPI()

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TripRequest(BaseModel):
    destination: str
    start_date: str
    end_date: str
    preferences: str = ""

# Define state schema for LangGraph
class TripState(TypedDict):
    destination: str
    start_date: str
    end_date: str
    preferences: str
    research: Dict[str, Any]
    itinerary: List[Dict[str, Any]]
    review: Dict[str, Any]

# Simple LLM function using Hugging Face inference API
def call_huggingface_api(prompt: str) -> str:
    """Call Hugging Face inference API for text generation"""
    try:
        # Using a free inference endpoint (no auth required)
        url = "https://api-inference.huggingface.co/models/gpt2"
        headers = {"Content-Type": "application/json"}
        payload = {"inputs": prompt, "parameters": {"max_length": 300}}
        
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            # Extract generated text
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
                # If the API response is too generic, use our mock
                if len(generated_text) < 50 or "the" in generated_text.lower()[:20]:
                    return generate_mock_response(prompt)
                return generated_text
            return str(result)
        else:
            # Fallback to mock response if API fails
            return generate_mock_response(prompt)
    except Exception as e:
        print(f"API call failed: {e}")
        return generate_mock_response(prompt)

def generate_mock_response(prompt: str) -> str:
    """Generate a mock response when API is not available"""
    import re
    
    # Extract trip duration from prompt
    start_date_match = re.search(r'from (\d{4}-\d{2}-\d{2})', prompt)
    end_date_match = re.search(r'to (\d{4}-\d{2}-\d{2})', prompt)
    
    # Extract destination
    destination_match = re.search(r'trip to ([A-Za-z\s]+) from', prompt)
    destination = destination_match.group(1).strip() if destination_match else "destination"
    
    # Extract preferences
    preferences_match = re.search(r'Preferences: ([^.]*)', prompt)
    preferences = preferences_match.group(1).strip() if preferences_match else ""
    
    # Calculate trip duration
    if start_date_match and end_date_match:
        from datetime import datetime
        start_date = datetime.strptime(start_date_match.group(1), '%Y-%m-%d')
        end_date = datetime.strptime(end_date_match.group(1), '%Y-%m-%d')
        duration = (end_date - start_date).days + 1
    else:
        duration = 3  # fallback
    
    if "itinerary" in prompt.lower():
        # Generate dynamic itinerary based on duration and preferences
        itinerary = []
        for day in range(1, duration + 1):
            activities = []
            
            if day == 1:
                activities.extend([
                    f"Arrive in {destination}",
                    "Check in to hotel",
                    "Explore the city center",
                    "Try local cuisine"
                ])
            elif day == duration:
                activities.extend([
                    "Final day exploration",
                    "Visit any missed attractions",
                    "Shopping for souvenirs",
                    "Departure"
                ])
            else:
                # Middle days - vary activities based on preferences
                if "museum" in preferences.lower():
                    activities.append(f"Visit {destination} Museum")
                if "food" in preferences.lower() or "cuisine" in preferences.lower():
                    activities.append("Food tour of local restaurants")
                if "culture" in preferences.lower():
                    activities.append("Cultural site visit")
                if "nature" in preferences.lower() or "park" in preferences.lower():
                    activities.append("Visit local parks and gardens")
                if "shopping" in preferences.lower():
                    activities.append("Shopping at local markets")
                if "history" in preferences.lower():
                    activities.append("Historical site exploration")
                
                # Add some default activities if no specific preferences
                if not activities:
                    activities.extend([
                        f"Explore {destination} attractions",
                        "Local sightseeing",
                        "Evening entertainment"
                    ])
                
                # Add variety
                if day % 2 == 0:
                    activities.append("Relaxing afternoon")
                else:
                    activities.append("Adventure activities")
            
            itinerary.append({"day": day, "activities": activities})
        
        return json.dumps(itinerary)
    
    elif "review" in prompt.lower():
        suggestions = []
        if "museum" in preferences.lower() and duration > 3:
            suggestions.append("Consider adding more museum visits")
        if "food" in preferences.lower():
            suggestions.append("Include more local food experiences")
        if duration > 5:
            suggestions.append("Add day trips to nearby attractions")
        if "culture" in preferences.lower():
            suggestions.append("Include more cultural activities")
        
        return json.dumps({
            "review": f"Good {duration}-day itinerary for {destination}",
            "suggestions": suggestions if suggestions else ["Add more local experiences", "Include evening activities"]
        })
    
    else:
        # Research response
        attractions = [
            f"Famous landmarks in {destination}",
            f"Local museums and galleries",
            f"Food markets and restaurants",
            f"Cultural sites and monuments"
        ]
        
        if "museum" in preferences.lower():
            attractions.append(f"Specialized museums in {destination}")
        if "food" in preferences.lower():
            attractions.append("Local cuisine hotspots")
        
        return json.dumps({
            "attractions": attractions,
            "weather": "Mild, 20-25C, mostly sunny",
            "local_tips": f"Best time to visit {destination} attractions"
        })

def researcher_node(state: TripState) -> TripState:
    # Simulate research: add local attractions and weather
    prompt = f"Research attractions and weather for {state['destination']}"
    response = call_huggingface_api(prompt)
    
    # Parse response or use fallback
    try:
        research = json.loads(response)
    except:
        research = {
            "attractions": [
                f"Famous museum in {state['destination']}",
                f"Popular park in {state['destination']}",
                f"Local food market in {state['destination']}"
            ],
            "weather": "Mild, 20-25C, mostly sunny"
        }
    
    state = dict(state)
    state["research"] = research
    return state

def generator_node(state: TripState) -> TripState:
    user_prompt = (
        f"Plan a detailed itinerary for a trip to {state['destination']} from {state['start_date']} to {state['end_date']}. "
        f"Preferences: {state['preferences']}. "
        f"Research: {state['research']}. "
        "Return a JSON list of days, each with a list of activities."
    )
    response = call_huggingface_api(user_prompt)
    
    # Try to extract JSON from the response
    import re
    match = re.search(r'\[.*\]', response, re.DOTALL)
    if match:
        try:
            itinerary = json.loads(match.group(0))
        except Exception:
            itinerary = []
    else:
        itinerary = []
    
    state = dict(state)
    state["itinerary"] = itinerary
    return state

def critique_node(state: TripState) -> TripState:
    user_prompt = (
        f"Review this itinerary for {state['destination']}: {state['itinerary']}. "
        f"Preferences: {state['preferences']}. "
        "Suggest improvements. Return a JSON object with 'review' and 'suggestions'."
    )
    response = call_huggingface_api(user_prompt)
    
    # Try to extract JSON from the response
    import re
    match = re.search(r'\{.*\}', response, re.DOTALL)
    if match:
        try:
            review = json.loads(match.group(0))
        except Exception:
            review = {}
    else:
        review = {}
    
    state = dict(state)
    state["review"] = review
    return state

# Build LangGraph workflow with agentic steps
graph = StateGraph(TripState)
graph.add_node("researcher", researcher_node)
graph.add_node("generator", generator_node)
graph.add_node("critique", critique_node)
graph.set_entry_point("researcher")
graph.add_edge("researcher", "generator")
graph.add_edge("generator", "critique")
graph.add_edge("critique", END)
workflow = graph.compile()

@app.post("/plan_trip")
async def plan_trip(request: TripRequest):
    # Run LangGraph workflow
    state = {
        "destination": request.destination,
        "start_date": request.start_date,
        "end_date": request.end_date,
        "preferences": request.preferences,
        "research": {},
        "itinerary": [],
        "review": {}
    }
    result = workflow.invoke(state)
    itinerary = result.get("itinerary", [])
    review = result.get("review", {})
    # Format for frontend
    formatted = []
    for i, day in enumerate(itinerary, 1):
        formatted.append({"day": i, "activities": day.get("activities", day)})
    return {
        "destination": request.destination,
        "start_date": request.start_date,
        "end_date": request.end_date,
        "preferences": request.preferences,
        "itinerary": formatted,
        "review": review
    }
