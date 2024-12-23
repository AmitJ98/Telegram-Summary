import re
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")



def pre_proccess_messages(unread_messages):
    proccessed_messages = []




def summarize_messages(preprocessed_text):
    pass



def summarize_group(unread_messages:list ,group_name:str):
    unread_messages = unread_messages[::-1]
    for message in unread_messages:
        if message.text:
            print(f"Message ID: {message.id}, Content: {message.text}")
        elif message.caption:
            print(f"Message ID: {message.id}, Content: {message.caption}")

        