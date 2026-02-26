DROP PROCEDURE IF EXISTS ADD_LAPTIME;
DELIMITER //
CREATE PROCEDURE ADD_LAPTIME (
IN raceName VARCHAR(255), 
IN raceDate VARCHAR(255),
IN driverFName VARCHAR(255),
IN driverLName VARCHAR(255),
IN p_lap INT, 
IN p_position INT,
IN p_time VARCHAR(255),
IN p_milliseconds INT, 
OUT success INT
)
	BEGIN
		DECLARE v_raceId INT;
        DECLARE v_driverId INT;
		
        SET v_driverId = (SELECT drivers.driverId FROM drivers WHERE drivers.forename = driverFName AND drivers.surname = driverLName LIMIT 1);
        SET v_raceId = (SELECT races.raceId FROM races WHERE races.name = raceName AND races.date = raceDate LIMIT 1);
        IF v_driverId IS NULL OR v_raceId IS NULL THEN
			SET success = -1;
        ELSE
			INSERT IGNORE lap_times (raceId,driverId,lap,position,time,milliseconds) -- IGNORE ensures so that no dublicates of the same lap is entered.
			VALUES (v_raceId, v_driverId, p_lap, p_position,p_time,p_milliseconds);
			SET success = 0;
		END IF;
        
    END //
DELIMITER ;

