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

if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'

# setup page
st.set_page_config(
    page_title="Scripture multi-search",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state=st.session_state.sidebar_state
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
            bom_search_toggle = st.toggle(label='Book of Mormon', 
                                        value=st.session_state[f"bom_search_toggle"], 
                                        key='bom_search_toggle',
                                        on_change=bom_search_toggle_callback)
        with nt_col:
            nt_search_toggle = st.toggle(label='King James - New Testament',
                                        value=st.session_state[f"nt_search_toggle"],
                                        key='nt_search_toggle',
                                        on_change=nt_search_toggle_callback)
        with ot_col:
            ot_search_toggle = st.toggle(label='King James - Old Testament',
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

                if st.session_state['selected_volume'] == 'BookOfMormon':
                    st.session_state['STEP_ARN'] = BOM_KEYWORD_STEP_ARN
                elif st.session_state['selected_volume'] == 'KingJamesNT':
                    st.session_state['STEP_ARN'] = NT_KEYWORD_STEP_ARN
                elif st.session_state['selected_volume'] == 'KingJamesOT':
                    st.session_state['STEP_ARN'] = OT_KEYWORD_STEP_ARN


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

### initialize state and callbacks for number_input chapter and verse ###
if f"chapter_number" not in st.session_state:
    st.session_state['chapter_number'] = 1
if f"verse_number" not in st.session_state:
    st.session_state['verse_number'] = 1

chapter_number = 1
verse_number = 1

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

    # set text area based on search type
    if st.session_state[f"keyword_search_toggle"] == True:
        if st.session_state['selected_volume'] == 'BookOfMormon':
            query_text = st.text_area(label='Enter keyword(s) separated by spaces:',placeholder='For example -"lord nephi sam"')
        elif st.session_state['selected_volume'] == 'KingJamesNT':
            query_text = st.text_area(label='Enter keyword(s) separated by spaces:', placeholder='For example - "lord heaven"')
        elif st.session_state['selected_volume'] == 'KingJamesOT':
            query_text = st.text_area(label='Enter keyword(s) separated by spaces:', placeholder='For example - "lord heaven"')

    elif st.session_state[f"vector_search_toggle"] == True:
        if st.session_state['selected_volume'] == 'BookOfMormon':
            query_text = st.text_area(label='Enter verse snippet:', placeholder='For example - "And they came down and went forth upon the face of the earth"')
        elif st.session_state['selected_volume'] == 'KingJamesNT':
            query_text = st.text_area(label='Enter verse snippet:', placeholder='For example - "At once we see via a dark glass but someday we will see each other clearly"')
        elif st.session_state['selected_volume'] == 'KingJamesOT':
            query_text = st.text_area(label='Enter verse snippet:', placeholder='For example - "At the start god made"')

    elif st.session_state[f"verse_search_toggle"] == True:
            chapter_number = st.number_input(label='Enter chapter number:', value = 1, step=1, min_value=1, max_value=40)
            verse_number = st.number_input(label='Enter verse number:', value = 1, step=1, min_value=1, max_value=100)

    # set submit button based on search type
    if st.session_state[f"keyword_search_toggle"] == True or st.session_state[f"vector_search_toggle"] == True:
        text_search_type = 'keyword'
        if st.session_state[f"vector_search_toggle"] == True:
            text_search_type = 'vector'
        
        # submit button        
        submitted = st.form_submit_button('Submit')
        
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
    elif st.session_state[f"verse_search_toggle"] == True:         
        # submit button        
        submitted = st.form_submit_button('Submit')
        
        # set submission action
        if submitted:

            # check for empty selected_options 
            if len(selected_options) == 0:
                st.write('Please select at least one book.')
            elif len(selected_options) > 1:
                st.write('Please select only one book.')
            else:
                # unpack book name from selected_options 
                book_name = selected_options[0]

                # convert book_name to book_number using book_chunk_lookup
                book_number = book_chunk_lookup[book_name] + 1

                # formulate book.chapter.verse query string
                query_text = f'{book_number}.{chapter_number}.{verse_number}'
                with st.spinner('Searching...'):
                    # make request
                    response = step_request(selected_options, 
                                            book_chunk_lookup,
                                            query_text,
                                            st.session_state['STEP_ARN'])

                    # unpack response 
                    result = unpack_response(response,
                                            chunk_book_lookup,
                                            kind='keyword')



# st.header('scrollable text')

# ### scrollable text ###

# text_content = """
# <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed in odio nec turpis ultricies vehicula ac ut orci. Nullam auctor nisi et est semper blandit. Sed in interdum nulla. Vivamus ut facilisis dui. Fusce nec ex purus. Integer vel feugiat odio, at fermentum lectus.</p>
# <p>Phasellus fringilla justo eu orci faucibus, id iaculis purus varius. Maecenas a quam vitae urna suscipit egestas. Duis hendrerit, nunc id cursus sollicitudin, quam velit venenatis odio, in elementum ipsum erat vel sapien.</p>
# <!-- Add more text here -->
# """

# scrollable_element = f"""
#     <div class="scroll-container">
#         {text_content}
# """


# st.markdown(scrollable_element, unsafe_allow_html=True)