import streamlit as st
import os
import uuid
import pandas as pd
from demonstrator import *
import math
from PIL import Image
from random import randint
from streamlit_image_select import image_select
import time

st.header("Upload Your Images")
st.markdown("You have the option to select images from our curated gallery or upload your own unique photos to personalize your experience.")
st.markdown("Scroll down for results ⏬ It may take a few seconds, so thank you for your patience! 😊")

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def create_unique_folder(base_path):
    unique_folder = str(uuid.uuid4())
    unique_folder_path = os.path.join(base_path, unique_folder)
    os.makedirs(unique_folder_path)
    return unique_folder_path

# Function to mimic the image processing function
def your_image_processing_function(unique_folder_path):
    concepts = image_processing_function(unique_folder_path)
    return concepts

# Predefined images
gallery_placeholder = st.empty()
img = None
with gallery_placeholder.container():
        img = image_select(
        label="Choose an image from the options below",
        images=[
            "C:/Users/adalal/OneDrive - Kansas State University/PhD/New_Research/demonstrator/examples/bedroom.jpeg",
            "C:/Users/adalal/OneDrive - Kansas State University/PhD/New_Research/demonstrator/examples/highway.jpg",
            "C:/Users/adalal/OneDrive - Kansas State University/PhD/New_Research/demonstrator/examples/living_space.jpg",
            "C:/Users/adalal/OneDrive - Kansas State University/PhD/New_Research/demonstrator/examples/road.jpeg",
            "C:/Users/adalal/OneDrive - Kansas State University/PhD/New_Research/demonstrator/examples/vehicle.jpeg"
            ],
        use_container_width=True)
process_image = st.button("Process Selected Image")

## File uploader for user-uploaded images       
st.markdown("Or upload your own images:")
with st.form("my-form", clear_on_submit=True):
    uploaded_files = st.file_uploader("Upload file", accept_multiple_files=True, type=["jpg", "jpeg"])
    if uploaded_files and len(uploaded_files) > 3:
        st.warning(f"Maximum {3} files allowed. Please upload fewer files.")
    submitted = st.form_submit_button("Process Uploaded Image")    

#if st.button("Process Uploaded Image") or process_image:
if submitted or process_image:
    with st.spinner('This might take couple seconds, please wait..'):
        time.sleep(3)
    class_name = "building"
    if not uploaded_files and not img:
        st.warning("Please upload at least one image file.")
    else:
        allowed_extensions = {"jpg", "jpeg"}
        base_path = "uploads/"
        
        # Create a unique folder  and subfolder for the upload
        unique_folder_path = create_unique_folder(base_path)
        class_folder_path = os.path.join(unique_folder_path, class_name)
        os.makedirs(class_folder_path, exist_ok=True)

        # save image selected from given images in the class subfolder
        if img and process_image:
            with st.spinner('This might take couple seconds, please wait..'):
                time.sleep(3)
            preset_image_name = os.path.basename(img)
            preset_image_save_path = os.path.join(class_folder_path, preset_image_name)
            with open(preset_image_save_path, "wb") as f:
                with open(img, "rb") as src:
                    f.write(src.read())
        
        # Save each uploaded file in the class subfolder
        for uploaded_file in uploaded_files:
            if allowed_file(uploaded_file.name, allowed_extensions):
                file_path = os.path.join(class_folder_path, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
        
        # Run your image processing function here
        result_df = image_processing_function(unique_folder_path)

        grouped_df = result_df.groupby('Image Name')
        st.markdown("### Detected Concepts and Non-Target Percentages")

        for image_name, group_df in grouped_df:
            col1, col2 = st.columns([1, 2])

            with col1:
                image_path = os.path.join(unique_folder_path, group_df.iloc[0]['Class Name'], image_name)
                image = Image.open(image_path)
                st.image(image, caption=image_name, use_column_width=True)

            with col2:
                fig, ax = plt.subplots(figsize=(7, 5))
                sorted_df = group_df.sort_values(by='Non-Target Percentage', ascending=False)
                ax.barh(sorted_df['Detected Concept'], sorted_df['Non-Target Percentage'])
                ax.set_xlabel('Error-rate Percentage')
                #plt.tight_layout()
                st.pyplot(fig)

   
# Add the footer with email and GitHub link
st.markdown("""
    **Contact Information**:
    - **Email**: [adalal@ksu.edu](mailto:adalal@ksu.edu)
    - **GitHub**: [https://github.com/abhilekha-dalal](https://github.com/abhilekha-dalal)
""")