#https://docs.streamlit.io/get-started/fundamentals/main-concepts
#https://github.com/streamlit

import openai
from openai import OpenAI, AzureOpenAI
import re
import streamlit as st
#from promptsmine import get_system_prompt
#from snowflake.snowpark.session import Session
import json

import argparse
import logging
import os
import sys
from dotenv import load_dotenv

from snowflake.snowpark import Session
from snowflake.snowpark.exceptions import *


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import time

load_dotenv()


st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))
#st.table(dataframe)
st.line_chart(dataframe)

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

#st.map(map_data)

x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

st.text_input("Your name", key="name")
# You can access the value at any point with:
st.session_state.name


if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)
add_selectbox 
# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)
add_slider

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")


'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(20):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'


if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1

st.header(f"This page has run {st.session_state.counter} times.")
st.button("Run it again")


#https://stackoverflow.com/questions/77395177/how-to-set-value-to-a-session-state-in-streamlits
# Define and initialize the data so that it is easier to update.
DATA_INIT = {
    "asset": {
        "asset1": {
            "cash_on_hand": 0,
            "account_receivable": 0
        },
        "asset2": {
            "cash_on_hand": 0,
            "account_receivable": 0
        }
    },
    "liabilities": {
        "liabilities1": {
            'current': 0
        },
        "liabilities2": {
            'current': 0
        }
    }
}


if 'data' not in st.session_state:
    st.session_state['data'] = DATA_INIT

st.markdown('### Data Entry')
with st.form('accounting', clear_on_submit=True):
    coh = st.number_input('Asset 1 / Cash On Hand', value=0.0, step=0.01)
    ar = st.number_input('Asset 1 / Account Receivable', value=0.0, step=0.01)

    # add other input here.

    submit = st.form_submit_button('save')

if submit:
    st.session_state['data']['asset']['asset1']['cash_on_hand'] += coh
    st.session_state['data']['asset']['asset1']['account_receivable'] += ar

st.markdown('### Current Data')
with st.expander('Current data', expanded=False):
    st.json(st.session_state['data'])


# conn = st.connection("snowflake_bsc")
# query="""select r.sobjecttype, r.name, count(*) as count from (				
# select id, recordtypeid, 'account'     as tablesource from cdl.salesforce_vw.account      union all				
# select id, recordtypeid, 'contact'     as tablesource from cdl.salesforce_vw.contact      union all				
# select id, recordtypeid, 'lead'        as tablesource from cdl.salesforce_vw.lead         union all				
# select id, recordtypeid, 'opportunity' as tablesource from cdl.salesforce_vw.opportunity) a				
# left join cdl.salesforce_vw.recordtype r on a.recordtypeid=r.id				
# group by 1,2				
# order by 1,2				
# """
# df = conn.query(query)
# st.dataframe(df)



# Initialize the chat messages history
#client = OpenAI(api_key=st.secrets.OPENAI_API_KEY)
if "messages" not in st.session_state:
    # system prompt includes table information, rules, and prompts the LLM to produce
    # a welcome message to the user.
    st.session_state.messages = [{"role": "system", "content": 'Hello, I am the system.'}]

# Prompt for user input and save
if prompt := st.chat_input():
    message = {"role": "user", "content": prompt}
    st.session_state.messages.append(message) 

# display the existing chat messages
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "results" in message:
            st.dataframe(message["results"])
        if "fig" in message:
            st.write(message["fig"])

# If last message is not from assistant, we need to generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response = "My reply is " + prompt if prompt is not None else " "
        #resp_container = st.empty()
        #resp_container.markdown(response)
        st.markdown(response)

        message = {"role": "assistant", "content": response}
        message["results"] = np.round(np.random.rand(3,4),2)
        st.dataframe(message["results"])

        #Visualize result
        df=pd.DataFrame(message["results"])
        df=df.sort_values(df.columns[-1],  ascending=True) #sort by last column (usually freequency)
        #st.bar_chart(df, x=df.columns[0], y=df.columns[1])
        #fig=px.bar(df, x=df.columns[0], y=df.columns[1], orientation='h')
        #fig=df.plot.barh(x=df.columns[0], y=df.columns[1])
        if df.shape[1]>=2 and np.issubdtype(df[df.columns[-1]].dtype, np.number): 
            fig, ax = plt.subplots()
            ax.barh(df[df.columns[0]], df[df.columns[-1]],  align='center')
            #st.pyplot(fig, clear_figure=False)
            message["fig"]=fig
            st.write(message["fig"])
        st.session_state.messages.append(message) 
        
st.write(st.session_state)

#copilot:  Certainly! When working with Streamlit, you can save your app’s output to an HTML page using a couple of different approaches: st-static-export


