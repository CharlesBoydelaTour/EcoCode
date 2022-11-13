import sys
sys.path.append('./')

from src.analysis_carbon import carbon_tracker
import src.improve_code as improve_code
import os 
import pandas as pd

def run_string_code(code:str):
    #function to run a string as code
    exec(code)

def run_file_code(file_path:str):
    #function to run a file as code
    with open(file_path, 'r') as f:
        code = f.read()
    exec(code)

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
def is_pair(n): 
        #this function returns true if n is a pair number and false if it is odd \n
        if n == 2:  
            return True 
        elif n == 4:
            return True 
        elif n == 6: 
            return True 
        else : 
            return False 
for i in range(100000): 
        is_pair(i) 
    """
    
    corrected_code_str, emissions_notcorrected, emissions_corrected, percent_reduction = process(code_to_correct)
    #print corrected code
    print(f"{corrected_code_str}")
    #print % reduction  
    print(f"Percentage of emission reduction: {percent_reduction}%")