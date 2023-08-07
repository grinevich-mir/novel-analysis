#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openai
import re

# Set up OpenAI API credentials
openai.api_key = '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'

# Define the chunk size and overlap
chunk_size = 5000  # Maximum token limit for GPT-3.5 is 4096
overlap = 500  # Number of tokens for overlapping context

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
    
    prompt = """Please extract the dialogues along with the speaker name and mood of the speaker from the following text. 
    If you couldn't find any dialogue then please don't make any artificial dialogue. 
    text: \n"""
    postpromt = """\n Please reply in a consistent format (dialogue in quotes followed by speaker name and mood of the speaker in brackets).
    If there is break in the dialogue then return it as two or more separate dialogues. If the name of speaker is not known then most probably he/she is Narrator."""
    
    dialogues = []
    for chunk in chunks:
        # Construct the conversation with overlapping context
        conversation = [
            {'role': 'system', 'content': 'You are an expert novel reader. You understand the context of dialogues and recognise the speaker of those dialogues.'},
            {'role': 'user', 'content': prompt+chunk+postpromt}
        ]

        # Call the OpenAI API to generate the response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=conversation,
            max_tokens=14000 # Adjust if using a different model with a different token limit
        )

        # Extract dialogues and metadata from the API response
        message = response['choices'][0]['message']
        if message['role'] == 'assistant':
            dialogues.append((message['role'], message['content']))

    return dialogues

# Example usage
chapter_file = './Data/Glimpse_Ch1.txt'  # Provide the path to the chapter file

dialogues = extract_dialogues_from_chapter(chapter_file)


#%% POst processing the results

# # Print the extracted dialogues
# for speaker, dialogue in dialogues:
#     print(f"{speaker}: {dialogue}")

# All reponses including the narator
tmp= [diag_tup[1].split("\n") for diag_tup in dialogues]

tmp2= [re.sub(r'^\d{1,2}\.\s*','',strings) for sublist in tmp for strings in sublist if (strings != '')]
dialogue_collec_Narr = [strings for strings in tmp2 if "Dialogue" not in strings] 

# Response without narrator
dialogue_collec = [re.sub(r'^\d{1,2}\.\s*', '', strings) for strings in dialogue_collec_Narr if "Narrator" not in strings]
    
print("Following are the dialogues including those of the Narrator also \n",dialogue_collec_Narr)
print("Following are the dialogues excluding Narrator's \n", dialogue_collec)

#%% Writing output to file

# writing file containing dialogues of Narrator also
with open('output_openai_raw.txt', 'w') as fil:
    for line in dialogue_collec_Narr:
        fil.write("%s\n" %line)

# writing file without dialogues of Narrator

with open('output_openai_fine.txt', 'w') as fil:
    for line in dialogue_collec:
        if "Unknown speaker" and "Narrator" and "Unknown" not in line:
            fil.write("%s\n" %line)




























