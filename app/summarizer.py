import re
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")



def pre_proccess_messages(unread_messages):
    pass


def summarize_text(preprocessed_text):
    pass



def summarize_group(unread_messages:list ,group_name:str):
    unread_messages = unread_messages[::-1]
    print(f"Begin Summary for {group_name} ---->")
    print(f"The oldest unread messeges is from {unread_messages[0].date}")

    for message in unread_messages:
        print(f"Message ID: {message.id}, Content: {message.text}")
        