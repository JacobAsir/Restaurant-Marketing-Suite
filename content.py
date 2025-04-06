import os
import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
import requests

# Set API keys
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")  # Add your Serper API Key

# Initialize the Groq LLaMA model
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="groq/llama-3.3-70b-versatile"
)

def get_real_time_trends(location):
    """Fetches real-time news or trending topics for the given location."""
    url = "https://serper-api.com/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    params = {"q": f"{location} trending food news", "num": 5}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return [item["title"] for item in response.json().get("organic", [])]
    return ["No trending topics found"]

# Define the AI agent
content_agent = Agent(
    role="Content Strategist",
    goal="Provide engaging content suggestions for restaurant owners based on trends.",
    backstory="An AI-powered marketing assistant that helps restaurant owners generate content ideas based on real-time trends.",
    llm=llm,
    verbose=True
)

# Define the task for the agent
def generate_content_suggestions(location):
    trends = get_real_time_trends(location)
    prompt = f"Generate engaging content ideas based on these trends: {trends}"
    return llm(prompt)

# Move the task definition inside the button click handler
content_task = Task(
    description="Analyze local food trends and provide content suggestions.",
    agent=content_agent,
    expected_output="A list of 5-10 engaging content ideas for restaurant marketing based on current trends"
)

# Create a Crew with the agent and task
crew = Crew(
    agents=[content_agent],
    tasks=[content_task],
    process=Process.sequential
)

# Streamlit UI
st.title("AI Content Suggestion Agent for Restaurants")
location = st.text_input("Enter your city or location:")

if st.button("Get Content Suggestions"):
    if location:
        # Update task description with current location
        content_task.description = f"Analyze local food trends in {location} and provide content suggestions."
        
        result = crew.kickoff()
        
        # Get today's date
        from datetime import datetime
        today = datetime.now().strftime("%B %d, %Y")
        
        # Extract content from the result
        if hasattr(result, 'raw') and result.raw:
            content = result.raw
            if isinstance(content, str):
                if content.startswith('"') and content.endswith('"'):
                    content = content[1:-1]
                content = content.replace('\\"', '"').replace('\\n', '\n')
            
            st.markdown(f"## Content Suggestions for {today}")
            st.markdown(content)
        else:
            st.markdown(f"## Content Suggestions for {today}")
            st.markdown(str(result))
    else:
        st.warning("Please enter a location to get content suggestions.")
