
import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
import os

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize the Groq LLaMA model
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="groq/llama-3.3-70b-versatile"
)

def create_agents_and_tasks(user_topic):
    # Define Restaurant Knowledge Agent
    restaurant_knowledge_agent = Agent(
        role="Restaurant Knowledge Agent",
        goal="Store detailed information about the restaurant and provide accurate details when requested.",
        backstory="""You are the knowledge keeper for Ceri-Mer Restaurant, a vibrant and welcoming dining spot known for its delicious international cuisine, cozy ambiance, and friendly atmosphere.
        You provide this information clearly and consistently to other agents to ensure all marketing content accurately reflects the restaurant's identity.
        
        Restaurant Details:
        Name: Ceri-Mer Restaurant
        Address: 123 Culinary Street, Foodville
        Phone: (555) 123-4567
        Email: info@ceri-mer.com.
        
        Operating Hours:
        - Monday to Thursday: 11am - 10pm
        - Friday to Saturday: 11am - 11pm
        - Sunday: 10am - 9pm
        
        Restaurant Theme:
        Ceri-Mer Restaurant offers a warm, inviting atmosphere inspired by a fusion of modern elegance and rustic charm. 
        The decor features cozy lighting, comfortable seating, and tasteful accents that create a welcoming environment perfect for family gatherings, romantic dinners, and casual meet-ups. 
        The restaurant prides itself on exceptional customer service, fresh ingredients, and a diverse menu that caters to various tastes and dietary preferences.""",
        llm=llm,
        verbose=True
    )

    content_creator_agent = Agent(
        role="Content Creator Agent",
        goal="Generate engaging, authentic, and creative marketing content for Instagram and Facebook posts based on restaurant details provided.",
        backstory="""You specialize in creating captivating social media posts, promotional content, and storytelling that resonates with the restaurant's target audience. You collaborate closely with the Restaurant Knowledge Agent to ensure accuracy and authenticity.
        
        When creating social media posts, always follow these formatting guidelines:
        1. Start with an attention-grabbing headline with relevant emojis
        2. Break content into short, readable paragraphs
        3. Use appropriate emojis throughout the text to enhance engagement
        4. Include a clear call-to-action
        5. End with relevant hashtags, grouped and properly spaced
        6. Ensure the post is visually appealing with proper spacing and line breaks
        7. Keep the tone friendly and inviting""",
        llm=llm,
        verbose=True
    )

    # Modified tasks to incorporate user's topic
    restaurant_task = Task(
        description=f"""Provide comprehensive details about the restaurant focusing on {user_topic if user_topic else 'general information including cuisine type, popular menu items, special promotions, events, and ambiance'}.""",
        agent=restaurant_knowledge_agent,
        expected_output="A detailed description of the restaurant including specific focus points and relevant information."
    )

    content_task = Task(
        description=f"""Using restaurant details provided, craft an engaging Instagram and Facebook post about {user_topic if user_topic else "today's special dishes and promotions"}. Ensure it's appealing and aligned with the restaurant's brand voice.""",
        agent=content_creator_agent,
        context=[restaurant_task],
        expected_output="A creative, engaging, and ready-to-post social media caption suitable for Instagram and Facebook."
    )

    return Crew(
        agents=[restaurant_knowledge_agent, content_creator_agent],
        tasks=[restaurant_task, content_task],
        process=Process.sequential,
        verbose=True
    )

st.title("Ceri-Mer Restaurant Content Generator")
st.write("""
Welcome to the Ceri-Mer Restaurant Content Generator! 
This tool helps create engaging social media content for your restaurant.
""")

# User input section
user_topic = st.text_input(
    "What would you like to create content about?",
    placeholder="E.g., weekend specials, new menu items, happy hour, etc."
)

if st.button("Generate Content"):
    if user_topic or st.checkbox("Generate general content"):
        with st.spinner("Generating your content..."):
            crew = create_agents_and_tasks(user_topic)
            result = crew.kickoff()
            st.success("Content Generated!")
            st.text_area("Generated Content:", value=result, height=300)
    else:
        st.warning("Please enter a topic or select 'Generate general content'")