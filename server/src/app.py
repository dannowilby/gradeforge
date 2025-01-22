from flask import Flask, request, jsonify, send_file
from markupsafe import escape

from .proto import student_details_pb2 as StudentDetails

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
    """
    data = parse_request(request.json)
    
    if data is None:
        return "Error parsing request", 400

    # send report card data to p2

    print(data)

    return "Creating report card! Please check back later for results.", 200


# Could potentially replace this with protobuf, but may be overkill
class ReportRequest:
    def __init__(self, name):
        self.name = name

def parse_request(json: dict[str]) -> ReportRequest | None:
    try:
        name = json["title"]

        return ReportRequest(name)
    except Exception:
        return None
