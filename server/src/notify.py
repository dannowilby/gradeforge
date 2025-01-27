import boto3

from .proto.student_details_pb2 import StudentDetails

class Notify:
    def __init__(self):
        self.client = boto3.client('sns')
        

    def send_message(self, details):
        self.client.publish(
            TopicArn="gradeforge-updates",
            Message=f"The report card for {details.student_name} has been finished.",
            Subject=f"GradeForge: Report card completed."
        )