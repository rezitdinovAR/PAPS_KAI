import psycopg2

class DB:
    def __init__(self):
        connection = psycopg2.connect(
            user="postgres",
            password="21032003",
            host="localhost",
            port="5432",
            database="MeroSearch",
        )

        self.cursor = connection.cursor()

    def authorize(self, email, password):
        self.cursor.execute("SELECT count(*) FROM Users WHERE Email=%s", (email,))
        if not self.cursor.fetchone()[0]:
            self.cursor.execute("SELECT Password FROM users WHERE Email=%s", (email,))
            if self.cursor.fetchone() == password:
                self.cursor.execute("SELECT UserType FROM Users WHERE Email=%s", (email,))
                return self.cursor.fetchone()
            else:
                return "Incorrect Password"
        else:
            return "Incorrect Email"

