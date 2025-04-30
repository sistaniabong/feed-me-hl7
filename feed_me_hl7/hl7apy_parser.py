from typing import Dict, Any
import click
from hl7apy.core import SubComponent
from hl7apy.parser import parse_message

def hl7_join_message(raw_message):
    """A method that join the HL7 lines with \r separator
    :param data: hl7 data coming from post request body
    """
    data = raw_message.replace("\n", "\r")
    return data

def hl7_to_json(message, desc=True) -> Dict[str, Any] | str:
    """A method that convert hl7 message to json
    This is done recursively by calling itself with any child elements
    return json of the hl7 message"""
    if message.children and not isinstance(message.children[0], SubComponent):
        hl7_json = {}
        for segment in message.children:
            name = str(segment.name).lower()
            if desc:
                name = str(segment.long_name).lower() if segment.long_name else name
            json_obj = hl7_to_json(segment, desc=desc)
            if name in hl7_json:
                if not isinstance(hl7_json[name], list):
                    hl7_json[name] = [hl7_json[name]]
                hl7_json[name].append(json_obj)
            else:
                hl7_json[name] = json_obj
        return hl7_json
    else:
        return message.to_er7()

@click.command()
@click.option(
    "--message", required=True
)
def hl7_message_to_json(message: str) -> dict:
    hl7_raw_message = hl7_join_message(message)
    hl7_message = parse_message(hl7_raw_message)
    if hl7_message:
        # convert hl7 message to json
        hl7_json = hl7_to_json(message=hl7_message, desc=True)
        print(hl7_json)
        return hl7_json
    
if __name__ == "__main__":
    hl7_message_to_json()

