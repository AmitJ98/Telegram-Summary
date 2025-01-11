import json
import re
import cohere
import dotenv
import os

dotenv.load_dotenv()

INVISIBLE_CHARS_PATTERN_RE = r'[\u200b-\u200d\n\r\t]'
SUMMARY_LENGTH = 0.13 # should be 10 - 25% of the original text

COHERE_API_KEY = os.getenv('COHERE_API_KEY')
cohere_client = cohere.Client(COHERE_API_KEY)


def generate_prompt_for_llm(processed_text:str, text_length:int):
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


def pre_proccess_test(unread_messages):
    ans = []
    messages_length = 0
    for m in unread_messages:
        curr_date = m['timestamp']
        curr_text = []
        if m['content']:
            curr_text.append(re.sub(INVISIBLE_CHARS_PATTERN_RE, '', m['content']))
            messages_length+=len(m['content'].split())
        if m['media_type'] == True:
            curr_text.append(re.sub(INVISIBLE_CHARS_PATTERN_RE, '', m['media_caption'])) 
            messages_length+=len(m['media_caption'].split())

        # ans.append(curr_date + ": " + "".join(curr_text) + '\n')
        ans.append('<START> '+ curr_date + ': ' + "".join(curr_text) + ' <END>\n')

    return ans, messages_length
   

def generate_summary(prompt:str, text_length:int):

    try:
        response = cohere_client.generate(
            model="command-r-plus", 
            prompt=prompt, 
            max_tokens=1200, 
            temperature=0.7 
        )
        summary = response.generations[0].text
        return summary
    except Exception as e:
        print(f"Error during summarization: {e}")
        return None



unread_messages = []
# Load unread messages from the JSON file
with open('unread_messages.json', 'r', encoding='utf-8') as f:
    unread_messages = json.load(f)

unread_messages = unread_messages[::-1]
text,l =  pre_proccess_test(unread_messages)
prompt_for_llm = generate_prompt_for_llm(text,l)

s = generate_summary(prompt_for_llm,l)
if s:
    print(s)
else:
    print("Error during summarization")






 #     unread_messages_test.append({
            #         'message_id': message.id,
            #         'content': content,  # Text content 
            #         'timestamp': message.date.isoformat(),  # Storing timestamp in ISO format
            #         'sender_id': sender_id,
            #         'sender_username': sender_username,
            #         'media_type': media,  # 'True', 'False'
            #         'media_caption': media_caption,  # The caption if media 
            #     })