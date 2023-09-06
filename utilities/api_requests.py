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
 
    # get max chunk number from book_chunk_lookup
    max_chunk = max(book_chunk_lookup.values())

    # construct initial query object
    query_object = {"query": query_text}
    for i in range(max_chunk):
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
    # loop over returned volumes
    for datapoint in output:
        try:
            # unpack datapoint
            book_number = datapoint['book_number']
            chapter_number = datapoint['chapter_number']
            verse_number = datapoint['verse_number']
            try: 
                verse = datapoint['verse_content']
            except:
                verse = datapoint['content']

            book_name = chunk_book_lookup[book_number]
            try:
                word_numbers = datapoint['word_numbers']
            except:
                pass
            try:
                score = datapoint['score']
            except:
                pass

            st.write('---')
            st.write(f"""
            Results from book: {book_name}
            ---
            ---
            """)
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
            output = json.loads(step_response['output'])
            output = output ['query_results'][1]['query_results']

            # separate into query results and toc
            query_results = None 
            if kind == 'keyword':
                query_results = output[0]
            else:
                query_results = output

            # display results
            display_results(query_results, chunk_book_lookup)
            print(f'query_results: {query_results}')
            return output
        except Exception as e:
            print('Error unpacking response:', e)
            print('Response:', step_response)
    else:
        print('Request failed with status code:', response.status_code, 'Response:', response.text)
        st.write('Request failed with status code:', response.status_code, 'Response:', response.text)
        return None
