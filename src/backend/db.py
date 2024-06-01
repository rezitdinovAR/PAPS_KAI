import psycopg2

class DB:
    def __init__(self):
        connection = psycopg2.connect(
            user="postgres",
            password="21032003",
            host="localhost",
            port="5432",
            database="MeroPoisk",
        )

        self.cursor = connection.cursor()

    def authorize(self, email, password):
        self.cursor.execute("SELECT count(*) FROM Users WHERE Email=%s", (email,))
        if self.cursor.fetchone()[0]:
            self.cursor.execute("SELECT Password FROM users WHERE Email=%s", (email,))
            if self.cursor.fetchone()[0] == password:
                self.cursor.execute("SELECT UserType FROM Users WHERE Email=%s", (email,))
                return self.cursor.fetchone()[0]
            else:
                return "Incorrect Password"
        else:
            return "Incorrect Email"

    def registrate(self, email, password, usertype):
        self.cursor.execute("SELECT count(*) FROM Users WHERE Email=%s", (email,))
        if not self.cursor.fetchone()[0]:
            self.cursor.execute("INSERT INTO Users (Email, Password, UserType) VALUES (%s, %s, %s)", (email, password, usertype))
            return "OK"
        else:
            return "Incorrect Email"
