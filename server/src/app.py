from flask import Flask, request, jsonify, send_file
from markupsafe import escape

# start another process p2 here to handle report card creation
app = Flask(__name__)

@app.get("/")
def index():
    return send_file("index.html")

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
