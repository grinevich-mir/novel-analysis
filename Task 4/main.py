#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import utilities
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


if __name__ == "__main__":
    
    api_key = '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'

    chat_model = utilities.initialize_chat_model(api_key)

    system_template = """"You are an expert novel reader.You can recognize various environment sounds in the text such as like rain, crowd, car passing by, wind, forest, etc."""
    system_message_prompt = utilities.create_system_message_prompt(system_template)

    human_template = "Please extract lines from the following text which contain environment sounds along with the name of the sound effect itself: \n {chnk} \n Please reply in a consistent format (text containing the sound effects followed by the name of the environment sound in brackets)."
    human_message_prompt = utilities.create_human_message_prompt(human_template)

    chat_prompt = utilities.create_chat_prompt(system_message_prompt, human_message_prompt)

    chat_chain = LLMChain(llm=chat_model, prompt=chat_prompt)

    chapter_file = './Data/chapter_1.txt'  # Provide the path to the chapter file

    dialogues = utilities.extract_dialogues_from_chapter(chapter_file, chat_chain)

    dialogue_collection_raw = utilities.process_dialogues(dialogues)

    print("Following are the environment sounds and sources of those sounds:\n", dialogue_collection_raw)

    output_raw_file = './output/output.txt'
   
    utilities.write_dialogues_to_file(dialogue_collection_raw, output_raw_file)