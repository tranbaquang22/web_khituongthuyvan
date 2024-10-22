import MySQLdb

# Cấu hình MySQL
def get_db_connection():
    connection = MySQLdb.connect(
        host="localhost",
        user="root",
        password="",
        db="weather_db3"
    )
    return connection
