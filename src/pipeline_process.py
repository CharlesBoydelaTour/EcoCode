from analysis_carbon import carbon_tracker
import improve_code
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

if __name__ == "__main__":
     
    #if it exists, supress emissions.csv
    try:
        os.remove("emissions.csv")
    except:
        pass
        
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
    
    @carbon_tracker
    def main_notcorrectec():
        #function to run the code to correct
        run_string_code(code_to_correct)
        #read the emissions.csv file and print the last line
    
    df = pd.read_csv("emissions.csv")
    #get emissions of the last line
    emissions_notcorrected = df.iloc[-1]["emissions"]
    
    #Correct the code
    corrected_code = improve_code.correct_code(code_to_correct)
    corrected_code_str = improve_code.select_code_from_output(corrected_code)
    print(f"{corrected_code_str}")

    @carbon_tracker
    def main_corrected():
        #function to run the corrected code
        run_string_code(corrected_code_str)
    
    #emissions of the corrected code
    df = pd.read_csv("emissions.csv")
    emissions_corrected = df.iloc[-1]["emissions"]
    
    #print the % of emission saved
    print(f"% emission saved : {100*(emissions_notcorrected-emissions_corrected)/emissions_notcorrected}%")
    