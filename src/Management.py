import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Blueprint, request, jsonify, session
import psycopg2
from config.db_config import get_db_connection

Management_blueprint = Blueprint('Management', __name__)

@Management_blueprint.route('/assign', methods=['POST'])
def assign():
    if 'user_id' not in session or session['role'] not in ['Admin', 'Teacher']:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    user_id = data.get("user_id")
    event_id = data.get("event_id")
    responsibility = data.get("responsibility")

    if not all([user_id, event_id, responsibility]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()


        # Check for event conflicts
        cursor.execute("""
                WITH new_event AS (
                SELECT event_date, start_time, end_time 
                FROM events 
                WHERE event_id = %s
            )
            SELECT e.event_id 
            FROM EventParticipation ep 
            JOIN events e ON ep.event_id = e.event_id 
            WHERE ep.user_id = %s 
            AND e.event_date = (SELECT ne.event_date FROM new_event ne) -- Date condition
            AND EXISTS (
                SELECT 1 
                FROM new_event ne
                WHERE (e.start_time, e.end_time) OVERLAPS (ne.start_time, ne.end_time)
            )

        """, (event_id, user_id))

        if cursor.fetchone():
            return jsonify({"error": "User has conflicting events"}), 409

        # Insert assignment
        cursor.execute("""
            INSERT INTO EventParticipation (user_id, event_id, responsibility)
            VALUES (%s, %s, %s)
        """, (user_id, event_id, responsibility))

        conn.commit()
        return jsonify({
            "message": "User assigned successfully",
            
        }), 201

    except psycopg2.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

