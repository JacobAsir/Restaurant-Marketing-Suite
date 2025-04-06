import streamlit as st
from groq import Groq
import base64
import os
from PIL import Image

# Initialize Groq client
client = Groq()
vision_model = 'llama-3.2-11b-vision-preview'
llama_model = 'llama-3.1-8b-instant'

st.title("Ceri-Mer Restaurant Content Generator")
st.write("Upload an image to create social media posts ")

# Function to encode image file
def encode_image_file(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

def generate_marketing_content(client, model, base64_image, extra_details=""):
    prompt = f"""
    You are the owner of Ceri-Mer Restaurant creating a social media post. 
    Analyze this image and create content in first-person perspective ("I", "we", "our").
    
    Restaurant Details:
    Name: Ceri-Mer Restaurant
    Address: 123 Culinary Street, Foodville
    Phone: (555) 123-4567
    Email: info@ceri-mer.com
    
    Operating Hours:
    - Monday to Thursday: 11am - 10pm
    - Friday to Saturday: 11am - 11pm
    - Sunday: 10am - 9pm
    
    {f"Additional details to include: {extra_details}" if extra_details else ""}
    
    Create a post following these guidelines:
    1. Attention-grabbing headline with emojis
    2. Short, readable paragraphs
    3. Appropriate emojis throughout
    4. Clear call-to-action
    5. Relevant hashtags at the end
    6. Warm, inviting tone
    7. Reference restaurant details naturally
    """
    
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model=model
    )
    return response.choices[0].message.content

# File uploader with extra details
uploaded_file = st.file_uploader("Choose an image to upload...", type=["jpg", "jpeg", "png"])
extra_details = st.text_area("Any special details about this image?", 
                           placeholder="E.g., ingredients, story behind the dish, special promotion")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)
    
    if st.button("Generate Content"):
        with st.spinner("Creating your Content..."):
            try:
                base64_image = encode_image_file(uploaded_file)
                result = generate_marketing_content(client, vision_model, base64_image, extra_details)
                
                st.success("Post Created Successfully!")
                st.subheader("Your Social Media Post")
                st.write(result)
                
            except Exception as e:
                st.error(f"Error generating content: {str(e)}")