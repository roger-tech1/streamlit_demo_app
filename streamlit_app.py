import requests
import os
import json
import streamlit as st
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()
step_endpoint_url = os.environ.get('STEP_ENDPOINT_URL')
step_arn = os.environ.get('STEP_ARN')
step_key = os.environ.get('STEP_API_KEY')

# load in streamlit
st.set_page_config(page_title="Scripture Keyword Lookup API")
st.title('Scripture Keyword Lookup API')

checks = st.columns(3)
with checks[0]:
    useBoM = st.checkbox('Book of Mormon', value=True)
with checks[1]:
    useNT = st.checkbox('New Testament', value=True)
with checks[2]:
    useOT = st.checkbox('Old Testament', value=True)


# step request function
def step_request(input_query):
    headers = {
      'x-api-key': step_key,
      'Content-Type': 'application/json'  # Adjust the content type if needed
    }

    # formulate payload based on input query
    json_query = json.dumps(input_query)
    data = {
        "input": f'{{"query": {json_query}, "useBoM": "{str(useBoM)}", "useNT": "{str(useNT)}", "useOT": "{str(useOT)}"}}',
        "name": "MyExecution",
        "stateMachineArn": step_arn
    }

    # make request
    response = requests.post(step_endpoint_url, json=data, headers=headers, timeout=900)

    # Check the response
    if response.status_code == 200:
        # unpack response and return
        try:
            step_response = response.json()
            output = json.loads(step_response['output'])
            
            # print('Output:', output)
 
            # loop over returned volumes
            for volume_data in output:
                try:
                    volume_name = volume_data['volume']
                    st.write('---')
                    st.write(f"""
                    Results from volume: {volume_name}
                    ---
                    ---
                    """)

                    # loop over returned verses in result
                    result = volume_data['result']
                    if len(result) == 0:
                        st.write('No results found')
                    else:
                        for verse_data in result:
                            verse = verse_data['verse_content']
                            st.write(f'**Verse**: {verse}')
                            st.write(f'**Word numbers**: {verse_data["word_numbers"]}')
                            st.write(f'**Verse number**: {verse_data["verse_number"]}')
                            st.write(f'**Chapter**: {verse_data["chapter"]}')
                            st.write(f'**Book**: {verse_data["book"]}')
                            st.write('---')
                except Exception as e:
                    print('Error unpacking volume data:', e)
                    print('Volume data:', volume_data)
        except Exception as e:
            st.write('Error unpacking response:', e)
            st.write('Response:', step_response)
    else:
        st.write('Request failed with status code:', response.status_code, 'Response:', response.text)


with st.form('my_form'):
    text = st.text_area('Enter word:', 'chicken')
    submitted = st.form_submit_button('Submit')
    if submitted:
        with st.spinner('Wait for it...'):
            step_request(text)
