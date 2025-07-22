# # ai_core.py
# import os
# import google.generativeai as genai
#
# genai.configure(api_key=os.getenv("saksham api"))
# model = genai.GenerativeModel('gemini-pro')
#
#
# def generate_contract_code(prompt: str) -> str:
#     """
#     Uses Gemini to generate a Solidity smart contract from a natural language prompt.
#     """
#     instructional_prompt = f"""
#     Based on the following request, generate a secure and efficient Solidity smart contract.
#     The contract should be written for Solidity version 0.8.20.
#     It must be self-contained in a single file and have no external dependencies unless specified.
#     Add comments explaining the purpose of the contract and its primary functions.
#
#     User Request: "{prompt}"
#
#     Generate the Solidity code now.
#     """
#
#     response = model.generate_content(instructional_prompt)
#
#     # Clean up the response to extract only the code block
#     cleaned_code = response.text.replace("``````", "").strip()
#
#     return cleaned_code

import os
import cohere
from dotenv import load_dotenv

load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

def generate_contract_code(prompt):
    response = co.generate(
        model='command-r-plus',  # or 'command-light' for faster responses
        prompt=prompt,
        max_tokens=1000,
        temperature=0.5
    )
    return response.generations[0].text.strip()
