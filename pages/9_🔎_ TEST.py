import streamlit as st
from utilities.create_multiselect import create_multiselect_container
from utilities.api_requests import step_request, unpack_response
import os
from dotenv import load_dotenv
parent_directory = os.path.dirname(os.path.dirname(__file__))

load_dotenv()
BOM_KEYWORD_STEP_ARN = str(os.environ.get('BOOK_OF_MORMON_KEYWORD_STEP_ARN'))
BOM_VECTOR_STEP_ARN = str(os.environ.get('BOOK_OF_MORMON_VECTOR_STEP_ARN'))
BOM_TOC_DATAPATH = parent_directory + '/tocs/BookOfMormon.json' 


NT_KEYWORD_STEP_ARN = str(os.environ.get('KINGJAMES_NT_KEYWORD_STEP_ARN'))
NT_VECTOR_STEP_ARN = str(os.environ.get('KINGJAMES_NT_EMBEDDING_STEP_ARN'))
NT_TOC_DATAPATH = parent_directory + '/tocs/KingJamesNT.json' 


OT_KEYWORD_STEP_ARN = str(os.environ.get('KINGJAMES_OT_KEYWORD_STEP_ARN'))
OT_VECTOR_STEP_ARN = str(os.environ.get('KINGJAMES_OT_EMBEDDING_STEP_ARN'))
OT_TOC_DATAPATH = parent_directory + '/tocs/KingJamesOT.json' 



# setup page
st.set_page_config(
    page_title="Scripture multi-search",
    page_icon="📚"
    )

st.header(body='Scripture multi-search',
          anchor=None,
          divider='blue')


### select scripture type ###
if 'selected_volume' not in st.session_state:
    st.session_state['selected_volume'] = 'BookOfMormon'
if 'selected_toc_datapath' not in st.session_state:
    st.session_state['selected_toc_datapath'] = BOM_TOC_DATAPATH

# select search type 
st.subheader('Select scripture:')
with st.expander(label='Scripture options:', expanded=True):
    with st.container():
        # initialize toggle button states 
        if f"bom_search_toggle" not in st.session_state:
            st.session_state[f"bom_search_toggle"] = True
        if f"nt_search_toggle" not in st.session_state:
            st.session_state[f"nt_search_toggle"] = False
        if f"ot_search_toggle" not in st.session_state:
            st.session_state[f"ot_search_toggle"] = False

        # callbacks
        def bom_search_toggle_callback():
            if st.session_state[f"bom_search_toggle"] == True:
                st.session_state['selected_volume'] = 'BookOfMormon'
                st.session_state['selected_toc_datapath'] = BOM_TOC_DATAPATH
                st.session_state[f"nt_search_toggle"] = False
                st.session_state[f"ot_search_toggle"]  = False

        def nt_search_toggle_callback():
            if st.session_state[f"nt_search_toggle"] == True:
                st.session_state['selected_volume'] = 'KingJamesNT'
                st.session_state[f"selected_toc_datapath"] = NT_TOC_DATAPATH
                st.session_state[f"bom_search_toggle"] = False
                st.session_state[f"ot_search_toggle"]  = False
        
        def ot_search_toggle_callback():
            if st.session_state[f"ot_search_toggle"] == True:
                st.session_state['selected_volume'] = 'KingJamesOT'
                st.session_state[f"selected_toc_datapath"] = OT_TOC_DATAPATH
                st.session_state[f"bom_search_toggle"] = False
                st.session_state[f"nt_search_toggle"]  = False

        # select scripture 
        bom_col, nt_col, ot_col = st.columns(3)
        with bom_col:
            bom_search_toggle = st.toggle('Book of Mormon', 
                                            value=st.session_state[f"bom_search_toggle"], 
                                            key='bom_search_toggle',
                                            on_change=bom_search_toggle_callback)
        with nt_col:
            nt_search_toggle = st.toggle('King James - New Testament',
                                            value=st.session_state[f"nt_search_toggle"],
                                            key='nt_search_toggle',
                                            on_change=nt_search_toggle_callback)
        with ot_col:
            ot_search_toggle = st.toggle('King James - Old Testament',
                                            value=st.session_state[f"ot_search_toggle"],
                                            key='ot_search_toggle',
                                            on_change=ot_search_toggle_callback)
