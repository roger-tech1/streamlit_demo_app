import streamlit as st
from utilities.toc_readin import get_toc
from utilities.create_multiselect import create_multiselect_container
from utilities.api_requests import step_request, unpack_response
import os
from dotenv import load_dotenv
load_dotenv()
STEP_ARN = os.environ.get('KINGJAMES_NT_EMBEDDING_STEP_ARN')


# setup page
st.set_page_config(
    page_title="King James New Testament Vector Search",
    page_icon="📚"
    )

st.title('King James New Testament Vector Search')

# create multiselect
parent_directory = os.path.dirname(os.path.dirname(__file__))
toc_datapath = os.path.join(parent_directory, 'tocs/KingJamesNT.json')
book_names, book_chunk_lookup, chunk_book_lookup, selected_options = create_multiselect_container(toc_datapath)

# start search form
with st.form('King James New Testament Vector Search'):

    # text area
    query_text = st.text_area('Enter verse snippet:', 'At once we see via a dark glass but someday we will see each other clearly')

    # submit button        
    submitted = st.form_submit_button('Submit')

    # check for submission
    if submitted:
        with st.spinner('Searching...'):
            # make request
            response = step_request(selected_options, 
                                    book_chunk_lookup, query_text, 
                                    STEP_ARN)

            # unpack response 
            result = unpack_response(response, 
                                     chunk_book_lookup,
                                     kind='vector')
    