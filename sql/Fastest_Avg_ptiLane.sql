SELECT constructors.name, AVG(pit_stops.milliseconds)/1000 AS average_pit_time_s
FROM pit_stops
JOIN results ON pit_stops.raceId = results.raceId
AND pit_stops.driverId = results.driverId
JOIN constructors ON results.constructorId = constructors.constructorId
WHERE pit_stops.milliseconds < 50000
GROUP BY constructors.name
ORDER BY average_pit_time_s ASC
LIMIT 1;