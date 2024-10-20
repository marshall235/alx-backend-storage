-- An SQL Script that creates a view need_meeting
-- that lists all students that have the score under
-- 80 and no last_meeting or more than one month


DROP VIEW IF EXISTS need_meeting;
CREATE VIEW need_meeting AS
SELECT name FROM students WHERE score < 80
AND (students.last_meeting IS NULL OR students.last_meeting < DATE_ADD(NOW(), INTERVAL -1 MONTH));
