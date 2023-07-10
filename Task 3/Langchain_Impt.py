#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

api_key = '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'

chat = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k", max_tokens=14000, openai_api_key=api_key, request_timeout=1500)

template = "You are an expert novel reader. You can reconise various sound effects in the text such as footsteps, something dropping on the floor, gunfire etc."

system_message_prompt = SystemMessagePromptTemplate.from_template(template)

human_template = "Please extract lines from the following text which contain sound effects along with the name of sound effect itself: \n {chnk} \n Please reply in a consistent format (text containing the sound effects followed by the name of sound effect in brackets)."

human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

chain = LLMChain(llm=chat, prompt=chat_prompt)

# Define the chunk size and overlap
chunk_size = 3000  # Check Maximum token limit for the model used

overlap = 400  # Number of tokens for overlapping context

def extract_dialogues_from_chapter(chapter_file):
    with open(chapter_file, 'r') as file:
        chapter_text = file.read()

    # Split the chapter into overlapping chunks
    chunks = []
    start = 0
    end = chunk_size
    while start < len(chapter_text):
        chunks.append(chapter_text[start:end])
        start = end - overlap
        end = start + chunk_size
    
    dialogues = []
    for chunk in chunks:
        response = chain.run(chnk=chunk)
        dialogues.append(response)
    
    return dialogues
        
chapter_file = './Data/chapter_1.txt'  # Provide the path to the chapter file

dialogues = extract_dialogues_from_chapter(chapter_file)

#%% POst processing the results

# # Print the extracted dialogues
# for speaker, dialogue in dialogues:
#     print(f"{speaker}: {dialogue}")
dialogue_collection_raw=[]
dialogue_collection_speakers=[]
# All reponses including the narator
for diag in dialogues:
    tmp = diag.split("\n")
    for strngs in tmp:
        dialogue_collection_raw.append(strngs)
        if "Unknown speaker" and "Narrator" and "Unknown" not in strngs:
            dialogue_collection_speakers.append(strngs)

# Response without narrator
# dialogue_collec = [re.sub(r'^\d{1,2}\.\s*', '', strings) for strings in dialogue_collec_Narr if "Narrator" not in strings]


    
print("Following are the dialogues including those of the Narrator also \n",dialogue_collection_raw)
# print("Following are the dialogues excluding Narrator's \n", dialogue_collec)

#%% Writing output to file

# writing file containing dialogues of Narrator also
with open('output_langchain_raw.txt', 'w') as fil:
    for line in dialogue_collection_raw:
        fil.write("%s\n" %line)

# writing file without dialogues of Narrator

with open('output_langchain_fine.txt', 'w') as fil:
    for line in dialogue_collection_speakers:
        fil.write("%s\n" %line)















#%% Output formating

