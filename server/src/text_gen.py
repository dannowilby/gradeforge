from abc import ABC, abstractmethod
import os

from anthropic import Anthropic
from google.protobuf.json_format import MessageToJson
import requests

from .proto.student_details_pb2 import StudentDetails

class TextGen(ABC):

    @abstractmethod
    def get_formatted_prompt(self, details: StudentDetails) -> str:
        return "Base implementation."

    @abstractmethod
    def generate_report(self, details: StudentDetails) -> str:
        return "Base implementation."


class Claude(TextGen):
    def __init__(self):
        self.name = "claude"
        self.client = Anthropic()

    def get_formatted_prompt(self, details: StudentDetails) -> str:
        return (
            "Create a paragraph that is around 500 characters long that will "
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


class Ollama(TextGen):
    def __init__(self):
        self.name = "ollama"
        self.port = os.environ["OLLAMA_PORT"]

    def get_formatted_prompt(self, details: StudentDetails) -> str:
        return (
            "You are the adminitstrator of a small tutoring service writing "
            "report cards about students to their parents."
            "Create a paragraph that is around 500 characters long that will "
            "serve as a report card. The report needs to start by mentioning "
            "the student's first name and explaining how their progress has "
            "been, if there is no information directly relating to this, then "
            "you should default to explaining that the progress has been good. "
            "The next part should explain anything notable happening during "
            "their sessions, only putting emphasis on the good information. "
            "End the report by listing the concepts they are currently working "
            "on and tie in how many pages they average per session. Below is an "
            "example of the output you should aim to create: "
            "First has shown good progress in their math work. They "
            "demonstrated particularly strong improvement with multi-digit "
            "subtraction, mastering the concept by the end of their session. "
            "Currently, they are working on geometric shapes, number patterns, "
            "and reasoning by grouping. First typically completes 3-4 pages per "
            "session."
            "Use the information from the object given below:\n"
            f"{MessageToJson(details)}"
            "Make sure to only provide the report in your response."
        )

    def generate_report(self, details):

        resp = requests.post(
            f"http://ollama:{self.port}/api/generate", 
            json={ 
                "model": "llama3.2", 
                "prompt": self.get_formatted_prompt(details), 
                "stream": False 
            }, 
            timeout=(10, 300)
        )
        
        return resp.json()['response']
    
