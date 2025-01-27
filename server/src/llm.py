from abc import ABC, abstractmethod
from anthropic import Anthropic
from google.protobuf.json_format import MessageToJson

from .proto.student_details_pb2 import StudentDetails

class LLM(ABC):

    @abstractmethod
    def get_formatted_prompt(self, details: StudentDetails) -> str:
        return "Base implementation."

    @abstractmethod
    def generate_report(self, details: StudentDetails) -> str:
        return "Base implementation."


class Claude(LLM):
    def __init__(self):
        self.client = Anthropic()

    def get_formatted_prompt(self, details: StudentDetails) -> str:
        return (
            "Create a paragraph that is at most 500 characters long that will "
            "serve as a report card. The report needs to start by mentioning "
            "the student's first name and explaining how their progress has "
            "been, if there is no information directly relating to this, then "
            "you should default to explaining that the progress has been good. "
            "The next part should explain anything notable happening during "
            "their sessions, only putting emphasis on the good information. "
            "End the report by listing the concepts they are currently working "
            "on and tie in how many pages they average per session. Use the "
            "information from the object given below:\n"
            f"{MessageToJson(details)}"
        )

    def generate_report(self, details):
        return self.client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": self.get_formatted_prompt(details),
                }
            ],
            model="claude-3-5-sonnet-latest",
        ).content[0].text


class Ollama(LLM):
    def __init__(self):
        self.name = "ollama"

    def get_formatted_prompt(self, details: StudentDetails) -> str:
        return "Unimplemented"

    def generate_report(self, details):
        return "Unimplemented"