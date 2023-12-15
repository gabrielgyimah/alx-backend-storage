-- creates a stored procedure ComputeAverageWeightedScoreForUser that computes
-- and store the average weighted score for a student
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER ++
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id INT)
BEGIN
    SELECT SUM(corrections.score * projects.weight) / NULLIF(SUM(projects.weight), 0) AS average_weighted_score
    INTO @avg_score
    FROM corrections
    INNER JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    UPDATE users
    SET average_score = COALESCE(@avg_score, 0)
    WHERE id = user_id;
END ++
DELIMITER ;
