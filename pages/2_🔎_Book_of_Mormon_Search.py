import streamlit as st
import json

# load in streamlit
st.set_page_config(page_title="Book of Mormon Search")
st.title('Book of Mormon Search')


with st.form('my_form'):

    # import BookofMormon.json from tocs folder
    with open('tocs/BookofMormon.json') as json_file:
        toc = json.load(json_file)

    # collect book numbers and names in separate lists
    book_names_raw = [v['book_name'].strip() for v in toc]
    book_names = []
    for name in book_names_raw:
        # capitalize first letter of each word
        better_name = ' '.join(v[0].upper() + v[1:].lower() for v in name.split(' '))
        book_names.append(better_name)
    book_numbers = [v['book_number'] for v in toc]

    # create inverse lookup dictionary consisting of book_name: book_number
    book_chunk_lookup = dict(zip(book_names, book_numbers))

    # define multiselect tool
    select_msg = "Select one or more books to search:"
    container = st.container()
    all = st.checkbox("Select all")
    if all:
        selected_options = container.multiselect(select_msg,
            book_names,book_names)
    else:
        selected_options =  container.multiselect(select_msg,
            book_names)
        
    submitted = st.form_submit_button('Submit')
    if submitted:
        print('you submitted the form')
        print(f'You selected: {selected_options}')