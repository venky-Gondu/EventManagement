### event.py
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Blueprint, request, jsonify, session

__all__ = ['event_blueprint']
import psycopg2
from config.db_config import get_db_connection

event_blueprint = Blueprint('event', __name__)

@event_blueprint.route('/create_event', methods=['POST'])
def create_event():
    if 'user_id' not in session or session['role'] not in ['admin', 'Teacher']:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    event_id = data.get("event_id")
    event_name = data.get("event_name")
    event_date = data.get("event_date")
    event_start_time = data.get("event_start_time")
    event_end_time = data.get("event_end_time")
    event_venue = data.get("event_venue")
    created_by = session['user_id']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Events (event_id, event_name, event_date, event_start_time, event_end_time, event_venue, created_by) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (event_id, event_name, event_date, event_start_time, event_end_time, event_venue, created_by))
        conn.commit()
        return jsonify({"message": "Event created successfully"}), 201
    except psycopg2.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@event_blueprint.route('/list_events', methods=['GET'])
def list_events():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT event_id, event_name, event_date, event_venue FROM Events")
        events = cursor.fetchall()
        return jsonify({"events": events}), 200
    except psycopg2.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@event_blueprint.route('/delete_past_events', methods=['DELETE'])
def delete_past_events():
    if 'user_id' not in session or session['role'] not in ['Admin']:
        return jsonify({"error": "Unauthorized"}), 403
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Events WHERE event_date < CURRENT_DATE or(event_date = CURRENT_DATE and current_time > event_time)")
        conn.commit()
        return jsonify({"message": "Past events deleted successfully"}), 200
    except psycopg2.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close() 

@event_blueprint.route('/edit_event/<event_id>', methods=['PUT'])
def edit_event(event_id):
    """Edit an existing event."""
    data = request.json
    event_name = data.get("event_name")
    event_date = data.get("event_date")
    event_start_time = data.get("event_start_time")
    event_end_time = data.get("event_end_time")
    event_venue = data.get("event_venue")
    updated_by = data.get("updated_by")  # The user making the edit

    if not all([event_name, event_date, event_start_time, event_end_time, event_venue, updated_by]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verify that the editor is an Admin or Teacher
        cursor.execute("SELECT COUNT(*) FROM Users WHERE user_id = %s AND user_role IN ('Admin', 'Teacher')", (updated_by,))
        user_exists = cursor.fetchone()[0]

        if user_exists == 0:
            return jsonify({"error": "Unauthorized user. Only Admins or Teachers can edit events."}), 403

        # Check if the event exists
        cursor.execute("SELECT COUNT(*) FROM Events WHERE event_id = %s", (event_id,))
        event_exists = cursor.fetchone()[0]

        if event_exists == 0:
            return jsonify({"error": "Event not found"}), 404

        # Update the event details
        cursor.execute("""
            UPDATE Events 
            SET event_name = %s, event_date = %s, event_start_time = %s, event_end_time = %s, event_venue = %s
            WHERE event_id = %s
        """, (event_name, event_date, event_start_time, event_end_time, event_venue, event_id))

        conn.commit()
        return jsonify({"message": "✅ Event updated successfully!"}), 200

    except psycopg2.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

