from bardapi import Bard
import openai
import streamlit as st
import os
import time
from transformers import GPT2Tokenizer
from dotenv import load_dotenv
load_dotenv()

BARD_API_KEY =os.getenv("BARD_API_KEY")
os.environ['_BARD_API_KEY'] = BARD_API_KEY

OPEN_API_KEY = os.getenv("OPEN_API_KEY")
openai.api_key = OPEN_API_KEY

bard = Bard(timeout=30)

def askbard(msg):  
    resp = bard.get_answer(msg)['content']
    return resp

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

def count_tokens(text):
    tokens = tokenizer.tokenize(text)
    return len(tokens)

def reduce_prompt(prompt, max_tokens=2000):
    tokenized_prompt = tokenizer.encode(prompt, add_special_tokens=False)
    if len(tokenized_prompt) < max_tokens:
        return prompt

    reduced_prompt_tokens = tokenized_prompt[:max_tokens]
    reduced_prompt = tokenizer.decode(reduced_prompt_tokens)
    return reduced_prompt


# Define the conversation history as a global variable
conversation_history = []
max_gpt_tokens = 2000
guide_prompt = """You are in a conversation with a very smart chatbot about  free will vs determinism.
    I want you to engage in the conversation and be reasonably challenging. Please generate a response based on 
    the following message: """
def chat_with_gpt(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": guide_prompt}, 
                {"role": "user", "content": message}
            ]
        )
    gpt_response = response['choices'][0]['message']['content']
    conversation_history.append(("GPT", gpt_response))  # Add GPT response to the conversation history

    return gpt_response

def main():
    st.title("BARD & GPT Chat")

    # User input area
    init_prompt = ""
    user_input = st.text_input("Init_prompt", init_prompt)
    # Process user input and display conversation
    if user_input:
        # Set the first prompt to initiate the conversation to user_input prompt
        bard_response = user_input
        # Start conversation timer
        start_time = time.time()
        i = 0
        while (time.time() - start_time) < 30:
            # Send user message to BART API 
            # Generate GPT response
            gpt_response = chat_with_gpt(bard_response)
            print(f"GPT{i} : ",gpt_response)
            if (gpt_response==""):
                gpt_response = "can you briefly summarize your last message?"
            # Add GPT response to the conversation history
            conversation_history.append(("GPT", gpt_response))
            st.text_area(f"GPT{i} : ", value=gpt_response, disabled=True)
            
            bard_response = askbard(gpt_response)
            print(f"BARD{i} : ", bard_response)
            # Add BART response to the conversation history
            conversation_history.append(("BARD", bard_response))
            st.text_area(f"BARD{i} : ", value=bard_response, disabled=True)
            
            if(count_tokens(bard_response)>2000):
                bard_response  = reduce_prompt(bard_response)
                print("Reduced: ",bard_response)
            
            # Countdown timer
            elapsed_time = time.time() - start_time
            remaining_time = max(30 - elapsed_time, 0)
            st.text(f"Time remaining: {int(remaining_time)} seconds")
            st.empty()
                
            i+=1
            
            
if __name__ == "__main__":
    main()