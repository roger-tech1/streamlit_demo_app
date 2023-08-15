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
st.set_page_config(page_title="BoM Verse Lookup")
st.title('BoM Verse Lookup')


# step request function
def step_request(input_query):
    headers = {
      'x-api-key': step_key,
      'Content-Type': 'application/json'  # Adjust the content type if needed
    }

    # formulate payload based on input query
    json_query = json.dumps(input_query)
    data = {
        "input": f'{{"query": {json_query}}}',
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
            body = json.loads(output['body'])
            result = body['result']
            st.write(result)
        except Exception as e:
            st.write('Error unpacking response:', e)
            st.write('Response:', step_response)
    else:
        st.write('Request failed with status code:', response.status_code, 'Response:', response.text)


with st.form('my_form'):
    text = st.text_area('Enter text:', 'Tell me the full verse that this snippet comes from - "And they came down and went forth upon the face of the earth"')
    submitted = st.form_submit_button('Submit')
    if submitted:
        with st.spinner('Wait for it...'):
            step_request(text)
