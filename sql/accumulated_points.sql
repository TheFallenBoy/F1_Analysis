DELIMITER //

    CREATE FUNCTION ACCUMULATED_POINTS(p_team VARCHAR(255), p_year INT)
    RETURNS INT DETERMINISTIC
    BEGIN
        DECLARE total_sum INT;
        DECLARE team_id INT;
        SET team_id = (SELECT constructorId FROM constructors WHERE p_team = name LIMIT 1);
        IF team_id IS NULL OR p_year NOT IN (SELECT races.year FROM races) THEN
            RETURN -1;
        END IF;
        SELECT IFNULL(SUM(results.points),0)
        INTO total_sum
        FROM results
        JOIN races ON races.raceId = results.raceId AND races.year = p_year
        WHERE results.constructorId = team_id;
        
        RETURN total_sum;
        
    END //
    DELIMITER ;