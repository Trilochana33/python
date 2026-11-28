from flask import Flask, jsonify
import pymysql

app = Flask(__name__)

def get_connection():
    connection = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = 'root',
        database = 'student_db'
    )
    return connection

@app.route('/students', methods = ['GET'])
def get_student():
    connection = get_connection()
    
    try:
        cursor = connection.cursor()
        query = "select * from student"
        cursor.execute(query)
        result = cursor.fetchall()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/student/<name>', methods = ['GET'])
def get_student_by_name(name):
    connection = get_connection()
    
    try:
        cursor = connection.cursor()
        query = "select * from student where name = %s"
        cursor.execute(query, (name))
        result = cursor.fetchall()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)