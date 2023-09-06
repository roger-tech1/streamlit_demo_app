import streamlit as st
from utilities.toc_readin import get_toc

def create_multiselect(container: st.container,
                        book_names: list):
    # define multiselect tool
    select_msg = "Select one or more books to search:"
    
    all = st.checkbox("Select all")
    if all:
        selected_options = container.multiselect(select_msg,
            book_names,book_names)
    else:
        selected_options =  container.multiselect(select_msg,
            book_names)
        
    return selected_options


def create_multiselect_container(toc_datapath):
    # read in table of contents
    book_names, book_chunk_lookup, chunk_book_lookup = get_toc(toc_datapath)

    # create container 
    container = st.container()

    # create multi-select tool
    selected_options = create_multiselect(container, book_names)
    return book_names, book_chunk_lookup, chunk_book_lookup, selected_options