import gradio as gr
import os
import time
from numpy import random

custom_css = """
<style>
  .fixed-size-box {
    color: #00ff00 !important;
    width: 100%;
    height: 600px;
    overflow: auto;
    padding: 10px;
  }
</style>
"""

import base64

def image_to_data_uri(filepath):
    with open(filepath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:image/png;base64,{encoded_string}"

image_data_uri = image_to_data_uri("assets/repo_logo_dark.png")

image = f"""
<img src="{image_data_uri}" alt="Your Image Alt Text" width="400"/>
Initializing BO, the smart way.
"""

from rambo.tools import BOInitializer
from rambo.utils import init_dspy
from dotenv import load_dotenv
import json

load_dotenv()

n=6
init_dspy(retrieval_type="embedding")  # TODO change this to embedding!
bo = BOInitializer(n)

state = gr.State()

def llm_answer(query: str):
    ctxt = bo.get_context(query)
    state.items = ctxt

    answer = bo(query=query)
    formatted = "Based on the reactions retrieved from the database, here are some conditions you can try first:\n"
    for c in answer.conditions[:1]:
        formatted += json.dumps(c.model_dump(), indent=4) + "\n"
    return formatted

def update_text(button_id):

    text = """{}"""

    for i in range(5):
        if button_id == f"Doc {i}":
            return text.format(state.items.passages[i])
    else:
        return "Click a button..."

import re

import requests
def cdk(smiles):
    """
    Get a depiction of some smiles.
    """
    
    url = "http://liacpc11.epfl.ch:8081/depict/wob/svg"
    headers = {'Content-Type': 'application/json'}
    response = requests.get(
        url,
        headers=headers,
        params={
            "smi": smiles,
            "zoom": 1,
            "w": 150,
            "h": 50,
            "abbr": "off",
        }
    )

    return response.text

def update_image(button_id):

    text = """{}"""

    for i in range(n):

        ret = state.items.passages[i]
        smiles = re.findall(r'( .*>>.*? )', ret)[0].split(' ')[-2]
        if button_id == f"Doc {i}":
            return text.format(cdk(smiles))
    else:
        return "Click a button..."

buttons = []

with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue=gr.themes.colors.green,
        secondary_hue=gr.themes.colors.green
    ),css=custom_css
) as demo:

    with gr.Row():
        gr.Markdown(image)

    with gr.Row():
        with gr.Column():
            chatbot = gr.Chatbot()
            msg = gr.Textbox()
            clear = gr.ClearButton([msg, chatbot])

            def respond(message, chat_history):
                bot_message = llm_answer(message)
                chat_history.append((message, bot_message))
                time.sleep(2)
                return "", chat_history

            msg.submit(respond, [msg, chatbot], [msg, chatbot])

        with gr.Column():
            with gr.Row():
                for i in range(n):
                    buttons.append(gr.Button(f'Doc {i}'))

            with gr.Column():
                retrieve_textbox = gr.Textbox()
                retrieve_image = gr.HTML()

    for i in range(n):
        buttons[i].click(fn=update_text, inputs=[buttons[i]], outputs=retrieve_textbox)
        buttons[i].click(fn=update_image, inputs=[buttons[i]], outputs=retrieve_image)


    # with gr.Row():
    #     gr.Markdown("## Built with [Langchain](https://python.langchain.com/en/latest/modules/llms/getting_started.html) 🦜️🔗️ at [LIAC, EPFL](https://schwallergroup.github.io/).")

demo.queue()
if __name__ == "__main__":
    demo.launch(
        server_name='0.0.0.0',
        server_port=8090
    )

	