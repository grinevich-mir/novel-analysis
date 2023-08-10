#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import utilities
from langchain import LLMChain


if __name__ == "__main__":
    
    api_key = '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'

    chat_model = utilities.initialize_chat_model(api_key)

    system_template = """"You are an expert novel reader. 
    You can recognize various background environment sounds in the text such as:
    footsteps, something dropping on the floor, gunfire, rain, crowd, car passing by, wind, forest, etc."""
    system_message_prompt = utilities.create_system_message_prompt(system_template)

    human_template = """Please extract lines from the text which contain background sounds along with the name of the sound effect itself.
    Following is the text in context:\n
    {chnk}
    \n After extracting sound please add 10 to 15 more associated sounds that could be present in the environment at the same time.
    For example in case of rain sounds, the other 10 sounds present at the same time are:
    Pitter-Patter of Rain, Distant Thunder, Leaves Rustling, River Flow, Birdsong, Forest Ambiance, Water Dripping,
    Insects Buzzing, Wind Through Grass, Echoing Caves etc
    \n Please reply in a consistent format (text containing the sound effects followed by the sound and then associated 10-15 sounds).
    output format: 
        1- Text: Idling engine, Sound: Car running sound, Associated sounds: Horn honking, tires screeching, cars passing by, engine revving, car stereo playing, traffic noise, engine running sound, car engine accelerating, car engine decelerating.
        2- Text: Radio playing golden oldies from the 60's, Sound: Music playing, Associated sounds: Guitar solo, drum beats, bassline, piano chords, saxophone melody, vocal harmonies, crowd cheering, tambourine shaking, trumpet solo, keyboard riff.
    \n Please do not extract the sounds like the following rom the text:
    speech, question, assurance, thinking, explaining and conversations sounds."""
    human_message_prompt = utilities.create_human_message_prompt(human_template)

    chat_prompt = utilities.create_chat_prompt(system_message_prompt, human_message_prompt)

    chat_chain = LLMChain(llm=chat_model, prompt=chat_prompt)

    chapter_file = './Data/chapter_1.txt'  # Provide the path to the chapter file

    dialogues = utilities.extract_dialogues_from_chapter(chapter_file, chat_chain)

    dialogue_collection_raw = utilities.process_dialogues(dialogues)

    print("Following are the environment sounds and sources of those sounds:\n", dialogue_collection_raw)

    output_raw_file = './output/output.txt'
   
    utilities.write_dialogues_to_file(dialogue_collection_raw, output_raw_file)