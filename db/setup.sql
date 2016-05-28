CREATE TABLE Users (
  id INT NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(80) NOT NULL,
  last_name VARCHAR(80) NOT NULL,
  encrypted_password VARCHAR(225) NOT NULL,
  email VARCHAR(100) NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  sign_in_count INT DEFAULT 0,
  current_sign_in_at DATETIME NOT NULL,
  last_sign_in_at DATETIME NOT NULL,
  current_sign_in_ip DATETIME NOT NULL,
  last_sign_in_ip DATETIME NOT NULL,
  privilege INT NOT NULL,
  CONSTRAINT U_PK PRIMARY KEY(id)
);

CREATE TABLE Rooms (
   roomCode CHAR(5) PRIMARY KEY,
   roomName VARCHAR(30) UNIQUE,
   beds INT,  -- number of beds
   bedType VARCHAR(8),
   maxOcc INT,  -- max occupancy
   basePrice FLOAT,
   decor VARCHAR(20)
);

CREATE TABLE Reservations (
  code INT,
  room CHAR(5),
  checkIn DATE,
  checkOut DATE,
  rate FLOAT,
  adults INT,
  kids INT,
  CONSTRAINT RES_PK PRIMARY KEY(code),
  CONSTRAINT RES_UNIQUE UNIQUE(room, checkIn),
  CONSTRAINT RES_ROOM FOREIGN KEY(room) REFERENCES Rooms(roomCode)
);

CREATE TABLE Guests (
	id INT NOT NULL,
	first_name VARCHAR(80) NOT NULL,
  	last_name VARCHAR(80) NOT NULL,
  	age INT NOT NULL,
  	reservation_code INT,
  	CONSTRAINT G_PK PRIMARY KEY(id),
  	CONSTRAINT G_RES_CODE FOREIGN KEY(reservation_code) REFERENCES Reservations(code)
);
