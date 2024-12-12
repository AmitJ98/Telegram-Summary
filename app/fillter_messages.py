def pre_proccess(unread_messages):
    unread_messages = unread_messages[::-1]
    for message in unread_messages:
        print(f"Message ID: {message.id}, Content: {message.text}")