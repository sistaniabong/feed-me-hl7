import re
from typing import List

import json
import pika
import click
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from settings import Settings
from schema import HL7Message

# from settings import RabbitMqConsumerSettings


def extract_json(message: AIMessage) -> List[dict]:
    """Extracts JSON content from a string where JSON is embedded between `\`\`\`json and `\`\`\` tags.

    Parameters:
        text (str): The text containing the JSON content.

    Returns:
        list: A list of extracted JSON strings.
    """
    text = message.content
    # Define the regular expression pattern to match JSON blocks
    pattern = r"\`\`\`json(.*?)\`\`\`"

    # Find all non-overlapping matches of the pattern in the string
    matches = re.findall(pattern, text, re.DOTALL)

    # Return the list of matched JSON strings, stripping any leading or trailing whitespace
    try:
        return [json.loads(match.strip()) for match in matches]
    except Exception:
        raise ValueError(f"Failed to parse: {message}")


@click.command()
@click.option(
    "--message", required=True
)
def main(message:str) -> None:
    """ 
    Does magic to HL7 ADT
    """
    settings = Settings()
    model = init_chat_model("gpt-4o-mini", model_provider="openai")

    # messages = [
    #     SystemMessage("Parse this HL7 ADT message into structured JSON preserving field meanings. And use the schema {schema} to validate the JSON."),
    #     HumanMessage(message),
    # ]

    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Parse this HL7 ADT message into structured JSON preserving field meanings following HL7 FHIR schema."
            "- Split subcomponents (separated by ^) into nested array."
            "- Do not omit any fields."
            "- Preserve all data, even empty fields."
            "- Identify datetime fields and convert them to ISO 8601 format."
            "matches the given schema: \`\`\`json\n{schema}\n\`\`\`. "
            ),
        ("human", "{message}"),
    ]
    ).partial(schema=HL7Message.model_json_schema())

    chain = prompt | model | extract_json
    response = chain.invoke({"message": message})


    
    print("Response:")
    print(response)
    # print(response.content)


if __name__ == "__main__":
    main()
