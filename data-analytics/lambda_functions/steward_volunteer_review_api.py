import json
import logging
import os
import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_db_connection():
    try:
        return psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            port=os.environ.get("DB_PORT"),
            cursor_factory=RealDictCursor
        )
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        page = body.get("page", 1)
        page_size = body.get("page_size", 5)

        conn = get_db_connection()
        cursor = conn.cursor()

        offset = (page - 1) * page_size

        # Using placeholder status because DB is not available
        review_status = 'pending_review'

        count_query = """
            SELECT COUNT(*) AS total
            FROM volunteer_applications
            WHERE application_status = %s;
        """

        cursor.execute(count_query, (review_status,))
        total_records = cursor.fetchone()['total']
        total_pages = (total_records + page_size - 1) // page_size

        query = """
            SELECT 
                u.user_id,
                va.updated_time,
                'Review' AS volunteer_review
            FROM volunteer_applications va
            JOIN users u ON u.user_id = va.user_id
            WHERE va.application_status = %s
            ORDER BY va.updated_time DESC
            LIMIT %s OFFSET %s;
        """

        cursor.execute(query, (review_status, page_size, offset))
        rows = cursor.fetchall()

        conn.close()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "data": rows,
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_records": total_records,
                    "total_pages": total_pages
                }
            })
        }

    except Exception as e:
        logger.error(f"Lambda error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal server error"
            })
        }
