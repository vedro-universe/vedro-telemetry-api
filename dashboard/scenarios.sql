SELECT project_id, discovered
FROM (
    SELECT
        DISTINCT ON (project_id)
        project_id,
        discovered
    FROM sessions
    WHERE discovered is not NULL
        AND saved_at BETWEEN $__timeFrom() AND $__timeTo()
        AND project_id != 'unknown'
    ORDER BY project_id ASC, discovered DESC
) as t
ORDER BY discovered DESC, project_id ASC
