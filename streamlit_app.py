import streamlit as st
import src.pipeline_process as pp
from io import StringIO

st.set_page_config(layout="wide")

#print current directory
import os
print(os.getcwd())

#with open('./app/style.css') as f:
#    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

col1, col2 = st.columns(2)
#put title at column 1 (Input) and column 2 (Output)
with col1:
    st.title('Input')
with col2:
    st.title('Recommendation')
#set a separator element between the two columns
st.markdown('---')

## Create 2 boxes in the page
#1st box is input code, 2nd box is output code
#input code either text or file
col1.subheader('Add country code and Input Code (Text or File)')
country_code = col1.text_input("Enter your country code", key="country_code")

code = col1.text_area("Input code", height=500)
code2 = col1.file_uploader("Upload file", type=['py'])

#output code
code_corrected = col2.code('''#Output Code''', language="python")

#When the button is clicked, the code is processed and the output is displayed in the 2nd box
if code:
    corrected_code_str, emissions_notcorrected, emissions_corrected, percent_reduction = pp.process(code_to_correct=code, country=country_code)
    code_corrected.code(corrected_code_str, language="python")
    col2.text("Co2 emission saved: {}%".format(percent_reduction))
    col2.text("Co2 emission left with code based in {}: {} kg".format(country_code, emissions_notcorrected))
if code2:
    stringio = StringIO(code2.getvalue().decode("utf-8"))
    code_to_read = stringio.read()
    corrected_code_str, emissions_notcorrected, emissions_corrected, percent_reduction = pp.process(code_to_correct=code_to_read, country=country_code)
    code_corrected.code(corrected_code_str, language="python")
    col2.text("Co2 emission saved: {}%".format(percent_reduction))
    col2.text("Co2 emission left with code based in {}: {} kg".format(country_code, emissions_notcorrected))