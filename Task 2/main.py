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

    system_template = """"You are an expert novel reader. 
    You store details of all the characters in the novel."""
    system_message_prompt = utility_func.create_system_message_prompt(system_template)

    human_template = """Please list the characters from the text.
    Following is the text in context:\n
    {chnk}
    \n Please reply in a consistent format (List of characters).
    \n If some detail is missing in the text then please write "not provided"."""
    human_message_prompt = utility_func.create_human_message_prompt(human_template)

    chat_prompt = utility_func.create_chat_prompt(system_message_prompt, human_message_prompt)

    chat_chain = LLMChain(llm=chat_model, prompt=chat_prompt)

    chapter_file = './Data/Sample_1.txt'  # Provide the path to the chapter file

    dialogues = utility_func.extract_dialogues_from_chapter(chapter_file, chat_chain)

    dialogue_collection_raw = utility_func.process_dialogues(dialogues)

    print("Following are the characters in the text:\n", dialogue_collection_raw)

    output_raw_file = './output_sample/output_sample.txt'
   
    utility_func.write_dialogues_to_file(dialogue_collection_raw, output_raw_file)