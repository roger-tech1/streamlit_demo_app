import streamlit as st
from utilities.toc_readin import get_toc
from utilities.create_multiselect import create_multiselect_container
from utilities.api_requests import step_request, unpack_response
import os
from dotenv import load_dotenv
load_dotenv()
STEP_ARN = str(os.environ.get('BOOK_OF_MORMON_KEYWORD_STEP_ARN'))

# setup page
st.set_page_config(
    page_title="Book of Mormon Keyword Search",
    page_icon="📚"
    )

st.title('Book of Mormon Keyword Search')

# state name for this page 
state_name = 'BookofMormonKeywordSearch'

# Create the relative path based on the parent directory
parent_directory = os.path.dirname(os.path.dirname(__file__))
toc_datapath = parent_directory + '/tocs/BookOfMormon.json'

# list all files in parent_directory 
print(f'parent_directory: {parent_directory}')
print(os.listdir(parent_directory + '/tocs'))
 

# check if toc_datapath file exists
if not os.path.isfile(toc_datapath):
    # if not, download from s3
    print('FAIL: toc_datapath does not exist')
    # download_toc_datapath_from_s3(toc_datapath)

# print(type(toc_datapath))
# print(type(test))

# print(toc_datapath)
# print(test)

# print(len(toc_datapath))
# print(len(test))


# create multiselect
book_names, book_chunk_lookup, chunk_book_lookup, selected_options = create_multiselect_container(toc_datapath,
                                                                                                  state_name)

# start search form
with st.form('Book of Mormon Keyword Search'):

    # text area
    query_text = st.text_area('Enter keyword:', 'love')

    # submit button        
    submitted = st.form_submit_button('Submit')

    # check for submission
    if submitted:
        with st.spinner('Searching...'):
            # make request
            response = step_request(selected_options, book_chunk_lookup,
                                     query_text,
                                     STEP_ARN)

            # unpack response 
            result = unpack_response(response,
                                     chunk_book_lookup,
                                     kind='keyword')
    