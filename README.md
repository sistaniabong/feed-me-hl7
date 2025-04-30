# Feed Me HL7

## Features

- Parses HL7 ADT messages into structured JSON using OpenAI LLM and map it to custom pydantic schema
- Parses HL7 ADT messages into structured JSON using [HL7Apy](https://crs4.github.io/hl7apy/)

## Installation

Install all dependencies for the project

`uv sync`

Update environment variables

`direnv allow`

refer to this [page](https://direnv.net/) to setup direnv if not already setup.

Parse HL7 ADT using HL7Apy

`uv run hl7apy_parser.py --message "<insert ADT message here>"`

Parse HL7 ADT using OpenAI LLM

`uv run main.py --message "<insert ADT message here>"`

## A few thoughts...

### 1. **HL7Apy**

#### Pros:
- **Standards-Based Parsing**: HL7Apy is specifically designed to handle HL7 messages and adheres strictly to the HL7 standard.
- **Lightweight**: It is a lightweight library with minimal dependencies, making it efficient for parsing HL7 messages.
- **Deterministic**: The parsing process is deterministic, so the output is predictable and consistent.

#### Cons:
- **Limited Flexibility**: HL7Apy is limited to the HL7 standard and cannot handle custom or non-standard variations of HL7 messages. This is particularly disadvantageous when receiving feeds from different HEI (Health Information Exchange) vendors (Bamboo vs PCC). In this case, HL7Apy cannot parse the example ADT feed from Bamboo.
- **Version Support**: Some HL7 versions or segments may not be supported, requiring manual intervention.
- **No Contextual Understanding**: It lacks the ability to infer or interpret ambiguous data beyond the HL7 specification
- **Inefficient Structure**: Key and value pair is redundant and inefficient. For example: 

        "date_time_of_message":{
            "time":"20240914203344"
        },
        "receiving_facility":{
            "namespace_id":"Waymark"
        }

        #it should just be

        "date_time_of_message":"20240914203344",
        "receiving_facility":"Waymark"

#### Use Case:
HL7Apy is ideal for scenarios where strict adherence to the HL7 standard is required, and the messages conform to supported versions and structures.

---

### 2. **OpenAI LLM**

#### Pros:
- **Flexibility**: The LLM can handle non-standard or custom HL7 messages, making it suitable for diverse use cases.
- **Contextual Understanding**: It can infer and interpret ambiguous or incomplete data, providing more meaningful outputs. This results in cleanly structured data without unnecessary nested dicts. For example: 

        "msh":{
            "fieldSeparator":"|",
            "encodingCharacters":"^~\\&",
            "sendingApplication":"Collective",
            "sendingFacility":"wa_se",
            "receivingApplication":"Waymark",
            "receivingFacility":"Waymark",
            "datetimeOfMessage":"20240914203344",
            "messageType":"ADT^A08",
            "messageControlId":"20240914203344",
            "processingId":"P",
            "versionId":"2.5"
        }

        vs hl7apy

        "msh":{
            "field_separator":{
                "st":"\\F\\"
            },
            "encoding_characters":{
                "st":"\\S\\\\R\\\\E\\\\T\\"
            },
            "sending_application":{
                "namespace_id":"Collective"
            },
            "sending_facility":{
                "namespace_id":"wa_se"
            },
            "receiving_application":{
                "namespace_id":"Waymark"
            },
            "receiving_facility":{
                "namespace_id":"Waymark"
            },
            "date_time_of_message":{
                "time":"20240914203344"
            },
            "message_type":{
                "message_code":"ADT",
                "trigger_event":"A08"
            },
            "message_control_id":{
                "st":"20240914203344"
            },
            "processing_id":{
                "processing_id":"P"
            },
            "version_id":{
                "version_id":"2.5"
            }
        }
- **Schema Mapping**: The LLM can map HL7 data to custom schemas, such as FHIR. See example [here](/results/llm_hl7_fhir.json).
- **Extensibility**: Easily adaptable to new requirements by modifying the prompt or schema.

#### Cons:
- **Resource Intensive**: Requires significant computational resources and may incur costs, especially when using large models.
- **Non-Deterministic**: The output may vary slightly depending on the model's interpretation of the input. This is particularly disadvantageous when it omits or misinterpret certain key fields such as visit_number.
- **Dependency on External Services**: Relies on external APIs (e.g., OpenAI), which may introduce latency or availability issues.

#### Use Case:
The LLM is ideal for scenarios where flexibility, contextual understanding, or mapping to custom schemas is required, especially when dealing with non-standard HL7 messages.

---

### OpenQ for OpenAI 🙊
OpenAI LLM seems to be doing a good job in interpreting HL7, but still a bit too wild... So what can we do to keep the result stable enough for production use?

- We could set the LLM temp to 0.0 to remove randomness and be less wild
- We could define a clear, unambiguous prompt, and use the same wording every time when it comes to instructions on edge cases etc
- We could enforce the output structure via Pydantic (so at least it would be flagged when it goes wild)


