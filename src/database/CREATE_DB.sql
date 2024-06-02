CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Password VARCHAR(100) NOT NULL,
    UserType VARCHAR(20) NOT NULL
);

CREATE TABLE Halls (
    HallID SERIAL PRIMARY KEY,
    OwnerID INT REFERENCES Users(UserID),
    Loc VARCHAR(100) NOT NULL,
    Capacity INT NOT NULL,
    EquipmentDetails TEXT,
    HallDescription TEXT,
    RentalPrice NUMERIC(10, 2) NOT NULL,
	HallImg TEXT
);

CREATE TABLE Bookings (
    BookingID SERIAL PRIMARY KEY,
    UserID INT REFERENCES Users(UserID),
    HallID INT REFERENCES Halls(HallID),
    BookingDate DATE NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    Status VARCHAR(20) NOT NULL
);

CREATE TABLE Reviews (
    ReviewID SERIAL PRIMARY KEY,
    HallID INT REFERENCES Halls(HallID),
    RevCom TEXT,
    Response TEXT
);

CREATE TABLE Payments (
    PaymentID SERIAL PRIMARY KEY,
    BookingID INT REFERENCES Bookings(BookingID),
    Amount NUMERIC(10, 2) NOT NULL,
    PaymentDate DATE NOT NULL,
    PaymentStatus VARCHAR(20) NOT NULL
);