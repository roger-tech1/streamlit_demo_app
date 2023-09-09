import streamlit as st
from utilities.toc_readin import get_toc
from utilities.create_multiselect import create_multiselect_container
from utilities.api_requests import step_request, unpack_response
import os
from dotenv import load_dotenv
load_dotenv()
STEP_ARN = str(os.environ.get('KINGJAMES_NT_KEYWORD_STEP_ARN'))

# setup page
st.set_page_config(
    page_title="King James New Testament Keyword Search",
    page_icon="📚"
    )

st.title('King James New Testament Keyword Search')

# state name for this page 
state_name = 'KingJamesNTKeywordSearch'

# Create the relative path based on the parent directory
parent_directory = os.path.dirname(os.path.dirname(__file__))
toc_datapath = parent_directory + '/tocs/KingJamesNT.json'

# create multiselect
book_names, book_chunk_lookup, chunk_book_lookup, selected_options = create_multiselect_container(toc_datapath,            
                                                                                                  state_name)

# start search form
with st.form('King James New Testament Keyword Search'):

    # text area
    query_text = st.text_area('Enter keyword(s) separated by spaces:', 'lord heaven')

    # submit button        
    submitted = st.form_submit_button('Submit')

    # check for submission
    if submitted:
        # check for empty selected_options 
        if len(selected_options) == 0:
            st.write('Please select at least one book.')
        else:
            with st.spinner('Searching...'):
                # make request
                response = step_request(selected_options, 
                                        book_chunk_lookup,
                                        query_text,
                                        STEP_ARN)
                # unpack response 
                result = unpack_response(response,
                                        chunk_book_lookup,
                                        kind='keyword')
    