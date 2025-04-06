import streamlit as st

# Set page configuration as the first Streamlit command
st.set_page_config(
    page_title="Cerimer Restaurant Marketing Suite",
    page_icon="🍽️",
    layout="wide"
)

# Define the navigation pages
pg = st.navigation([
    st.Page(page="post.py", url_path='Social_Media_Posts'),
    st.Page(page="img_gen.py", url_path='Image_Generator'),
    st.Page(page="content.py", url_path='Content_Ideas'),
    st.Page(page="img_cap.py", url_path='Image_Captions')
])

# Add descriptions in the sidebar
st.sidebar.title("Descriptions")
st.sidebar.write("**Social Media Posts**: Create engaging content for your platforms.")
st.sidebar.write("**Image Generator**: Generate AI images for your restaurant.")
st.sidebar.write("**Content Ideas**: Get AI-powered marketing suggestions.")
st.sidebar.write("**Image Captions**: Create captions for your food photos.")

# Run the navigation
pg.run()