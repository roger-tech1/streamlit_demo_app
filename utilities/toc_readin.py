import json 

def get_toc(toc_datapath:str):
    # import BookofMormon.json from tocs folder
    with open(toc_datapath) as json_file:
        toc = json.load(json_file)

    # collect book numbers and names in separate lists
    book_names_raw = [v['book_name'].strip() for v in toc]
    book_names = []
    for name in book_names_raw:
        # capitalize first letter of each word
        better_name = ' '.join(v[0].upper() + v[1:].lower() for v in name.split(' '))
        book_names.append(better_name)
    book_numbers = [v['book_number'] for v in toc]

    # create lookup dictionary consisting of book_name: book_number, and vice versa
    book_chunk_lookup = dict(zip(book_names, book_numbers))
    chunk_book_lookup = dict(zip(book_numbers, book_names))
    

    return book_names, book_chunk_lookup, chunk_book_lookup