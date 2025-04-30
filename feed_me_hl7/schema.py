from pydantic import BaseModel, Field


class HL7Message(BaseModel):
    """HL7 message model"""

    msh : dict = Field(description="MSH segment of the HL7 message")
    evn : dict = Field(description="EVN segment of the HL7 message")
    pid : dict = Field(description="PID segment of the HL7 message")
    pd1 : dict = Field(description="PD1 segment of the HL7 message")
    pv1 : dict = Field(description="PV1 segment of the HL7 message")
    pv2 : dict = Field(description="PV2 segment of the HL7 message")
    dg1 : dict = Field(description="DG1 segment of the HL7 message")
    in1 : dict = Field(description="IN1 segment of the HL7 message")
    
    