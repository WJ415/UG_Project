import streamlit as st
import UMLS_search
import pre_process

# Define a dictionary of image-to-word-to-phrase mappings

#LDA analysis

#merge keywords to word cloud
#make a dictionary of keyword->first five head/tail words (related)

#visualise hidden topics



image_to_word_to_phrases = {
    'image1.png': {
        'apple': ['red fruit', 'juicy', 'crunchy'],
        'banana': ['diabetes', 'social care', 'hospital care'],
        'cherry': ['red fruit', 'small', 'tart'],
    },
    'image2.png': {
        'durian': ['spiky fruit', 'strong odor', 'creamy'],
        'elderberry': ['purple fruit', 'small', 'bitter'],
        'apple': ['red fruit', 'juicy', 'crunchy'],
    },
}

# Define a list of images for the first select box
image_list = list(image_to_word_to_phrases.keys())

# Display the images with a scrollable view
image_name = st.selectbox('Select an image:', image_list)
if image_name:
    with open("./word_cloud_figures/"+image_name, 'rb') as f:
        image_bytes = f.read()
    st.image(image_bytes, use_column_width=True)
    
    # Create a floating sidebar box for the select boxes
    with st.sidebar:
        # Display the first select box with clickable words
        word_list = list(image_to_word_to_phrases[image_name].keys())
        selected_word = st.selectbox('Select a word:', word_list)
        st.write(f"Searching {selected_word} on UMLS ... (may take up to two minutes)")

        def_list = [UMLS_search.umls_search(phrase) for phrase in image_to_word_to_phrases[image_name][selected_word]]
        def_list = [defi for defi in def_list if defi is not None]
        if len(def_list) != 0:
        	st.write(f"For {selected_word}, here are related concepts found on UMLS:")
        	for defi in def_list:
        		if defi != None:
        			st.write(f" - {defi[1]}, CUI: {defi[0]}")
        			st.write(f" -- {defi[2]} \n")
        else:
        	st.write(f"Sorry, did not found related concepts on UMLS")
