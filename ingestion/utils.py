import json
from datetime import datetime
from os import getenv

DEBUG = True

def format_message_obj(from_id:str, timestamp:str, text_value:str) -> dict:
    """creates a dict from message parameters

    Args:
        from_id (str): user id
        timestamp (str): unix timestamp
        text_value (str): message content

    Returns:
        dict: dict containing parameters
    """
    try:
        dt = datetime.fromtimestamp(float(timestamp))
        return {
            "user": from_id,
            "time": dt.strftime("%d-%m-%Y, %H:%M"),
            "message": text_value
        }
    except Exception as e:
        print("error formatting message_obj")
        if DEBUG:
            print(e)
        exit(1)

def extract_all_messages(filepath:str) -> list:
    """main component for ingesting chat log exports

    Args:
        filepath (str): path of file

    Returns:
        list: list of message objects
    """
    extracted_texts = []
    with open(filepath, "r") as file:

        jsonfile = json.load(file)
        messages = (jsonfile.get("messages", None))

        for msg in messages:
            # check if it is of type message
            if msg.get("type", None) != "message":
                continue
            text_value = msg.get("text", None)
            # check if text_value is null
            # if it is then put empty string
            if text_value == None:
                text_value = ""
            timestamp = msg.get("date_unixtime", None)
            # from_id = msg.get("from_id", None)
            username = msg.get("from", None)
            # check if `from` field is not null - this can be the case when user has deleted their account
            # if it is then use default username
            if username == None:
                username = getenv("DEFAULT_USERNAME")
                message_obj = format_message_obj(username, timestamp, text_value)
            else:
                message_obj = format_message_obj(username, timestamp, text_value)
            extracted_texts.append(message_obj)

    return extracted_texts

def format_output(filepath:str) -> str:
    """returns a formatted string of all messages in the file
    Args:
        filepath (str): path of the file to be formatted

    Returns:
        str: formatted string
    """
    ret = ""
    all_msg = extract_all_messages(filepath)
    for i in range(len(all_msg)):
        ret += f"{all_msg[i].get('user')} at {all_msg[i].get('time')}: {all_msg[i].get('message')}\n"
    return ret
