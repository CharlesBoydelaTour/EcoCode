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
    
## Create 2 boxes in the page
#1st box is input code, 2nd box is output code
#input code either text or file
code = col1.text_area("Input code", height=500)
code2 = col1.file_uploader("Upload file", type=['py'])
#code = col1.file_uploader("Enter your  code here", key="code")
country_code = col1.text_input("Enter your country code", key="country_code")
#output code
code_corrected = col2.code('''#Output Code''', language="python")

#When the button is clicked, the code is processed and the output is displayed in the 2nd box
if code:
    corrected_code_str, emissions_notcorrected, emissions_corrected, percent_reduction = pp.process(code_to_correct=code, country=country_code)
    code_corrected.code(corrected_code_str, language="python")
    col2.text("Improvement: {}%".format(percent_reduction))

if code2:
    stringio = StringIO(code2.getvalue().decode("utf-8"))
    code_to_read = stringio.read()
    col2.text("Improvement: {}%".format(code_to_read))
    corrected_code_str, emissions_notcorrected, emissions_corrected, percent_reduction = pp.process(code_to_correct=code_to_read, country=country_code)
    code_corrected.code(corrected_code_str, language="python")
    col2.text("Improvement: {}%".format(percent_reduction))