import psycopg2

class DB:
    def __init__(self):
        self.connection = psycopg2.connect(
            user="postgres",
            password="21032003",
            host="localhost",
            port="5432",
            database="MeroPoisk",
        )

        self.cursor = self.connection.cursor()

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
            self.connection.commit()
            return "OK"
        else:
            return "Incorrect Email"

    def load_org(self, email):
        self.cursor.execute("SELECT UserID FROM Users WHERE Email=%s", (email,))
        userid = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT HallID, BookingDate, StartDate, EndDate FROM Bookings WHERE UserID=%s", (userid,))
        raw_book_info = self.cursor.fetchall()
        book_info = {}
        for row in raw_book_info:
            if row[0] not in book_info.keys():
                self.cursor.execute("SELECT Loc, HallImg FROM Halls WHERE HallID=%s",(row[0],))
                additional = self.cursor.fetchone()
                book_info[row[0]] = [[row[1]], [row[2]], [row[3]]] + [additional[0], additional[1]]

            else:
                book_info[row[0]][0].append(row[1])
                book_info[row[0]][1].append(row[2])
                book_info[row[0]][2].append(row[3])

        return book_info

    def delete_booking(self, address, date_of_book, start_date, end_date):
        self.cursor.execute("SELECT HallID FROM Halls WHERE Loc=%s", (address,))
        hallid = self.cursor.fetchone()[0]

        try:
            self.cursor.execute(
                "DELETE FROM Bookings WHERE HallID=%s AND BookingDate=%s AND StartDate=%s AND EndDate=%s",
                (hallid, date_of_book, start_date, end_date))
            self.connection.commit()

        except Exception as e:
            status = "Error"

        else:
            status = "OK"

        return status

    def load_own(self, email):
        self.cursor.execute("SELECT UserID FROM Users WHERE Email=%s", (email,))
        userid = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT HallID, Loc, HallImg FROM Halls WHERE OwnerID=%s", (userid,))
        halls = self.cursor.fetchall()
        book_info = {}

        for hall in halls:
            self.cursor.execute("SELECT BookingDate, StartDate, EndDate FROM Bookings WHERE HallID=%s",(hall[0],))
            bookings = self.cursor.fetchall()
            book_info[hall[1]] = (bookings, hall[2])

        return book_info

    def add_hall(self, email, loc, capacity, equip, desc, rent, hall_img):
        try:
            self.cursor.execute("SELECT UserID FROM Users WHERE Email=%s", (email,))
            owner = self.cursor.fetchone()[0]
            self.cursor.execute("INSERT INTO Halls(OwnerID, Loc, Capacity, EquipmentDetails, HallDescription, RentalPrice, HallImg) VALUES (%s, %s, %s, %s, %s, %s, %s)", (owner, loc, capacity, equip, desc, rent, hall_img))
            self.connection.commit()
        except Exception as e:
            print(e)
            status = "Error"
        else:
            status = "OK"

        return status

    def del_hall(self, address):
        self.cursor.execute("SELECT HallID FROM Halls WHERE Loc=%s", (address,))
        hall = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT BookingID FROM Bookings WHERE HallID=%s", (hall,))
        bookings = self.cursor.fetchone()[0]
        if bookings:
            try:
                self.cursor.execute("DELETE FROM Reviews WHERE HallID=%s", (hall,))
                self.connection.commit()
                self.cursor.execute("DELETE FROM Halls WHERE Loc=%s", (address,))
                self.connection.commit()

            except Exception as e:
                print(e)
                status = "Error"

            else:
                status = "OK"
        else:
            status = "Hall has bookings"

        return status

    def list_halls(self):
        self.cursor.execute("SELECT Loc, HallDescription, HallImg FROM Halls")
        halls = self.cursor.fetchall()
        info={}

        for hall in halls:
            info[hall[0]] = [hall[1], hall[2]]

        return info

    def hall_page(self, address):
        print(address)
        self.cursor.execute("SELECT Capacity, EquipmentDetails, HallDescription, RentalPrice, HallImg FROM Halls WHERE Loc=%s", (address,))
        hall = self.cursor.fetchone()
        return hall

    def list_reviews(self, address):
        self.cursor.execute("SELECT HallID FROM Halls WHERE Loc=%s", (address,))
        hall = self.cursor.fetchone()[0]
        info = {}


        self.cursor.execute("SELECT RevCom, Response FROM Reviews WHERE HallID=%s", (hall,))
        reviews = self.cursor.fetchall()
        revs = []

        for review in reviews:
            revs.append([review[0], review[1]])

        info[hall] = revs

        return info

    def add_review(self, address, revcom, resp):
        try:
            self.cursor.execute("SELECT HallID FROM Halls WHERE Loc=%s", (address,))
            hall = self.cursor.fetchone()[0]
            self.cursor.execute("INSERT INTO Reviews (HallID, RevCom, Response) VALUES (%s, %s, %s)", (hall, revcom, resp))
            self.connection.commit()

        except Exception as e:
            status = "Error"

        else:
            status = "OK"

        return status
    def list_times(self, address):
        self.cursor.execute("SELECT HallID FROM Halls WHERE Loc=%s", (address,))
        hall = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT BookingDate, StartDate, EndDate FROM Bookings WHERE HallID=%s", (hall,))
        booked_times = self.cursor.fetchall()
        info = {}

        for booked_time in booked_times:
            info[booked_time[0]] = [booked_time[1], booked_time[2]]

        return info

    def add_booking(self, Email, Address, BookingDate, StartDate, EndDate):
        self.cursor.execute("SELECT UserID FROM Users WHERE Email=%s",(Email))
        UserID = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT HallID FROM Halls WHERE Loc=%s", (Address))
        HallID = self.cursor.fetchone()[0]

        try:
            self.cursor.execute("INSERT INTO Bookings (UserID, HallID, BookingDate, StartDate, EndDate) VALUES (%s, %s, %s, %s, %s)",(UserID, HallID, BookingDate, StartDate, EndDate))
            self.connection.commit()

        except Exception as e:
            status = "Error"

        else:
            status = "OK"

        return status