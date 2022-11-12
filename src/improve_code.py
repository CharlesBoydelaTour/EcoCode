### Call the openai api to improve code given as a string, and return the improved code as a string ###

import getpass
import os
from typing import List

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def completion_with_backoff(**kwargs):
    return openai.Completion.create(**kwargs)

def correct_code(
    chunks: str
) -> list:
    """
    It takes a chunk of code as text and returns the corrected code
    :param chunks: the text to be corrected
    :type chunks: str
    :return: Corrected code as a string
    """
    correction = completion_with_backoff(
        model="text-davinci-002",
        prompt=f'Rewrite the code in excerpt to make it more efficient.'
        f"\n###\nExcerpt:```{chunks}```\n###\n Corrected code:",
        temperature=0,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    corrected_code = correction["choices"][0]["text"]
    #print(f"{corrected_code}")
    return corrected_code

def select_code_from_output(output:str):
    corrected_code_str = ""
    to_select = False
    for line in output.splitlines():
        if line =="```":
            to_select = True
            continue
        if to_select:
            corrected_code_str += line + '\n'
    #if empty then return original code
    if corrected_code_str == "":
        return output
    return corrected_code_str

if __name__ == "__main__":
    code_to_correct = """
    def is_pair(n): \n
        #this function returns true if n is a pair number and false if it is odd \n
        if n == 2:  \n
            return True \n
        elif n == 4: \n
            return True \n
        elif n == 6: \n
            return True \n
        else : \n
            return False \n
    """
    corrected_code = correct_code(code_to_correct)
    corrected_code_str = select_code_from_output(corrected_code)
    print(f"{corrected_code_str}")