import os
from datetime import datetime

from sqlalchemy import create_engine, text

# This is a dirty but cheap way to interface with our db. If the goal was to
# use all SQLAlchemy's features as an ORM, then we wouldn't do things this
# way, but as our schema is so simple, there's no real harm at the moment.
class Database:
    def __init__(self):
        db_user = os.environ["PG_USER"]
        db_pass = os.environ["PG_PASS"]
        db_port = os.environ["PG_PORT"]
        db_name = os.environ["PG_DB"]
        self.engine = create_engine(
            f"postgresql+psycopg://{db_user}:{db_pass}@db:{db_port}/{db_name}"
        )

        with self.engine.connect() as conn:
            conn.execute(text("DROP TABLE report_cards"))
            conn.execute(text("CREATE TABLE IF NOT EXISTS report_cards (student_id TEXT, student_name TEXT, report TEXT, created_at TIMESTAMP)"))
            conn.commit()
        
    def store_report(self, details, report):
        with self.engine.connect() as conn:
            conn.execute(
                text("INSERT INTO report_cards (student_id, student_name, report, created_at) VALUES (:si, :sn, :r, :d)"),
                [{ 'si': details.student_id, 'sn': details.student_name, 'r': report, 'd': datetime.now() }]
            )
            conn.commit()

    def get_students(self):
        with self.engine.connect() as conn:
            result = conn.execute(
                text("SELECT distinct on (student_name) student_name, student_id FROM report_cards")
            )
            return collect_results(result)
        
    def get_reports_for_student(self, student_id):
        with self.engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM report_cards WHERE student_id = :student_id ORDER BY created_at DESC"), [{ 'student_id': student_id }]
            )

            return collect_results(result)
        
def collect_results(results):
    output = []
    for row in results:
        output.append(row)
    return output