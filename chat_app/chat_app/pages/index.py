"""The home page of the app."""

from chat_app import styles
from chat_app.templates import template

import reflex as rx
from reflex_chat import chat
#api
from datetime import date
import re
import json

today = date.today()

# dd/mm/YY
td = today.strftime("%d/%m/%Y")

"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""


def parse_string(string_to_parse):
    # Find the start and end index of the JSON part
    start_index = string_to_parse.find('{')
    end_index = string_to_parse.rfind('}') + 1

    # Extract the JSON part from the string
    json_string = string_to_parse[start_index:end_index]

    # Remove leading and trailing whitespace and newlines
    json_string = json_string.strip()

    # Remove the initial 'json' label and surrounding newlines
    json_string = json_string.replace('```json', '').replace('```', '').strip()

    # Split the string by commas to get key-value pairs
    pairs = json_string.split(',')

    # Initialize an empty dictionary to store key-value pairs
    parsed_dict = {}

    # Iterate over key-value pairs and split them by colons to extract keys and values
    for pair in pairs:
        key, value = pair.split(':')
        # Remove surrounding whitespace and quotes from the key and value
        key = key.strip().strip('"')
        value = value.strip().strip('"')
        # Add the key-value pair to the dictionary
        parsed_dict[key] = value
    return parsed_dict


import google.generativeai as genai

genai.configure(api_key="AIzaSyD4niUQYhpIMQPf7L56CNCQ_v8RvG2-hLo")

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 100,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]
#     try:
#         system_instruction1 = "Given the current task: {}. As a personal assistant, your task is to inquire about the progress on the current tasks and to gather information about any new tasks along with their deadlines. It's important to approach this with empathy and encouragement, especially if the user seems tired.".format(str(h2))
#     except:
system_instruction1 = "As a personal assistant, your task is to inquire about the progress on the current tasks and to gather information about any new tasks along with their deadlines. It's important to approach this with empathy and encouragement, especially if the user seems tired."
system_instruction2 = "Given that today is {}. Extract the due date of every task mentioned, and output in the json format.".format(
    td)

model1 = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                               generation_config=generation_config,
                               system_instruction=system_instruction1,
                               safety_settings=safety_settings)

model2 = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                               generation_config=generation_config,
                               system_instruction=system_instruction2,
                               safety_settings=safety_settings)

convo1 = model1.start_chat(history=[])
convo2 = model2.start_chat(history=[])


def gemini(input_text):
    # conversation
    response1 = convo1.send_message(input_text)
    print(response1.text)

    response2 = model2.generate_content(input_text)
    #     progress.update(parse_string(response2.text))

    #     return progress
    print(response2.text)
    return response1.text


# print(convo.last.text)


async def process(chat):
    messages = chat.get_messages()
    last_message = messages[-2]
    response = gemini(last_message["content"])
    chat.append_to_response(response)
    yield


#return process

# @rx.page(route="/", title="Home Page")
@template(route="/", title="Chat")
def index() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    # """
    # with open("README.md", encoding="utf-8") as readme:
    #     content = readme.read()
    # return rx.markdown(content, component_map=styles.markdown_style)
    return rx.container(
        rx.box(
            chat(process=process),
            height="100vh",
        ),
        size="4"
    )