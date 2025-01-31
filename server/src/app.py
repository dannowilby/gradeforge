import os

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from markupsafe import escape
from google.protobuf.message import DecodeError

from .database import Database
from .proto.student_details_pb2 import StudentDetails


def app(queue):
    """
    The frontend for the generation service. Creates a Flask app with endpoints
    for report card generation and viewing.

    Takes a multiprocessing queue that is shared with the generator process.
    """

    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    database = Database()

    # Register routes without decorator so that we can pass more context
    # Flask specifically has a context data structure for this purpose, but
    # this method for now.
    app.get("/view")(reports_overview_wrapper(database))
    app.get("/view/<student_id>")(view_report_wrapper(database))
    app.post("/generate")(lambda: generate(queue))

    return app

def reports_overview_wrapper(database):
    """
    Wraps the `reports_overview` function to allow passing a database engine.

    Endpoint to show all the unique students who have report cards generated 
    for them in the database.
    """
    def reports_overview():
        students = database.get_students()
        return jsonify(students)
    
    return reports_overview

def view_report_wrapper(database):
    """
    Wraps the `view_reports` function to allow passing a database engine.

    Endpoint to show the reports for a specific student. The target student is
    specified by using their student_id as a part of the slug.
    """
    
    def view_report(student_id=None):
        results = database.get_reports_for_student(student_id)
        return jsonify(results)
    
    return view_report

def generate(queue):
    """
    Endpoint to initiate the generation of a report card. It adds the incoming
    serialized student's details to the background process's queue, where it
    will be processed.
    """
    
    student_details = StudentDetails()

    try:
        data = request.get_data()
        student_details.ParseFromString(data)
    except DecodeError:
        return "Error parsing student details.\n", 400
    
    # If the queue is full, don't accept it and tell the extension instead
    try:
        queue.put(data, False)
    except queue.Full:
        return f"Queue is full, try again later", 200


    return f"Creating report card for {student_details.student_name}! Please check back later for results.\n", 200
