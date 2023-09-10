import streamlit as st
from utilities.create_multiselect import create_multiselect_container
from utilities.api_requests import step_request, unpack_response
import os
from dotenv import load_dotenv
load_dotenv()
BOM_KEYWORD_STEP_ARN = str(os.environ.get('BOOK_OF_MORMON_KEYWORD_STEP_ARN'))
BOM_VECTOR_STEP_ARN = str(os.environ.get('BOOK_OF_MORMON_VECTOR_STEP_ARN'))

# setup page
st.set_page_config(
    page_title="Book of Mormon Search",
    page_icon="📚"
    )

st.header(body='Book of Mormon Search',
          anchor=None,
          divider='blue')

# initialize state arn
if f"STEP_ARN" not in st.session_state:
    st.session_state['STEP_ARN'] = BOM_KEYWORD_STEP_ARN

# select search type 
st.subheader('Select search type:')
with st.container():
    # initialize toggle button states 
    if f"keyword_search_toggle" not in st.session_state:
        st.session_state[f"keyword_search_toggle"] = True
        st.session_state['STEP_ARN'] = BOM_KEYWORD_STEP_ARN
    if f"vector_search_toggle" not in st.session_state:
        st.session_state[f"vector_search_toggle"] = False
    if f"verse_search_toggle" not in st.session_state:
        st.session_state[f"verse_search_toggle"] = False

    # callbacks
    def keyword_search_toggle_callback():
        if st.session_state[f"keyword_search_toggle"] == True:
            st.session_state['STEP_ARN'] = BOM_KEYWORD_STEP_ARN
            st.session_state[f"vector_search_toggle"] = False
            st.session_state[f"verse_search_toggle"]  = False

    def vector_search_toggle_callback():
        if st.session_state[f"vector_search_toggle"] == True:
            st.session_state['STEP_ARN'] = BOM_VECTOR_STEP_ARN
            st.session_state[f"keyword_search_toggle"] = False
            st.session_state[f"verse_search_toggle"]  = False
    
    def verse_search_toggle_callback():
        if st.session_state[f"verse_search_toggle"] == True:
            st.session_state[f"keyword_search_toggle"] = False
            st.session_state[f"vector_search_toggle"]  = False

    # select search type
    keyword_col, vector_col, verse_col = st.columns(3)
    with keyword_col:
        keyword_search_toggle = st.toggle('keyword search', 
                                        value=st.session_state[f"keyword_search_toggle"], 
                                        key='keyword_search_toggle',
                                        on_change=keyword_search_toggle_callback)
    with vector_col:
        vector_search_toggle = st.toggle('vector search',
                                        value=st.session_state[f"vector_search_toggle"],
                                        key='vector_search_toggle',
                                        on_change=vector_search_toggle_callback)
    with verse_col:
        verse_search_toggle = st.toggle('verse search',
                                        value=st.session_state[f"verse_search_toggle"],
                                        key='verse_search_toggle',
                                        on_change=verse_search_toggle_callback)
st.write('---')

def create_multi_select():
    # state name for this page 
    state_name = 'BookofMormonKeywordSearch'

    # Create the relative path based on the parent directory
    parent_directory = os.path.dirname(os.path.dirname(__file__))
    toc_datapath = parent_directory + '/tocs/BookOfMormon.json' 

    # create multiselect
    book_names, book_chunk_lookup, chunk_book_lookup, selected_options = create_multiselect_container(toc_datapath,
                                                                                                        state_name)
    
    return book_names, book_chunk_lookup, chunk_book_lookup, selected_options

book_names, book_chunk_lookup, chunk_book_lookup, selected_options = create_multi_select()

# start search form
with st.form(key='Search Form'):

    # submit button        
    submitted = st.form_submit_button('Submit')

    # set text area based on search type
    if st.session_state[f"keyword_search_toggle"] == True:
        # set query text
        query_text = st.text_area('Enter keyword(s) separated by spaces:', 'lord nephi sam')
                    
    elif st.session_state[f"vector_search_toggle"] == True:
        query_text = st.text_area('Enter verse snippet:', 'And they came down and went forth upon the face of the earth')


    # set submit button based on search type
    if st.session_state[f"keyword_search_toggle"] == True or st.session_state[f"vector_search_toggle"] == True:
        text_search_type = 'keyword'
        if st.session_state[f"vector_search_toggle"] == True:
            text_search_type = 'vector'
         

        # set submission action
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
                                            st.session_state['STEP_ARN'])
                    # unpack response 
                    result = unpack_response(response,
                                            chunk_book_lookup,
                                            kind=text_search_type)