import re
import cohere
import os
from dotenv import load_dotenv

INVISIBLE_CHARS = r'[\u200b-\u200d\n\r\t]'
SUMMARY_LENGTH = 0.17 # should be 10 - 25% of the original text


load_dotenv()

COHERE_API_KEY = os.getenv('COHERE_API_KEY')
cohere_client = cohere.Client(COHERE_API_KEY)


def pre_proccess_messages(unread_messages:list[str]) ->  tuple[str,int]:
    """Pre proccess the messages to remove invisible characters and get the length of the text
        return one text with all the messages and the length of the text"""

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
        
        proccessed_text.append('<START> '+ curr_date + ': ' + "".join(curr_text) + ' <END>\n')

    return proccessed_text,text_length


def generate_prompt_for_llm(processed_text:str, text_length:int) -> str:
    prompt = f"""Task:
Generate a concise and accurate summary of the provided text.
 The original text consists of messages separated by <START> and <END>, along with their respective date and time for context.


Input:
Text: {processed_text}
Original Text Length: {text_length}


Requirements:

1. Clarity and Accuracy: Maintain the core meaning and key information of the original messages.
2. Length Constraint: Ensure the summary length is approximately 13% of the original text length.
3. Readability: Structure the summary into sections if it improves clarity or flow.
4. Exclusions: Do not include references to videos or images that are not provided in the text.

Output:
[Your summary here]"""
    return prompt


def send_to_llm(prompt:str) -> str:
    """Send the prompt to the LLM model and return the summary"""

    try:
        response = cohere_client.generate(
            model="command-r-plus", 
            prompt=prompt, 
            max_tokens=1200, # TODO: Adjust max tokens based on the length of the original text
            temperature=0.7 
        )
        summary = response.generations[0].text
        return summary
    
    except Exception as e:
        print(f"[SUMMARY ERROR] during summarization: {e}")
        return None


def summarize_messages(group_name:str, processed_text:str, text_length:int):
    prompt = generate_prompt_for_llm(processed_text,text_length)
    summary = send_to_llm(prompt)
    if summary:
        return group_name + '\n' + summary
    else:  
        return None


def summarize_group(group_name:str, unread_messages:list) ->str:
    unread_messages = unread_messages[::-1]
    proccessed_text,text_length = pre_proccess_messages(unread_messages)
    summary = summarize_messages(group_name, proccessed_text,text_length)
    return summary
        