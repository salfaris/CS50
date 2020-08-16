SELECT p.name
FROM people AS p
WHERE p.name IS NOT "Kevin Bacon" AND p.id IN (
    -- Get stars id that starred in such movies
    SELECT s.person_id
    FROM stars AS s
    WHERE s.movie_id IN(
        -- Get movies id that KB starred in
        SELECT s.movie_id
        FROM stars AS s
        WHERE person_id IN (
            -- Getting KB's id
            SELECT p.id
            FROM people AS p
            WHERE p.name = "Kevin Bacon" AND p.birth = 1958)));