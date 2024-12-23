import json
from summarizer import summarize_group
import json
import re

INVISIBLE_CHARS_PATTERN_RE = r'[\u200b-\u200d\n\r\t]'


def pre_proccess_test(unread_messages):
    unread_messages = unread_messages[:10]
    ans = []
    for m in unread_messages:
        curr_date = m['timestamp']
        curr_text = []
        if m['content']:
            curr_text.append(re.sub(INVISIBLE_CHARS_PATTERN_RE, '', m['content']))
        if m['media_type'] == True:
            curr_text.append(re.sub(INVISIBLE_CHARS_PATTERN_RE, '', m['media_caption'])) 
        ans.append(curr_date + ": " + "".join(curr_text) + '\n')

    



unread_messages = []
# Load unread messages from the JSON file
with open('unread_messages.json', 'r', encoding='utf-8') as f:
    unread_messages = json.load(f)

unread_messages = unread_messages[::-1]
pre_proccess_test(unread_messages)



 #     unread_messages_test.append({
            #         'message_id': message.id,
            #         'content': content,  # Text content 
            #         'timestamp': message.date.isoformat(),  # Storing timestamp in ISO format
            #         'sender_id': sender_id,
            #         'sender_username': sender_username,
            #         'media_type': media,  # 'True', 'False'
            #         'media_caption': media_caption,  # The caption if media 
            #     })