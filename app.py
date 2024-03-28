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

def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)

def add_message(history, message):
    for x in message["files"]:
        history.append(((x,), None))
    if message["text"] is not None:
        history.append((message["text"], None))
    return history, gr.MultimodalTextbox(value=None, interactive=False)

def bot(history):
    response = "**That's cool!**"
    history[-1][1] = ""
    for character in response:
        history[-1][1] += character
        time.sleep(0.05)
        yield history

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

init_dspy(retrieval_type="test")  # TODO change this to embedding!
bo = BOInitializer(5)

state = gr.State()

def llm_answer(query: str):
    ctxt = bo.get_context(query)
    state.items = ctxt

    answer = bo(query=query)
    formatted = ""
    for c in answer.conditions:
        formatted += json.dumps(c.model_dump(), indent=4) + "\n"
    return formatted

def update_text(button_id):
    if button_id == "Doc 0":
        return state.items.passages[0]
    elif button_id == "Doc 1":
        return state.items.passages[1]
    elif button_id == "Doc 2":
        return state.items.passages[2]
    elif button_id == "Doc 3":
        return state.items.passages[3]
    elif button_id == "Doc 4":
        return state.items.passages[4]
    else:
        return "Click a button..."

buttons = []

with gr.Blocks(theme=gr.themes.Soft(primary_hue=gr.themes.colors.green,secondary_hue=gr.themes.colors.green),css=custom_css) as demo:

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
                for i in range(3):
                    buttons.append(gr.Button(f'Doc {i}'))

            with gr.Row():
                retrieve_textbox = gr.Textbox()

    for i in range(3):
        buttons[i].click(fn=update_text, inputs=[buttons[i]], outputs=retrieve_textbox)


    # with gr.Row():
    #     gr.Markdown("## Built with [Langchain](https://python.langchain.com/en/latest/modules/llms/getting_started.html) 🦜️🔗️ at [LIAC, EPFL](https://schwallergroup.github.io/).")

demo.queue()
if __name__ == "__main__":
    demo.launch(
        server_name='0.0.0.0',
        server_port=8090
    )

	