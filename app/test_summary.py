import json
from summarizer import summarize_group
import json

def pre_proccess_test(unread_messages):
    pass



unread_messages = []
# Load unread messages from the JSON file
with open('unread_messages.json', 'r', encoding='utf-8') as f:
    unread_messages = json.load(f)

unread_messages [::-1]
summarize_group(unread_messages,"Test Group")




 #     unread_messages_test.append({
            #         'message_id': message.id,
            #         'content': content,  # Text content 
            #         'timestamp': message.date.isoformat(),  # Storing timestamp in ISO format
            #         'sender_id': sender_id,
            #         'sender_username': sender_username,
            #         'media_type': media,  # 'True', 'False'
            #         'media_caption': media_caption,  # The caption if media 
            #     })