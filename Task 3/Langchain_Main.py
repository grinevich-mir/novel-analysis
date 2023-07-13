#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


def initialize_chat_model(api_key):
    chat_model = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo-16k",
        max_tokens=14000,
        openai_api_key=api_key,
        request_timeout=1500
    )
    return chat_model


def create_system_message_prompt(template):
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    return system_message_prompt


def create_human_message_prompt(template):
    human_message_prompt = HumanMessagePromptTemplate.from_template(template)
    return human_message_prompt


def create_chat_prompt(system_message_prompt, human_message_prompt):
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    return chat_prompt


def extract_dialogues_from_chapter(chapter_file, chat_chain):
    chunk_size = 4500
    overlap = 500
    with open(chapter_file, 'r') as file:
        chapter_text = file.read()

    chunks = []
    start = 0
    end = chunk_size
    while start < len(chapter_text):
        chunks.append(chapter_text[start:end])
        start = end - overlap
        end = start + chunk_size

    dialogues = []
    for chunk in chunks:
        response = chat_chain.run(chnk=chunk)
        dialogues.append(response)

    return dialogues


def process_dialogues(dialogues):
    dialogue_collection_raw = []

    for diag in dialogues:
        tmp = diag.split("\n")
        for strngs in tmp:
            dialogue_collection_raw.append(strngs)

    return dialogue_collection_raw


def write_dialogues_to_file(dialogue_collection_raw, output_raw_file):
    with open(output_raw_file, 'w') as file:
        for line in dialogue_collection_raw:
            file.write("%s\n" % line)

def main():
    api_key = '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'

    chat_model = initialize_chat_model(api_key)

    system_template = "You are an expert novel reader. You can recognize various sound effects in the text such as footsteps, something dropping on the floor, gunfire etc."
    system_message_prompt = create_system_message_prompt(system_template)

    human_template = "Please extract lines from the following text which contain sound effects along with the name of the sound effect itself: \n {chnk} \n Please reply in a consistent format (text containing the sound effects followed by the name of the sound effect in brackets)."
    human_message_prompt = create_human_message_prompt(human_template)

    chat_prompt = create_chat_prompt(system_message_prompt, human_message_prompt)

    chat_chain = LLMChain(llm=chat_model, prompt=chat_prompt)

    chapter_file = './Data/chapter_1.txt'  # Provide the path to the chapter file

    dialogues = extract_dialogues_from_chapter(chapter_file, chat_chain)

    dialogue_collection_raw = process_dialogues(dialogues)

    print("Following are the sounds and sources of those spunds also:\n", dialogue_collection_raw)

    output_raw_file = 'output_langchain_Sounds_task3.txt'
   
    write_dialogues_to_file(dialogue_collection_raw, output_raw_file)

if __name__ == "__main__":
    main()
