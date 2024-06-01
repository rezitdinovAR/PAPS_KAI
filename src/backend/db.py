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
        self.cursor.execute(f"SELECT count(*) FROM users WHERE email={email}")
        if self.cursor.fetchone():
            self.cursor.execute(f"SELECT Password FROM users WHERE email={email}")
            if self.cursor.fetchone() == password:
                self.cursor.execute(f"SELECT UserType FROM users WHERE email={email}")
                return self.cursor.fetchone()
            else:
                return "Incorrect Password"
        else:
            return "Incorrect Email"

