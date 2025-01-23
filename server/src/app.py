from flask import Flask, request, jsonify, send_file
from markupsafe import escape
import google

from .proto.student_details_pb2 import StudentDetails


def app(generator, queue):
    app = Flask(__name__)

    # register routes
    app.get("/")(index)
    app.get("/about")(about)
    app.get("/view/<student_id>")(view_reports)
    app.post("/generate")(lambda: generate(queue))
    
    # Daemon generator process debug endpoints
    # app.get("/process/poke_with_stick")(poke_with_stick(generator))
    # app.get("/process/i_cast_magic_missile")(magic_missile(queue))

    return app


def index():
    return send_file("pages/index.html")

def about():
    return send_file("pages/about.html")

def view_reports(student_id=None):
    return f"<p>Not implemented yet: {escape(student_id)}.</p>"

def generate(queue):
    """
    Endpoint to initiate the generation of a report card.

    curl -X POST --data-raw $'\n\x06103348\x12\nNAme, Test(\x04' http://localhost:5000/generate
    """
    
    student_details = StudentDetails()

    try:
        data = request.get_data()
        student_details.ParseFromString(data)
    except google.protobuf.message.DecodeError:
        return "Error parsing student details.\n", 400

    print(student_details)
    
    # need to check if queue can accept, in its current state it will block 
    # until it can place the value
    queue.put(data)

    return f"Creating report card for {student_details.student_name}! Please check back later for results.\n", 200


def poke_with_stick(generator):
    def c():
        return f"Did it move? {generator.is_alive()}", 200
    return c

def magic_missile(queue):
    def d():
        queue.put(None) # kill signal
        return "Job done milord", 200    
    return d
