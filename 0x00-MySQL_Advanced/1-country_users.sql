-- The sql script creates the table users
-- with the following attributes
-- id(integer, never null, auto increment and Primary)
-- email(string 255 characters, never null and unique)
-- name (string, 255 characters)
-- country (enumeration of countries US, CO, and TN never
-- null

CREATE TABLE IF NOT EXISTS users (
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255),
	country ENUM("US", "CO", "TN") DEFAULT "US" NOT NULL
	
);
