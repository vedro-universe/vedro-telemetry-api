SELECT name, count(*) as projects
FROM (
    SELECT
        s.project_id as project_id,
        p.name as name
    FROM sessions as s
    JOIN plugins as p
        ON p.session_id = s.id
    WHERE p.enabled IS TRUE
        AND saved_at BETWEEN $__timeFrom() AND $__timeTo()
        AND s.project_id != 'unknown'
    GROUP by s.project_id, p.name
) as t
GROUP by name
ORDER BY projects DESC, name ASC
