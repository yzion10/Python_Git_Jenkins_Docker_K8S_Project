import pymysql

# This class connect to a remote MySql
# and implements a couple of methods (INSERT,SELECT,UPDATE,DELETE)
class DBConnector:

    # initialize the class (constructor)
    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.conn = None

    # create the connection to the MySql
    def connect(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db)

    # close the connection to the MySql
    def disconnect(self):
        if self.conn is not None:
            self.conn.close()

    # add new user to users table
    def addUser(self, user_id, user_name):
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                # sql = f"INSERT INTO users VALUES ({user_id}, '{user_name}', NOW())"
                sql = "INSERT INTO users VALUES (%s, %s, NOW())"
                cursor.execute(sql, (user_id, user_name)) # prepared statement
                self.conn.commit()
        finally:
            self.disconnect()

    # return the username by the user_id parameter
    def getUserName(self, user_id):
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                sql = f"SELECT user_name FROM users WHERE user_id = %s"
                cursor.execute(sql, user_id) # prepared statement
                result = cursor.fetchone() # fetchone = returns a single record or None if no more rows are available
                if result is not None:
                    return result[0]
                else:
                    return None
        finally:
            self.disconnect()

    # update the username by the user_id parameter
    def updateUserName(self, user_id, user_name):
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                sql = f"UPDATE users SET user_name = %s WHERE user_id = %s"
                cursor.execute(sql, (user_name, user_id)) # prepared statement
                self.conn.commit()
        finally:
            self.disconnect()

    # delete the username by the user_id parameter
    def deleteUser(self, user_id):
        self.connect()
        try:
            with self.conn.cursor() as cursor:
                sql = f"DELETE FROM users WHERE user_id = %s"
                cursor.execute(sql, user_id) # prepared statement
                self.conn.commit()
        finally:
            self.disconnect()
