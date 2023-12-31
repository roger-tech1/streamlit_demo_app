import requests
import os
import re
import streamlit as st
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()
lambda_endpoint_url = os.environ.get('WIKITIONARY_ENDPOINT_URL')
lambda_api_key = os.environ.get('WIKITIONARY_API_KEY')

# load in streamlit
st.set_page_config(page_title="BoM Verse Lookup")
st.title('Wiktionary api test')


# lambda request function
def lambda_request(word):
    headers = {
      'x-api-key': lambda_api_key,
      'Content-Type': 'application/json'  # Adjust the content type if needed
    }

    # formulate payload based on input query
    data = {
        "word": word
    }

    # make request
    response = requests.post(lambda_endpoint_url, json=data, headers=headers, timeout=300)

    # Check the response
    if response.status_code == 200:
        # unpack response and return
        try:
            _response = response.json()
            output = _response['data']
            if len(output) == 0:
                st.write('No results found.')
                return
            else:
                # find maximum length of definitions 
                max_def_len = max([len(d['definitions']) for d in output])
                if max_def_len == 0:
                    st.write('No results found.')
                    return

                for d in output:
                    keys = list(d.keys())
                    values = list(d.values())
                    for k, v in zip(keys, values):
                        st.write(k, v)
                    st.write('---')
        except Exception as e:
            st.write('Error unpacking response:', e)
            st.write('Response:', response)
    else:
        st.write('Request failed with status code:', response.status_code, 'Response:', response.text)


def preprocess_text(text):
    # Remove punctuation and specified symbols using regular expressions
    text = re.sub(r'[^\w\s]|[\n\t\r\f\v\u2028\u2029]', '', text)

    # Convert text to lowercase
    text = text.lower()

    return text

with st.form('my_form'):
    # input query text
    text = st.text_area('Enter text:', 'caramel')

    # cleanup text - remove punctuation, lowercase, newline symbols, etc., use regular expressions
    text = preprocess_text(text)

    submitted = st.form_submit_button('Submit')
    if submitted:
        with st.spinner('Searching...'):
            lambda_request(text)