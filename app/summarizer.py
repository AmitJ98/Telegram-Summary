import re
import openai
import os
from dotenv import load_dotenv

INVISIBLE_CHARS = r'[\u200b-\u200d\n\r\t]'
SUMMARY_LENGTH = 0.17 # should be 10 - 25% of the original text


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def pre_proccess_messages(unread_messages):
    proccessed_text = []
    text_length = 0
    for message in unread_messages:
        curr_date = ""
        curr_text = []
        if message.text:
            curr_text.append(re.sub(INVISIBLE_CHARS, '', message.text))
            text_length += len(message.text.split())
        if message.caption:
            curr_text.append(re.sub(INVISIBLE_CHARS, '', message.caption))
            text_length += len(message.caption.split())
        
        proccessed_text.append('<START> '+ curr_date + ': ' + "".join(curr_date) + ' <END>\n')

    return proccessed_text,text_length


#this function will get the pre procced text and will send the text to the openai api to get the summary
def summarize_messages(preprocessed_text,text_length):
    pass



def summarize_group(unread_messages:list):
    unread_messages = unread_messages[::-1]
    proccessed_text,text_length = pre_proccess_messages(unread_messages)
    summary = summarize_messages(proccessed_text,text_length)
    return summary
        