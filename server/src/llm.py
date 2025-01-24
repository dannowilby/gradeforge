from abc import ABC, abstractmethod
from anthropic import Anthropic

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
        return f"Not implemented"

    def generate_report(self, details):
        return "Not implemented"
    # self.client.messages.create(
    #         max_tokens=1024,
    #         messages=[
    #             {
    #                 "role": "user",
    #                 "content": self.get_formatted_prompt(details),
    #             }
    #         ],
    #         model="claude-3-5-sonnet-latest",
    #     )


class Ollama(LLM):
    def __init__(self):
        self.name = "ollama"

    def get_formatted_prompt(self, details: StudentDetails) -> str:
        return "Unimplemented"

    def generate_report(self, details):
        return "Unimplemented"