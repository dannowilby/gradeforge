import sys
import os

import google

from .proto.student_details_pb2 import StudentDetails

def run(queue):
    """
    To wait on an async queue for incoming request data. When data is 
    recieved, this function will create the report card (send requests to the
    LLM), add it to the data base, and send a confirmation text that the 
    procedure has completed.
    """
    
    while msg := queue.get():
        if msg is None:
            sys.exit()
        
        details = StudentDetails()
        try:
            details.ParseFromString(msg)        
        except google.protobuf.message.DecodeError:
            continue

        # generate the report card
        generate_report_card(details)
        
        # store the report in the db

        # send a text message that jobs done


def generate_report_card(details):
    pass