SELECT results.driverId, drivers.forename, drivers.surname, COUNT(results.driverId) AS TotalWins
FROM results
INNER JOIN drivers
ON drivers.driverId = results.driverId
WHERE results.position = 1
GROUP BY results.driverId
ORDER BY TotalWins DESC
LIMIT 5;