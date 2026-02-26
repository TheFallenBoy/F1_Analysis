SELECT constructors.name as constructor, count(results.resultId) as TotalWins 
FROM results
JOIN races ON results.raceId = races.raceId
JOIN constructors ON constructors.constructorId = results.constructorId
WHERE results.position = 1
AND races.year between 2020 AND 2020
GROUP BY constructors.name
ORDER BY TotalWins DESC
LIMIT 1
