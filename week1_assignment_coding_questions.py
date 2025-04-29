# imports
import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

MODEL_GPT = 'gpt-4o-mini'
MODEL_LLAMA = 'llama3.2'

# set up environment
load_dotenv("C:/Users/ashetty/Documents/Personal_Git/LLM/llm_engineering_personal/llm_engineering_course/.env")
api_key = os.getenv('OPENAI_API_KEY')
llama_key = os.getenv('LLAMA_KEY')
if not api_key:
    print("Error: OPENAI_API_KEY environment variable is not set.")
    sys.exit(1)



default_question = """
Please explain what this code does and why:
yield from {book.get("author") for book in books if book.get("author")}
"""

def create_message(question):
    return [
        {"role": "user", "content": question},
        {"role": "system", "content": "You are a Software developer with the knowledge of all the prominent coding languages."}
    ]

def ask_model(model, model_name, question):
    stream = model.chat.completions.create(
        model=model_name,
        messages=create_message(question),
        stream=True,
        temperature=0.5,
        max_tokens=1000
    )
    result = ''
    # result = response.choices[0].message.content
    for chunk in stream:
        if hasattr(chunk, 'choices') and chunk.choices and hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
            if chunk.choices[0].delta.content:
                result += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end='', flush=True)
    return result

def run():
    # Get gpt-4o-mini to answer, with streaming
    model = OpenAI()
    result = ask_model(model, MODEL_GPT, default_question)
    # print("GPT-4o-Mini response:", result)


    # Get Llama 3.2 to answer
    model = OpenAI(base_url='http://localhost:11434/v1', api_key=llama_key)
    result = ask_model(model, MODEL_LLAMA, default_question)
    # print("ollama response:", result)

run()
