import sys
import os

from google.protobuf.message import DecodeError

from .llm import Claude, Ollama
from .database import Database
from .proto.student_details_pb2 import StudentDetails

def run(queue):
    """
    To wait on an async queue for incoming request data. When data is 
    recieved, this function will create the report card (send requests to the
    LLM), add it to the database, and send a confirmation text that the 
    procedure has completed.
    """

    gen_service = {
        'claude': Claude(),
        'ollama': Ollama()
    }[os.environ["MODEL"]] # Do better

    # now that we are on a separate process, create its own db connection
    database = Database()


    while msg := queue.get():
        if msg is None:
            sys.exit()
        
        details = StudentDetails()
        try:
            details.ParseFromString(msg)        
        except DecodeError:
            continue

        # generate the report card
        report = gen_service.generate_report(details)
        
        # store the report in the db
        database.store_report(details, report)

        # send a text message that jobs done


def generate_report_card(details):
    pass