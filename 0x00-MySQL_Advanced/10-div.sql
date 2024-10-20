-- An sql script that creates a function SafeDiv that
-- deides (and returns) the first by the second number
-- or returns 0 if the second number is equal to 0

DELIMITER //

DROP FUNCTION IF EXISTS SafeDiv;
CREATE function SafeDiv(a INT, b INT)

returns FLOAT Deterministic

BEGIN
	return(IF (b = 0, 0, a / b));
END//

DELIMITER;