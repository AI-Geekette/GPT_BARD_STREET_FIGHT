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

# tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
bard = Bard(timeout=30)

def askbard(msg):  
    resp = bard.get_answer(msg)['content']
    return resp


# def count_tokens(text):
#     tokens = tokenizer.tokenize(text)
#     return len(tokens)


# Define the conversation history as a global variable
conversation_history = []
max_gpt_tokens = 1000
guide_prompt = """You are in a conversation with a very smart chatbot about  free will vs determinism.
    I want you to engage in the conversation and be reasonably challenging. Please generate a response based on 
    the following message: """
def chat_with_gpt(message):
    conversation_history.append(("Init_prompt", message))
    # Generate GPT response
    response = openai.Completion.create(
        model="text-curie-001",
        prompt= message,
        temperature=0.7,
        max_tokens=max_gpt_tokens,
        frequency_penalty=1,
        presence_penalty=1
    )
    gpt_response = response.choices[0].text.strip()

    conversation_history.append(("GPT", gpt_response))  # Add GPT response to the conversation history

    return gpt_response

def main():
    st.title("BARD & GPT Chat")

    # User input area
    init_prompt = ""
    user_input = st.text_input("Init_prompt", init_prompt)
    init_chat = True
    # Process user input and display conversation
    if user_input:
        # Start conversation timer
        start_time = time.time()
        i = 0
        while (time.time() - start_time) < 30:
            if(init_chat==True):
                # Send user message to BART API
                bard_response = askbard(user_input)
                print(f"BARD{i} : ", bard_response)
                # Add BART response to the conversation history
                conversation_history.append(("BARD", bard_response))
                st.text_area(f"BARD{i} : ", value=bard_response, disabled=True)
                
                # Generate GPT response
                gpt_response = chat_with_gpt(bard_response)
                print(f"GPT{i} : ",gpt_response)
                # Add GPT response to the conversation history
                conversation_history.append(("GPT", gpt_response))
                st.text_area(f"GPT{i} : ", value=gpt_response, disabled=True)
                init_chat = False
            else:
                # token_count = count_tokens(bard_response)
                # print("token_count: ", token_count)
                # if(token_count>max_gpt_tokens):
                #     print('Bard long: ', bard_response)
                #     bard_response = chat_with_gpt(bard_response+ "\n Tl;dr:")
                #     print('Bard short: ', bard_response)
                # Generate GPT response
                if(gpt_response==""):
                    gpt_response = "Can you explain more concisely please and suggest a more thorough question?"
                    print(f"GPT{i} : ",gpt_response)
                    # Add GPT response to the conversation history
                    conversation_history.append(("GPT", gpt_response))
                    st.text_area(f"GPT{i} : ", value=gpt_response, disabled=True)
                    
                # Send user message to BART API
                bard_response = askbard(gpt_response)
                print(f"BARD{i} : ",bard_response)
                # Add BART response to the conversation history
                conversation_history.append(("BARD", bard_response))
                st.text_area(f"BARD{i} : ", value=bard_response, disabled=True)
                
                # Generate GPT response
                gpt_response = chat_with_gpt(bard_response)
                print(f"GPT{i} : ",gpt_response)
                # Add GPT response to the conversation history
                conversation_history.append(("GPT", gpt_response))
                st.text_area(f"GPT{i} : ", value=gpt_response, disabled=True)
            i+=1
            
            # Countdown timer
            elapsed_time = time.time() - start_time
            remaining_time = max(30 - elapsed_time, 0)
            st.text(f"Time remaining: {int(remaining_time)} seconds")
            st.empty()

if __name__ == "__main__":
    main()