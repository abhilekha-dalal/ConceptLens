import streamlit as st
import pandas as pd

st.set_page_config(page_title="ConceptLens",
                   page_icon=":bridge_at_night:",
                   layout="wide")

# Create two columns
col1, col2 = st.columns([2,1.5])

# First vertical container in the first column
with col1:
    ### video
    video_file = open('video.mp4', 'rb')
    video_bytes = video_file.read()
    width = st.sidebar.slider(
    label="Width", min_value=0, max_value=100, value=100, format="%d%%"
    )
    width = max(width, 0.01)
    side = max((100 - width) / 2, 0.01)
    _, container, _ = st.columns([side, width, side])
    container.video(data=video_bytes,loop=True, autoplay=True)

    with st.sidebar:
        st.header("Link to related resources")
        st.link_button("ECII", url = 'https://arxiv.org/abs/1812.03243')
        st.link_button("Error-margin Analysis", url = 'https://arxiv.org/abs/2405.09580')
        st.link_button("Hidden Neuron Activation Analysis", url = 'http://arxiv.org/abs/2404.13567')
        st.link_button("Github repo", url = 'https://github.com/abhilekha-dalal/ConceptLens')

        
    # button to the "Upload Images" page
    st.link_button("Explore ConceptLens now!", url = '/Upload_Images')
    
# Second vertical container in the second column
with col2:
    st.markdown("# :rainbow[ConceptLens]")
    st.subheader("_from Pixels to Understanding_")
    st.markdown("**Created by Abhilekha Dalal**")

#####################
st.header("Summary")
st.write("Dive into the vibrant world of ConceptLens, where we turn the complex labyrinths of artificial neural networks into a visual spectacle of understanding! At ConceptLens, we pride ourselves on our pioneering approach to interpreting hidden neuron activations. Our unique blend of advanced deep learning models and symbolic methods illuminates the once obscure decision-making of neural networks. It’s like having a conversation with the AI itself, as you uncover what activates neurons and how they react to various stimuli—this is our error-margin analysis in action, a feature you’ll find only with us.")
# st.write("Dive into the vibrant world of ConceptLens, where we turn the complex labyrinths of artificial neural networks into a visual spectacle of understanding! Our platform is not just a tool; it’s a revolution in the realm of deep learning. With ConceptLens, you’re not just analyzing image data; you’re embarking on an expedition to decode the very essence of AI thought processes.")
# st.write("At ConceptLens, we pride ourselves on our pioneering approach to interpreting hidden neuron activations. Our unique blend of advanced deep learning models and symbolic methods illuminates the once obscure decision-making of neural networks. It’s like having a conversation with the AI itself, as you uncover what activates neurons and how they react to various stimuli—this is our error-margin analysis in action, a feature you’ll find only with us.")
st.write("Our intuitive interface invites you to effortlessly upload images and witness the magic unfold in real time. The results? A detailed, colorful visualization that not only educates but also captivates. It’s a gateway to understanding neuron functionality like never before, pushing the boundaries of what’s possible in deep learning.")
st.markdown("For a deep dive into the science behind our platform, our [*Research Paper*](https://arxiv.org/abs/2405.09580) - “Error-margin Analysis for Hidden Neuron Activation Labels” awaits your curiosity. We envision a world where researchers like you leverage ConceptLens to unlock groundbreaking insights into images.")
st.write("So why wait? Step into the lens of ConceptLens and see the unseen. Let’s reshape the future of neural network interpretability together!")
#####################
st.header("Usage")
st.write("To the left, is the main menu for navigating to different pages in the *ConceptLens*:")
st.markdown("- **Home Page:** We are here!")
st.markdown("- **Upload Images:** This section allows you to explore *ConceptLens'* functionalities. You can either select images from our curated gallery or upload your own images. Once uploaded, ConceptLens will generate a plot with detected concepts and an error margin percentage.")
st.markdown("- **Explore ConceptLens now:** This takes you directly to the Upload Images page.")
st.markdown("- **Related Resources:** Interested in learning more about the research behind *ConceptLens*? Visit this section to find links to the relevant paper." )
#####################
st.header("Authors")
st.write("Please feel free to contact with any issues, comments, or questions.")
st.subheader("Abhilekha Dalal")
contact_info = """
**Email:** [adalal@ksu.edu](mailto:adalal@ksu.edu)  
**GitHub:** [https://github.com/abhilekha-dalal](https://github.com/abhilekha-dalal)
"""

st.markdown(contact_info)

