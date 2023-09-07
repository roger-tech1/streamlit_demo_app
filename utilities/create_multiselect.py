import streamlit as st
from utilities.toc_readin import get_toc

def create_multiselect(container: st.container,
                        book_names: list,
                        toc_datapath: str):
    # get filename from datapath 
    filename = toc_datapath.split("/")[-1].split(".")[0]

    # check session state for checkbox value called checkbox_<filename>
    if f"checkbox_{filename}" not in st.session_state:
        st.session_state[f"checkbox_{filename}"] = False

    # create selected options state for filename multi-select if does not exist
    if f"selected_options_{filename}" not in st.session_state:
        st.session_state[f"selected_options_{filename}"] = []
 
    # define multi-select with session state selected options
    selected_options = st.multiselect(
        label= "Select one or more books to search",
        options=book_names,
        key=f"multiselect_{filename}",
        placeholder="Select one or more books to search",
        default =st.session_state[f"selected_options_{filename}"],
        max_selections=len(book_names)
    )


    # define checkbox callback
    def checkbox_callback():
        # check session state for checkbox value called checkbox_<filename>
        if f"checkbox_{filename}" not in st.session_state:
            st.session_state[f"checkbox_{filename}"] = False
        else:
            # update checkbox state
            st.session_state[f"checkbox_{filename}"] = not st.session_state[f"checkbox_{filename}"]

        # update selected options state
        if st.session_state[f"checkbox_{filename}"]:
            st.session_state[f"selected_options_{filename}"] = book_names
        else:
            st.session_state[f"selected_options_{filename}"] = []

    # create checkbox to select all books with statr
    all= st.checkbox(label="Select all", 
                     value = st.session_state[f"checkbox_{filename}"],
                     on_change=checkbox_callback)    

    return selected_options


def create_multiselect_container(toc_datapath):
    # read in table of contents
    book_names, book_chunk_lookup, chunk_book_lookup = get_toc(toc_datapath)

    # create container 
    container = st.container()

    # create multi-select tool
    selected_options = create_multiselect(container, book_names, toc_datapath)

    return book_names, book_chunk_lookup, chunk_book_lookup, selected_options