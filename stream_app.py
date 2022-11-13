import os
import json
import requests
import openai
import numpy as np
import streamlit as st
import pandas as pd

from datetime import datetime
from transformers import GPT2TokenizerFast
#from streamlit_webrtc import WebRtcMode


# OpenAI creds:
k = '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'
openai.organization = "org-0hLSeCcoBZl9cuiCloL2uPRC"
openai.api_key = k
COMPLETIONS_MODEL = "text-davinci-002"

COMMENT_TEMPLATE_MD = """{} - {}
> {}"""

aws_data = pd.read_csv('impact.csv')
aws_data = aws_data[aws_data['provider']=='aws']
aws_data = aws_data[['region', 'country_name', 'city', 'impact']]

REGION_PROMPT = """

Consider the table below:
{pd_table}
-----
1. In the table above, what are the three closest cities to {region}?
2. Sort these by lowest impact? Be sure to include the impact associated.
3. What is your recommendation for the best climate friendly option? lowest impact

Answers:

"""

def question_page():
    st.header("Q&A")
    st.write("**Ask a question about the climate friendliness of the diferent hosting regions**")
    temp = st.number_input('Temperature of answer')
    n_char = st.number_input('Length of answer', 100)
    form2 = st.form("comment2")
    question = form2.text_area("Question")
    #comment = form.text_area("Comment")
    submit2 = form2.form_submit_button("Get an answer")

    if submit2:
        st.write("Answer:")
        text = get_gpt_answer(question, temp, int(n_char))
        st.write(text)

def main_page():
    st.header("Region Summarizer")
    st.dataframe(aws_data)
    st.write("**Input your region for best climate friendly options**")
    form = st.form("comment")
    region = form.text_input("Region")
    #comment = form.text_area("Comment")
    submit = form.form_submit_button("Submit")

    if submit:
        st.write("Submitted")
        formated_prompt = REGION_PROMPT.format(
                                pd_table=aws_data.to_string(), region=region)
        text = get_gpt_answer(formated_prompt)
        st.write(text)

def request_page():
    st.header("Request to Electricity Maps")
    zone = st.text_input("zone")
    url = "https://api-access.electricitymaps.com/tw0j3yl62nfpdjv4/carbon-intensity/forecast?zone="
    headers = {
      "X-BLOBR-KEY": "xeQEO59SITDrUW8DQJrskr3dWngPG8di"
    }

    #response = requests.get(url, headers=headers)
    #data = json.loads(response.text)
    f = open('sim_data.json')
    data = json.load(f)
    f.close()
    forecast_df = pd.DataFrame(data['forecast'])[:24]
    forecast_df['datetime'] = pd.to_datetime(forecast_df['datetime'])
    forecast_df['date'] = forecast_df['datetime'].dt.date
    forecast_df['hour'] = forecast_df['datetime'].dt.hour
    forecast_df['price'] = np.random.randint(150,270, len(forecast_df))
    str_data = forecast_df[['carbonIntensity', 'hour', 'date', 'price']].to_string(index=False)
    st.write("**Forecast per hour of region**")
    st.dataframe(forecast_df)
    df_plot = forecast_df[['datetime','carbonIntensity','price']].set_index('datetime').copy()
    st.line_chart(df_plot)
    FORECAST_PROMPT = """
    Answer the following as truthfully as possible, if you do not know the answer say "I dont know".
    Consider the following forecast:
    {data_string}
    ---
    What is the best time to run a python script for approx 30 minutes?
    Consider the carbon intensity and the lowest price, provide an explanation and reference the price and carbon intensity.
    Explain step by step.

    """.format(data_string=str_data)
    temp = st.number_input('Temperature of answer')
    n_char = st.number_input('Length of answer', 100)
    if st.button('Get recommendation'):
        text = get_gpt_answer(FORECAST_PROMPT, temp, int(n_char))
        print(text)
        st.write(text)


def get_gpt_answer(prompt, temperature=0.0, max_tokens=300):
    return openai.Completion.create(
    prompt=prompt,
    temperature=0.2,
    max_tokens=max_tokens,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    model=COMPLETIONS_MODEL)["choices"][0]["text"].strip(" \n")

def main():
    
    page_names_to_funcs = {
    "Main Page": main_page,
    "Ask a question": question_page,
    "Request ": request_page
    }
    selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
    page_names_to_funcs[selected_page]()

main()
