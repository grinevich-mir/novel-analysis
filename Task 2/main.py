#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from source import utility_func
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


if __name__ == "__main__":
    
    api_key = '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'

    chat_model = utility_func.initialize_chat_model(api_key)

    system_template = """"You are an expert novel reader. You recognise the following traits of each character in the text:
        1- Name
        2- Age
        3- Gender
        4- Race
        5- Any other character
    You store these details of all the characters in the text."""
    system_message_prompt = utility_func.create_system_message_prompt(system_template)

    human_template = """Please extract all the traits (Name, age, race, gender etc) of all the characters in the following text:
    {chnk}
    Try to infer all these traits from the text. If some of the traits cannot be infer then please please write "not available".
    output should be in the following format:
    Lor (Age-not available, Gender-Female, Race-not available, Princess)
    John (Age-25 available, Gender-male, Race- Asian)"""
    
    human_message_prompt = utility_func.create_human_message_prompt(human_template)

    chat_prompt = utility_func.create_chat_prompt(system_message_prompt, human_message_prompt)

    chat_chain = LLMChain(llm=chat_model, prompt=chat_prompt)

    chapter_file = './Data/Sample_1.txt'  # Provide the path to the chapter file

    dialogues = utility_func.extract_dialogues_from_chapter(chapter_file, chat_chain)

    dialogue_collection_raw = utility_func.process_dialogues(dialogues)

    # print("Following are the characters in the text:\n", dialogue_collection_raw)

    output_raw_file = './output_sample/output_sample.txt'
   
    # utility_func.write_dialogues_to_file(dialogue_collection_raw, output_raw_file)
#%%
    unique_characters = utility_func.remove_repeating_characters(dialogue_collection_raw)
    
    unique_charac= utility_func.remove_enumerations_and_repeating_keys(unique_characters)
    
    utility_func.print_characters_with_traits(unique_charac)
    
    utility_func.write_to_file(output_raw_file, unique_charac)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    