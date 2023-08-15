import requests
import streamlit as st
import os
step_key = os.environ.get('STEP_API_KEY')
st.set_page_config(page_title="BoM Verse Lookup")
st.title('BoM Verse Lookup')

# step request function
def step_request(input_query):
  endpoint_url = 'https://p1oiumm9wc.execute-api.us-west-2.amazonaws.com/dev'
  headers = {
    'x-api-key': step_key,
    'Content-Type': 'application/json'  # Adjust the content type if needed
  }

  # formulate payload based on input query
  data =  {
      "input": f'{"query": {input_query}}',
      "name": "MyExecution",
      "stateMachineArn": "arn:aws:states:us-west-2:453900232671:stateMachine:BoM_QA"
    }

  print(f'Payload: {data}')
  print(f'Headers: {headers}')
  
  # make request
  response = requests.post(endpoint_url, json=data, headers=headers)

  # Check the response
  if response.status_code == 200:
      st.write(response)
  else:
      st.write('Request failed with status code:', response.status_code, 'Response:', response.text)

def generate_response(input_text):
  response = query_bom(input_text)
  st.write(response)

with st.form('my_form'):
  text = st.text_area('Enter text:', 'Tell me the full verse that this snippet comes from - "And they came down and went forth upon the face of the earth"')
  submitted = st.form_submit_button('Submit')
  if submitted:
    with st.spinner('Wait for it...'):
      generate_response(text)
