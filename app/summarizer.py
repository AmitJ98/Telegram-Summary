def pre_proccess(unread_messages):
    unread_messages = unread_messages[::-1]
    for message in unread_messages:
        print(f"Message ID: {message.id}, Content: {message.text}")






def summarize_group(unread_messages:list ,group_name:str):
    unread_messages = unread_messages[::-1]
    print(f"Begin Summary for {group_name} ---->")
    print(f"The unread messeges are from {unread_messages[0].date}")