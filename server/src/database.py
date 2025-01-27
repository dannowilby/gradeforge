import os
from datetime import datetime

import psycopg

class Database:
    def __init__(self):
        db_user = os.environ["PG_USER"]
        db_pass = os.environ["PG_PASS"]
        db_port = os.environ["PG_PORT"]
        db_name = os.environ["PG_DB"]
        self.connection = psycopg.connect(
            f"postgresql://{db_user}:{db_pass}@db:{db_port}/{db_name}"
        )

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS report_cards (
                student_id TEXT, 
                student_name TEXT, 
                report TEXT, 
                created_at TIMESTAMP
            )
            """)
        self.connection.commit()
        
    def __del__(self):
        self.connection.close()

    def store_report(self, details, report):
        self.connection.execute(
            """
            INSERT INTO report_cards 
                (student_id, student_name, report, created_at) 
            VALUES (%s, %s, %s, %s)
            """,
            (details.student_id, details.student_name, report, datetime.now())
        )
        self.connection.commit()

    def get_students(self):
        result = self.connection.execute(
            """
            SELECT distinct on (student_name) 
                student_id, student_name 
            FROM report_cards
            """
        ).fetchall()
        return result
        
    def get_reports_for_student(self, student_id):
        result = self.connection.execute(
            """
            SELECT 
                student_name, report, created_at 
            FROM report_cards 
            WHERE student_id = %s 
            ORDER BY created_at DESC
            """, 
            (student_id,)
        ).fetchall()

        return result