import streamlit as st
import UMLS_search
from multiprocessing import Process, freeze_support
import json

import time

collection_1 = "Social care"
collection_2 = "Hospital care"

# Define the function for the first page
def page1():
	# Load the dictionary from the file using the json module
	with open('./cache/generalised_1.json', 'r') as f:
	    generalised_1 = json.load(f)

	image_to_word_to_phrases = generalised_1

	# Define a list of images for the first select box
	image_list = list(image_to_word_to_phrases.keys())

	# Display the images with a scrollable view
	image_name = st.selectbox('Select a topic:', image_list)
	if image_name:
	    with open(rf"./Word_Cloud_Figures/{collection_1}/{image_name}.png", 'rb') as f:
	        image_bytes = f.read()
	    with open(rf"./Word_Cloud_Figures/{collection_1}/{image_name}.json", 'r') as f:
	        keyword_with_five_context = json.load(f)

	    st.image(image_bytes, use_column_width=True)
	    
	    # Create a floating sidebar box for the select boxes
	    with st.sidebar:
	        # Display the first select box with clickable words
	        word_list = list(image_to_word_to_phrases[image_name])
	        selected_word = st.selectbox('Select a word:', word_list)
	        st.write(f'Searching concepts related to "{selected_word}" on UMLS ... (may take up to two minutes)')

	        context_phrases = []
	        for i in keyword_with_five_context[selected_word][0]:
	        	context_phrases.append(i+" "+selected_word)
	        for i in keyword_with_five_context[selected_word][1]:
	        	context_phrases.append(selected_word+" "+i)
	        context_phrases = list(set(context_phrases))


	        def_list = [UMLS_search.umls_search(phrase) for phrase in context_phrases]
	        def_list = [defi for defi in def_list if defi is not None]
	        if len(def_list) != 0:
	        	st.write(f'For "{selected_word}", here are related concepts found on UMLS:\n')
	        	for defi in def_list:
	        		if defi != None:
	        			st.write(f" - {defi[1]}, CUI: {defi[0]}")
	        			st.write(f" Definition: \n {defi[2]} \n \n")
	        else:
	        	st.write(f"Sorry, did not found related concepts on UMLS")

    
# Define the function for the second page
def page2():
	# Load the dictionary from the file using the json module
	with open('./cache/generalised_2.json', 'r') as f:
	    generalised_2 = json.load(f)

	image_to_word_to_phrases = generalised_2

	# Define a list of images for the first select box
	image_list = list(image_to_word_to_phrases.keys())

	# Display the images with a scrollable view
	image_name = st.selectbox('Select a topic:', image_list)
	if image_name:
	    with open(rf"./Word_Cloud_Figures/{collection_2}/{image_name}.png", 'rb') as f:
	        image_bytes = f.read()
	    with open(rf"./Word_Cloud_Figures/{collection_2}/{image_name}.json", 'r') as f:
	        keyword_with_five_context = json.load(f)

	    st.image(image_bytes, use_column_width=True)
	    
	    # Create a floating sidebar box for the select boxes
	    with st.sidebar:
	        # Display the first select box with clickable words
	        word_list = list(image_to_word_to_phrases[image_name])
	        selected_word = st.selectbox('Select a word:', word_list)
	        st.write(f'Searching concepts related to "{selected_word}" on UMLS ... (may take up to two minutes)')

	        context_phrases = []
	        for i in keyword_with_five_context[selected_word][0]:
	        	context_phrases.append(i+" "+selected_word)
	        for i in keyword_with_five_context[selected_word][1]:
	        	context_phrases.append(selected_word+" "+i)
	        context_phrases = list(set(context_phrases))


	        def_list = [UMLS_search.umls_search(phrase) for phrase in context_phrases]
	        def_list = [defi for defi in def_list if defi is not None]
	        if len(def_list) != 0:
	        	st.write(f'For "{selected_word}", here are related concepts found on UMLS:\n')
	        	for defi in def_list:
	        		if defi != None:
	        			st.write(f" - {defi[1]}, CUI: {defi[0]}")
	        			st.write(f" Definition: \n {defi[2]} \n \n")
	        else:
	        	st.write(f"Sorry, did not found related concepts on UMLS")

# Define the function for the third page
def page3():
    # Load the dictionary from the file using the json module
	with open(f"./Word_Cloud_Figures/joint/{collection_1}.json", 'r') as f:
	    keyword_with_five_context1 = json.load(f)
	with open(f"./Word_Cloud_Figures/joint/{collection_2}.json", 'r') as f:
	    keyword_with_five_context2 = json.load(f)

	# Display the images with a scrollable view
	with open(rf"./Word_Cloud_Figures/joint/{collection_1} & {collection_2}.png", 'rb') as f:
	    image_bytes = f.read()

	st.image(image_bytes, use_column_width=True)
	    
	# Create a floating sidebar box for the select boxes
	with st.sidebar:
	    # Display the first select box with clickable words
	    word_list = list(keyword_with_five_context1.keys())
	    selected_word = st.selectbox('Select a word:', word_list)
	    st.write(f'Searching concepts related to "{selected_word}" on UMLS ... (may take up to three minutes)')

	    context_phrases = []
	    for i in keyword_with_five_context1[selected_word][0]:
	        context_phrases.append(i+" "+selected_word)
	    for i in keyword_with_five_context1[selected_word][1]:
	        context_phrases.append(selected_word+" "+i)
	    for i in keyword_with_five_context2[selected_word][0]:
	        context_phrases.append(i+" "+selected_word)
	    for i in keyword_with_five_context2[selected_word][1]:
	        context_phrases.append(selected_word+" "+i)
	    context_phrases = list(set(context_phrases))


	    def_list = [UMLS_search.umls_search(phrase) for phrase in context_phrases]
	    def_list = [defi for defi in def_list if defi is not None]
	    if len(def_list) != 0:
	        st.write(f'For "{selected_word}", here are related concepts found on UMLS:\n')
	        for defi in def_list:
	        	if defi != None:
	        		st.write(f" - {defi[1]}, CUI: {defi[0]}")
	        		st.write(f" Definition: \n {defi[2]} \n \n")
	    else:
	        st.write(f"Sorry, did not found related concepts on UMLS")


# Define a dictionary of page names to functions
pages = {
    collection_1: page1,
    collection_2: page2,
    'Joint keywords': page3
}

# Create a sidebar menu with links to each page
selection = st.sidebar.radio('Select collection:', list(pages.keys()))

# Call the function for the selected page
pages[selection]()


