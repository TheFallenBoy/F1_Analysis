SELECT races.date, pit_stops.milliseconds
FROM pit_stops
JOIN races ON races.raceId = pit_stops.raceId
WHERE pit_stops.milliseconds < 50000
ORDER BY races.date asc