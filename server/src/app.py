from flask import Flask, request, jsonify, send_file
from markupsafe import escape
import google

from .proto import student_details_pb2 as proto

# start another process p2 here to handle report card creation
app = Flask(__name__)

@app.get("/")
def index():
    return send_file("pages/index.html")

@app.get("/about")
def about():
    return send_file("pages/about.html")


@app.get("/view/<student_id>")
def view_reports(student_id=None):
    return f"<p>Not implemented yet: {escape(student_id)}.</p>"

@app.post("/generate")
def generate():
    """
    Endpoint to initiate the generation of a report card.

    curl -X POST --data-raw $'\n\x06103348\x12\nNAme, Test(\x04' http://localhost:5000/generate
    """
    
    student_details = proto.StudentDetails()

    try:
        data = request.get_data()
        student_details.ParseFromString(data)
    except google.protobuf.message.DecodeError:
        return "Error parsing student details.\n", 400

    print(student_details)

    # send report card data to p2


    return f"Creating report card for {student_details.student_name}! Please check back later for results.\n", 200
