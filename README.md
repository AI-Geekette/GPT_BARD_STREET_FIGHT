# GPT & BARD CONVERSATIONAL APP
Can you guess who would win the conversation if we put chatgpt and bard to a conversational challenge?

## Run Locally

Clone the project

```bash
  git clone https://github.com/AI-Geekette/GPT_BARD_STREET_FIGHT.git
```

Create a python env

```bash
cd GPT_BARD_STREET_FIGHT/
python -m venv bardgpt_env
source ./bardgpt_env/bin/activate
```

Install requirements
```bash
  pip3 install -r requirements.txt

```

Add .env file to the project stucture

```bash
  touch .env
```

Add your OPEN_API_KEY and BARD cookie to .env file
```bash
BARD_API_KEY=<put_key_here_no_quotes>
OPEN_API_KEY=<put_key_here_no_quotes>
```


Run streamlit app
```bash
streamlit run main.py
```

Go to streamlit page on your browser
Give the bots a prompt about a conversation topic

Watch them talk

You can change the conversation time limit in while loop condition: default is 30 seconds
![code snippet](media/code_gpt_bard.png)

## Link to Bard API repo

https://github.com/dsdanielpark/Bard-API/blob/main/README.md

Check on Bard API repo how to get the Bard API "Key", it's actually  __Secure-1PSID
Do not expose it, it's your browser ad cookies, use it at your own risk

## ⚠️ Warning

If you clone this repo and push to your github or fork this repo, do NOT push you API KEYS
Use and .env file and .gitignore

.gitignore content

```bash
bardgpt_env/*
.env
```

## BARD & CHATGPT Conversation notes in Notion.so

Give it a read if you ae curious about the conversation betweent the two most controvertial LLMs about free will and determinism.

https://sandy-concrete-1af.notion.site/ChatGPT-vs-BARD-update-enhancement-64b5e38d61944416b66d8ccd96c39170?pvs=4