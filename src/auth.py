import hashlib
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import jsonify, request, session, Blueprint
import psycopg2
from config.db_config import get_db_connection

auth = Blueprint('auth', __name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth.route('/register/admin', methods=['POST'])
def register_admin():
    data = request.json
    user_id = data.get('user_id')
    username = data.get('username')
    password = data.get('password')
    user_role = 'admin'

    if not all([user_id, username, password]):
        return jsonify({"error": "Missing required fields"}), 400

    hashed_password = hash_password(password)

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (user_id, username, user_role, user_pass) VALUES (%s, %s, %s, %s)",
                       (user_id, username, user_role, hashed_password))
        conn.commit()
        return jsonify({"message": "Admin registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@auth.route('/register/student', methods=['POST'])
def register_student():
    data = request.json
    user_id = data.get('user_id')
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone')
    student_class = data.get('student_class')
    user_role = 'Student'

    if not all([user_id, username, password, email, phone, student_class]):
        return jsonify({"error": "Missing required fields"}), 400

    hashed_password = hash_password(password)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # First insert into Users table
        cursor.execute("INSERT INTO Users (user_id, username, user_role, user_pass) VALUES (%s, %s, %s, %s)",
                       (user_id, username, user_role, hashed_password))
        # Then insert into Students table
        cursor.execute("INSERT INTO Students (user_id, email, phone, student_class) VALUES (%s, %s, %s, %s)",
                       (user_id, email, phone, student_class))
        conn.commit()
        return jsonify({"message": "Student registered successfully"}), 201
    except psycopg2.Error as err:
        conn.rollback()
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@auth.route('/register/teacher', methods=['POST'])
def register_teacher():
    data = request.json
    user_id = data.get('user_id')
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone')
    user_role = 'Teacher'

    if not all([user_id, username, password, email, phone]):
        return jsonify({"error": "Missing required fields"}), 400

    hashed_password = hash_password(password)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # First insert into Users table
        cursor.execute("INSERT INTO Users (user_id, username, user_role, user_pass) VALUES (%s, %s, %s, %s)",
                       (user_id, username, user_role, hashed_password))
        # Then insert into Teachers table
        cursor.execute("INSERT INTO Teachers (user_id, email, phone) VALUES (%s, %s, %s)",
                       (user_id, email, phone))
        conn.commit()
        return jsonify({"message": "Teacher registered successfully"}), 201
    except psycopg2.Error as err:
        conn.rollback()
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@auth.route('/login', methods=['POST'])
def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({"error": "Missing username or password"}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, user_role, user_pass FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and hash_password(password) == user[2]:
            session['user_id'] = user[0]
            session['role'] = user[1]
            return jsonify({"message": "Login successful", "user_id": user[0], "role": user[1]}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@auth.route('/logout', methods=['POST'])
def logout_user():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200