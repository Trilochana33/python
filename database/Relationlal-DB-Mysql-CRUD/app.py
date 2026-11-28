import pymysql


def get_connection():
    connection = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = 'root',
        database = 'student_db'
    )
    return connection

def get_studetn():
    connection = get_connection()
    
    try:
        cursor = connection.cursor()
        query = "select * from student"
        cursor.execute(query)
        result = cursor.fetchall()
        
        return result
    except Exception as e:
        print("Error while fetching student data:", e)
    finally:
        cursor.close()
        connection.close()
        
def get_studetn_by_name(name):
    connection = get_connection()
    
    try:
        cursor = connection.cursor()
        query = "select * from student where name = %s"
        cursor.execute(query, (name))
        result = cursor.fetchall()
        
        return result
    except Exception as e:
        print("Error while fetching student data:", e)
    finally:
        cursor.close()
        connection.close()
        
        return result

result = get_studetn()

result_1 = get_studetn_by_name('Priya')

for student in result:
    print (student)

for student in result_1:
    print (student)
    