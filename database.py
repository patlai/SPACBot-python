import pymysql.cursors

host = "localhost"
user = "root"
password = ""
dbName = "test"


def insertMessage(email, message):
    connection = pymysql.connect(host = host, user = user, password = password, db = dbName, charset = 'utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `messages` (`msgID`, `email`, `message`) VALUES (uuid(), %s, %s)"
            cursor.execute(sql, (email, message))
        connection.commit()
    finally:
        connection.close()