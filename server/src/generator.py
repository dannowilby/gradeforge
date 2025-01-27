import sys
import os

from google.protobuf.message import DecodeError
from google.protobuf.json_format import MessageToJson


from .text_gen import Claude, Ollama
from .database import Database
from .notify import Notify
from .proto.student_details_pb2 import StudentDetails

def run(queue):
    """
    To wait on an async queue for incoming request data. When data is 
    recieved, this function will create the report card (send requests to the
    LLM), add it to the database, and send a confirmation text that the 
    procedure has completed.
    """

    text_gen = None
    match os.environ["MODEL"]:
        case "claude":
            text_gen = Claude()
        case "ollama":
            text_gen = Ollama()

    # now that we are on a separate process, create its own db connection
    database = Database()

    notify_enabled = "NOTIFICATIONS_ENABLED" in os.environ
    notifier = notify_enabled and Notify()

    while msg := queue.get():
        if msg is None:
            sys.exit()
        
        details = StudentDetails()
        try:
            details.ParseFromString(msg)        
        except DecodeError:
            continue

        # generate the report card
        report = text_gen.generate_report(details)
        
        # store the report in the db
        database.store_report(details, report)

        # send a text message that jobs done
        if notify_enabled:
            notifier.send_message(details)
