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

    def load_org(self, email):
        self.cursor.execute("SELECT UserID FROM Users WHERE Email=%s", (email,))
        userid = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT HallID, BookingDate, StartDate, EndDate FROM Booking WHERE UserID=%s", (userid,))
        raw_book_info = self.cursor.fetchall()
        book_info = {}
        for row in raw_book_info:
            if row[0] not in book_info.keys():
                self.cursor.execute("SELECT Loc, HallImg FROM Halls WHERE HallID=%s",)
                additional = self.cursor.fetchone()
                book_info[row[0]] = [[row[1]], [row[2]], [row[3]]] + additional

            else:
                book_info[row[0]][0].append(row[1])
                book_info[row[0]][1].append(row[2])
                book_info[row[0]][2].append(row[3])

        return book_info