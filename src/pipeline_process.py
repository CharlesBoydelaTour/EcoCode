import sys
sys.path.append('./')

from src.analysis_carbon import carbon_tracker
import src.improve_code as improve_code
import os 
import pandas as pd

def run_string_code(code:str):
    #function to run a string as code
    glob = {}
    exec(code, glob)

def run_file_code(file_path:str):
    #function to run a file as code
    with open(file_path, 'r') as f:
        code = f.read()
    glob = {}
    exec(code, glob)

def process(code_to_correct:str, country='FRA'):
    #if it exists, supress emissions.csv
    try:
        os.remove("emissions.csv")
    except:
        pass

    #function to run the code and track the carbon emissions
    @carbon_tracker
    def main_notcorrectec():
        #function to run the code to correct
        run_string_code(code_to_correct)
        #read the emissions.csv file and print the last line
    
    data_em = pd.read_csv("emissions.csv")
    #get emissions of the last line
    emissions_notcorrected = data_em.iloc[-1]["emissions"]
    
    corrected_code = improve_code.correct_code(code_to_correct)
    corrected_code_str = improve_code.select_code_from_output(corrected_code)
    print(f"{corrected_code_str}")
    
    @carbon_tracker
    def main_corrected():
        #function to run the corrected code
        run_string_code(corrected_code_str)
    
    data_em = pd.read_csv("emissions.csv")
    #get emissions of the last line
    emissions_corrected = data_em.iloc[-1]["emissions"]
    percent_reduction = (emissions_notcorrected - emissions_corrected) / emissions_notcorrected * 100
    
    return corrected_code_str, emissions_notcorrected, emissions_corrected, percent_reduction
    
if __name__ == "__main__":   
    code_to_correct = """
# Program to display the Fibonacci sequence up to n-th term

nterms = 5

# first two terms
n1, n2 = 0, 1
count = 0

# check if the number of terms is valid
if nterms <= 0:
   print('Please enter a positive integer')
# if there is only one term, return n1
elif nterms == 1:
   print(' sequence upto',nterms,':')
   print(n1)
# generate fibonacci sequence
else:
   print('Fibonacci sequence:')
   while count < nterms:
       print(n1)
       nth = n1 + n2
       # update values
       n1 = n2
       n2 = nth
       count += 1
 
    """
    
    corrected_code_str, emissions_notcorrected, emissions_corrected, percent_reduction = process(code_to_correct)
    #print corrected code
    print(f"{corrected_code_str}")
    #print % reduction  
    print(f"Percentage of emission reduction: {percent_reduction}%")