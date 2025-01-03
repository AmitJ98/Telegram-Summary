import re
import openai
import os
from dotenv import load_dotenv

INVISIBLE_CHARS = r'[\u200b-\u200d\n\r\t]'
SUMMARY_LENGTH = 0.17 # should be 10 - 25% of the original text


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def pre_proccess_messages(unread_messages:list):
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


def generate_prompt_for_llm(processed_text:str, text_length:int):
    prompt = f"""I have a text that I would like you to summarize.

Input: 
Text: {processed_text}
Original Text Length: {text_length}

Output:
Summary: Summarize the provided text concisely and accurately. You may split the summary into sections as you see fit to improve readability.
The original text is separated by "<START>" and "<END>" to divide different messages. You are also provided with the date and time of the messages for additional context.
Summary Length: The length of the summary should be approximately 0.17 times the original text length.
Please ensure the summary maintains the core meaning and key information of the original text while adhering to the specified length constraint.
In addition, if part of the text refers to a video or image that is not included, please avoid mentioning it."""

    return prompt


#this function will get the pre procced text and will send the text to the openai api to get the summary
def summarize_messages(processed_text:str,text_length:int):
    prompt = generate_prompt_for_llm(processed_text,text_length)




def summarize_group(unread_messages:list):
    unread_messages = unread_messages[::-1]
    proccessed_text,text_length = pre_proccess_messages(unread_messages)
    summary = summarize_messages(proccessed_text,text_length)
    print("done")
    return summary
        