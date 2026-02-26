SELECT 
YEAR(races.date) as year, 
AVG(pit_stops.milliseconds)/1000 as avg_time_sec,
MIN(pit_stops.milliseconds)/1000 as min_time_sec
FROM pit_stops
JOIN races ON races.raceId = pit_stops.raceId
WHERE pit_stops.milliseconds < 50000
GROUP BY YEAR(races.date)
ORDER BY year ASC
