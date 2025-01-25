import os

from flask import Flask, request, jsonify, send_file
from markupsafe import escape
import google
from sqlalchemy import create_engine, text

from .database import Database
from .proto.student_details_pb2 import StudentDetails


def app(queue):
    """
    The frontend for the generation service. Creates a Flask app with endpoints
    for report card generation and viewing.

    Takes a multiprocessing queue that is shared with the generator process.
    """

    app = Flask(__name__)

    database = Database()

    # Register routes without decorator so that we can pass more context
    # Flask specifically has a context data structure for this purpose, but
    # this method for now. 
    app.get("/")(index)
    app.get("/about")(about)
    app.get("/view")(reports_overview_wrapper(database))
    app.get("/view/<student_id>")(view_report_wrapper(database))
    app.post("/generate")(lambda: generate(queue))

    return app


def index():
    return send_file("pages/index.html")

def about():
    return send_file("pages/about.html")

def reports_overview_wrapper(database):
    """
    Wraps the `reports_overview` function to allow passing a database engine.

    Endpoint to show all the unique students who have report cards generated 
    for them in the database.
    """
    def reports_overview():
        output = "<h2>Student Reports</h2>"
        students = database.get_students()
        for student in students:
            output += f"<p><a href='/view/{student.student_id}'>{student.student_name}</a></p>"
        return output, 200
    
    return reports_overview

def view_report_wrapper(database):
    """
    Wraps the `view_reports` function to allow passing a database engine.

    Endpoint to show the reports for a specific student. The target student is
    specified by using their student_id as a part of the slug.
    """
    
    def view_report(student_id=None):
        results = database.get_reports_for_student(student_id)
        
        if len(results) < 1:
            return "<p>No results.</p>", 200
        
        # manually building out the interface like this is not the greatest 
        # solution ever however it works, and is relatively easy to maintain
        output = f"<h2>{results[0].student_name}</h2><h3>{student_id}</h3>"
        for row in results:
            output += "<div style='margin: 1rem;border-top: solid;'>"
            output +=   f"<p>{row.created_at}</p>"
            output +=   f"<p style='margin-left: 2rem;'>{row.report}</p>"
            output += "</div>"
        return output, 200
    
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
    except google.protobuf.message.DecodeError:
        return "Error parsing student details.\n", 400
    
    # need to check if queue can accept, in its current state it will block 
    # until it can place the value
    queue.put(data)

    return f"Creating report card for {student_details.student_name}! Please check back later for results.\n", 200
