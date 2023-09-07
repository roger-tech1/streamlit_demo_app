import streamlit as st
from utilities.toc_readin import get_toc

def create_multiselect(container: st.container,
                       book_names: list,
                       state_name: str):

    # check session state for checkbox value called checkbox_<filename>
    if f"checkbox_{state_name}" not in st.session_state:
        st.session_state[f"checkbox_{state_name}"] = False

    if f'selected_options_{state_name}' not in st.session_state:
        st.session_state[f'selected_options_{state_name}'] = []

    # define multi-select with session state selected options
    selected_options = container.multiselect(
        label= "Select one or more books to search",
        options=book_names,
        key=f"multiselect_{state_name}",
        placeholder="Select one or more books to search",
        default =st.session_state[f'selected_options_{state_name}'],
        max_selections=len(book_names)
    )

    # define checkbox callback
    def checkbox_callback():
        # check session state for checkbox value called checkbox_<filename>
        if f"checkbox_{state_name}" not in st.session_state:
            st.session_state[f"checkbox_{state_name}"] = False
        else:
            # update checkbox state
            st.session_state[f"checkbox_{state_name}"] = not st.session_state[f"checkbox_{state_name}"]

        # update selected options state
        if st.session_state[f"checkbox_{state_name}"]:
            selected_options= book_names
            st.session_state[f'selected_options_{state_name}'] = book_names
        else:
            selected_options = []
            st.session_state[f'selected_options_{state_name}'] = []

    # create checkbox to select all books with statr
    all= st.checkbox(label="Select all", 
                     value = st.session_state[f"checkbox_{state_name}"],
                     on_change=checkbox_callback)    

    return selected_options


def create_multiselect_container(toc_datapath: str,
                                 state_name: str):
    # read in table of contents
    book_names, book_chunk_lookup, chunk_book_lookup = get_toc(toc_datapath)

    # create container 
    container = st.container()

    # create multi-select tool
    selected_options = create_multiselect(container,
                                          book_names,
                                          state_name)

    return book_names, book_chunk_lookup, chunk_book_lookup, selected_options