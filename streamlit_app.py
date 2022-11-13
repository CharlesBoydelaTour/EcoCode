import streamlit as st
import src.pipeline_process as pp

st.set_page_config(layout="wide")

#print current directory
import os
print(os.getcwd())

#with open('./app/style.css') as f:
#    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

col1, col2 = st.columns(2)
    
## Create 2 boxes in the page
#1st box is input code, 2nd box is output code
#input code 
code = col1.text_area("Input Code", height=500)
#code = col1.file_uploader("Enter your  code here", key="code")
country_code = col1.text_input("Enter your country code", key="country_code")
#output code
code_corrected = col2.code('''#Output Code''', language="python")

#When the button is clicked, the code is processed and the output is displayed in the 2nd box
if code:
    corrected_code_str, emissions_notcorrected, emissions_corrected, percent_reduction = pp.process(code_to_correct=code, country=country_code)
    code_corrected.code(corrected_code_str, language="python")
    col2.text("Improvement: {}%".format(percent_reduction))