import streamlit as st
from together import Together
import requests
from io import BytesIO
import os

# Streamlit App Title
st.title("Cerimer Restaurant Image Generator")
st.write("Generate custom food and restaurant images for Cerimer using AI. Perfect for menus, promotions, and social media.")

# Sidebar Description
st.sidebar.title("Restaurant Image Generator")
st.sidebar.write("""
Provide a text prompt describing the food, ambiance, or promotional image you want to create for Cerimer.
The AI will generate a custom image based on your description.

**For example:**
- **Prompt**: A gourmet plate of Cerimer's signature seafood pasta with garnish.
- **Output**: A beautiful image of the described dish.
""")

# Get API key from environment variable
api_key = os.environ.get("TOGETHER_API_KEY")

# Initialize Together AI Client
client = Together(api_key=api_key)

# Function to Generate Image
def generate_image(prompt, model="black-forest-labs/FLUX.1-schnell-Free", steps=4):
    try:
        # Add Cerimer context to the prompt if not already included
        if "cerimer" not in prompt.lower():
            prompt = f"Cerimer Restaurant: {prompt}"
        response = client.images.generate(
            prompt=prompt, model=model, steps=steps
        )
        return response.data[0].url
    except Exception as e:
        st.error(f"Error generating image: {e}")
        return None

# Function to Download Image
def download_image(image_url):
    response = requests.get(image_url)
    return BytesIO(response.content)

# Text-to-Image Generation
st.header("Cerimer Restaurant Image Creator")
prompt = st.text_input("Describe the restaurant image you want to generate:")
st.caption("Examples: 'A beautifully plated signature dish', 'Cozy interior of Cerimer at night', 'Chef preparing food in Cerimer kitchen'")

if st.button("Generate Restaurant Image"):
    if prompt:
        st.info("Creating your Cerimer restaurant image...")
        image_url = generate_image(prompt)
        if image_url:
            st.image(image_url, caption="Generated Cerimer Image", width=500)
            # Add download button
            img_data = download_image(image_url)
            st.download_button(
                label="Download Image for Cerimer",
                data=img_data,
                file_name="cerimer_image.png",
                mime="image/png",
            )
    else:
        st.warning("Please enter a description for your restaurant image.")

# Footer
st.write("Powered by Cerimer Restaurant Marketing Team")