import os

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
        self.engine = create_engine(f"postgresql+psycopg://{db_user}:{db_pass}@db:{db_port}/{db_name}")

        with self.engine.connect() as conn:
            conn.execute(text("CREATE TABLE IF NOT EXISTS report_cards (student_id TEXT, student_name TEXT, report TEXT)"))
            conn.commit()
        
    def store_report(self, details, report):
        with self.engine.connect() as conn:
            conn.execute(
                text("INSERT INTO report_cards (student_id, student_name, report) VALUES (:si, :sn, :r)"),
                [{ 'si': details.student_id, 'sn': details.student_name, 'r': report }]
            )
            conn.commit()

    def get_students(self):
        with self.engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM report_cards")
            )
            output = []
            for row in result:
                output.append((row.student_name, row.student_id))

            return output