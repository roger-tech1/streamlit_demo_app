import streamlit as st
import os
from dotenv import load_dotenv
import json 
import requests

# Load variables from .env file
load_dotenv()
STEP_ENDPOINT_URL = os.environ.get('STEP_ENDPOINT_URL')
STEP_API_KEY = os.environ.get('STEP_API_KEY')
BOOK_OF_MORMON_KEYWORD_STEP_ARN = os.environ.get('BOOK_OF_MORMON_KEYWORD_STEP_ARN')


def prepare_request_data(selected_options, book_chunk_lookup, query_text, step_arn):
    # convert selection_options using book_chunk_lookup
    selected_chunks = [book_chunk_lookup[v] for v in selected_options]

    # construct initial query object
    query_object = {"query": query_text}
    for i in range(len(book_chunk_lookup)):
        query_object[f"useChunk{i}"] = False

    # set useChunk to true for selected chunks
    for chunk in selected_chunks:
        query_object[f"useChunk{chunk}"] = True

    data = {
        "input": json.dumps(query_object),
        "name": "MyExecution",
        "stateMachineArn": step_arn
    }

    # prepare headers
    headers = {
      'x-api-key': STEP_API_KEY,
      'Content-Type': 'application/json'  # Adjust the content type if needed
    }

    return data, headers


# step request function
def step_request(selected_options, book_chunk_lookup, query_text, step_arn):
    # prepare data
    data, headers = prepare_request_data(selected_options, book_chunk_lookup, query_text, step_arn)

    # make request
    response = requests.post(STEP_ENDPOINT_URL, json=data, headers=headers, timeout=900)
    return response


def display_results(output, chunk_book_lookup):
    if len(output) == 0:
        st.write('No results found.')
        return None
    
    # loop over returned volumes
    for volume_results in output:
        book_number = volume_results[0]['book_number']
        book_name = chunk_book_lookup[book_number-1]

        st.write('---')
        st.write(f"""
        Results from book: {book_name}
        ---
        ---
        """)
        
        for datapoint in volume_results:
            try:
                # unpack datapoint
                book_number = datapoint['book_number']
                chapter_number = datapoint['chapter_number']
                verse_number = datapoint['verse_number']
                try: 
                    verse = datapoint['verse_content']
                except:
                    verse = datapoint['content']

                try:
                    word_numbers = datapoint['word_numbers']
                except:
                    pass
                try:
                    score = datapoint['score']
                except:
                    pass


                st.write(f'**Verse**: {verse}')
                st.write(f'**Verse number**: {verse_number}')
                st.write(f'**Chapter**: {chapter_number}')
                try:
                    st.write(f'**Word numbers**: {word_numbers}')
                except:
                    pass
                try:
                    st.write(f'**Score**: {score}')
                except:
                    pass
                st.write('---')
            except Exception as e:
                print('Error unpacking volume data:', e)
                print('datapoint:', datapoint)

# unpack response for keyword
def unpack_response(response, 
                    chunk_book_lookup,
                    kind='keyword'):
    # Check the response
    if response.status_code == 200:
        # unpack response and return
        try:
            # unpack response
            step_response = response.json()
            output = json.loads(step_response['output'])['query_results']
            output = [o for o in output if isinstance(o, dict)]
            query_results = []
            if kind == 'keyword':
                for v in output:
                    try:
                        query_results.append(v['query_results'][0])
                    except:
                        pass
            else:
                for v in output:
                    try:
                        query_results.append(v['query_results'])
                    except:
                        pass

            # display results
            display_results(query_results, chunk_book_lookup)
            return output
        except Exception as e:
            print('Error unpacking response:', e)
            print('Response:', step_response)
    else:
        print('Request failed with status code:', response.status_code, 'Response:', response.text)
        st.write('Request failed with status code:', response.status_code, 'Response:', response.text)
        return None