st.write('---')

     


### select search type ###
# initialize state arn
if f"STEP_ARN" not in st.session_state:
    st.session_state['STEP_ARN'] = BOM_KEYWORD_STEP_ARN

# select search type 
st.subheader('Select search type:')
with st.expander(label='Search options:', expanded=True):
    with st.container():
        # initialize toggle button states 
        if f"keyword_search_toggle" not in st.session_state:
            st.session_state[f"keyword_search_toggle"] = True
        if f"vector_search_toggle" not in st.session_state:
            st.session_state[f"vector_search_toggle"] = False
        if f"verse_search_toggle" not in st.session_state:
            st.session_state[f"verse_search_toggle"] = False

        # callbacks
        def keyword_search_toggle_callback():
            if st.session_state[f"keyword_search_toggle"] == True:
                st.session_state[f"vector_search_toggle"] = False
                st.session_state[f"verse_search_toggle"]  = False

                if st.session_state['selected_volume'] == 'BookOfMormon':
                    st.session_state['STEP_ARN'] = BOM_KEYWORD_STEP_ARN
                elif st.session_state['selected_volume'] == 'KingJamesNT':
                    st.session_state['STEP_ARN'] = NT_KEYWORD_STEP_ARN
                elif st.session_state['selected_volume'] == 'KingJamesOT':
                    st.session_state['STEP_ARN'] = OT_KEYWORD_STEP_ARN

        def vector_search_toggle_callback():
            if st.session_state[f"vector_search_toggle"] == True:
                st.session_state[f"keyword_search_toggle"] = False
                st.session_state[f"verse_search_toggle"]  = False

                if st.session_state['selected_volume'] == 'BookOfMormon':
                    st.session_state['STEP_ARN'] = BOM_VECTOR_STEP_ARN
                elif st.session_state['selected_volume'] == 'KingJamesNT':
                    st.session_state['STEP_ARN'] = NT_VECTOR_STEP_ARN
                elif st.session_state['selected_volume'] == 'KingJamesOT':
                    st.session_state['STEP_ARN'] = OT_VECTOR_STEP_ARN

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


### create multi select books ###
def create_multi_select():
    # state name for this page 
    state_name = st.session_state['selected_volume']

    # Create the relative path based on the parent directory
    toc_datapath = st.session_state['selected_toc_datapath']    

    # create multiselect
    book_names, book_chunk_lookup, chunk_book_lookup, selected_options = create_multiselect_container(toc_datapath,
                                                                                                        state_name)
    return book_names, book_chunk_lookup, chunk_book_lookup, selected_options

book_names, book_chunk_lookup, chunk_book_lookup, selected_options = create_multi_select()
st.text("")
st.text("")


### create search form ###
with st.form(key='Search Form'):

    # submit button        
    submitted = st.form_submit_button('Submit')

    # set text area based on search type
    if st.session_state[f"keyword_search_toggle"] == True:
        if st.session_state['selected_volume'] == 'BookOfMormon':
            query_text = st.text_area('Enter keyword(s) separated by spaces:', 'lord nephi sam')
        elif st.session_state['selected_volume'] == 'KingJamesNT':
            query_text = st.text_area('Enter keyword(s) separated by spaces:', 'lord heaven')
        elif st.session_state['selected_volume'] == 'KingJamesOT':
            query_text = st.text_area('Enter keyword(s) separated by spaces:', 'lord heaven')

    elif st.session_state[f"vector_search_toggle"] == True:
        if st.session_state['selected_volume'] == 'BookOfMormon':
            query_text = st.text_area('Enter verse snippet:', 'And they came down and went forth upon the face of the earth')
        elif st.session_state['selected_volume'] == 'KingJamesNT':
            query_text = st.text_area('Enter verse snippet:', 'At once we see via a dark glass but someday we will see each other clearly')
        elif st.session_state['selected_volume'] == 'KingJamesOT':
            query_text = st.text_area('Enter verse snippet:', 'At the start god made')

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