import requests
import streamlit as st
import os
step_arn = os.environ.get('STEP_ARN')
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

  print(headers) 
  # formulate payload based on input query
  data =  {
      "input": f'{"query": {input_query}}',
      "name": "MyExecution",'"' + step_arn + '"'
      "stateMachineArn": "arn:aws:states:us-west-2:453900232671:stateMachine:BoM_QA"
    }
  
  print(data)