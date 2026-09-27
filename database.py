import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "resume_analyzer")
        )
    except mysql.connector.Error as error:
        print("Database connection error:", error)
        return None

def save_application(candidate_name, company_name, job_title, match_score,
                     matching_skills, missing_skills, keywords, suggestions):
    connection = get_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO applications
            (candidate_name, company_name, job_title, match_score)
            VALUES (%s, %s, %s, %s)
            """,
            (candidate_name, company_name, job_title, match_score)
        )

        application_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO analysis_results
            (application_id, matching_skills, missing_skills, keywords, suggestions)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                application_id,
                ", ".join(map(str, matching_skills)),
                ", ".join(map(str, missing_skills)),
                ", ".join(map(str, keywords)),
                "\n".join(map(str, suggestions))
            )
        )

        connection.commit()
        return True

    except mysql.connector.Error as error:
        print("Database error:", error)
        connection.rollback()
        return False

    finally:
        cursor.close()
        connection.close()

def get_applications():
    connection = get_connection()
    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT id, candidate_name, company_name, job_title,
                   match_score, created_at
            FROM applications
            ORDER BY created_at DESC
            """
        )
        return cursor.fetchall()
    except mysql.connector.Error as error:
        print("Database error:", error)
        return []
    finally:
        cursor.close()
        connection.close()
