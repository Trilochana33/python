from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'student_db'
}

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(**db_config)

# 1️⃣ Get all students
@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM student")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(students)

# 2️⃣ Get student by ID
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM student WHERE id = %s", (student_id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    if student:
        return jsonify(student)
    return jsonify({'error': 'Student not found'}), 404

# 3️⃣ Add a new student
@app.route('/students/add', methods=['POST'])
def add_student():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    college = data.get('college')
    if not name or not age or not college:
        return jsonify({'error': 'Name, Age, and College are required'}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO student (name, age, college) VALUES (%s, %s, %s)",
            (name, age, college)
        )
        conn.commit()
        return jsonify({'message': 'Student added successfully'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# 4️⃣ Update student by ID
@app.route('/students/update/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json
    name = data.get('name')
    age = data.get('age')
    college = data.get('college')
    if not name or not age or not college:
        return jsonify({'error': 'Name, Age, and College are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student WHERE id = %s", (student_id,))
    if not cursor.fetchone():
        return jsonify({'error': 'Student not found'}), 404

    try:
        cursor.execute(
            "UPDATE student SET name = %s, age = %s, college = %s WHERE id = %s",
            (name, age, college, student_id)
        )
        conn.commit()
        return jsonify({'message': 'Student updated successfully'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# 5️⃣ Delete student by ID
@app.route('/students/delete/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student WHERE id = %s", (student_id,))
    if not cursor.fetchone():
        return jsonify({'error': 'Student not found'}), 404

    try:
        cursor.execute("DELETE FROM student WHERE id = %s", (student_id,))
        conn.commit()
        return jsonify({'message': 'Student deleted successfully'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# 🔹 Simple Hello route
@app.route('/')
def index():
    return "Hello"

# Entry Point
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)