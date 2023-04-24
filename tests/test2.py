import mysql.connector

config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'database': 'tt',
}

try:
    cnx = mysql.connector.connect(**config)
    print('Connected to MySQL database:', cnx.get_server_info())
    cursor = cnx.cursor()
    cursor.execute('SELECT DATABASE()')
    db_name = cursor.fetchone()[0]
    print('Connected to database:', db_name)
    cursor.close()
    cnx.close()
except mysql.connector.Error as err:
    print('Failed to connect to MySQL database:', err)