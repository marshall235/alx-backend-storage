-- The script creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and stores the average weighted score for a student


DELIMITER $$
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;;
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
	UPDATE users set average_score = (
		SELECT(corrections.score * projects.weight) / SUM(projects.weight)
		FROM corrections
		INNER JOIN projects
		ON projects.id = corrections.project_id
		where corrections.user_id = user_id)
	        WHERE users.id = user_id;
END $$
DELIMITER ;
