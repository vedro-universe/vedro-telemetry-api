select
    project_id,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY elapsed) AS median,
    ROUND(AVG(elapsed), 2) as avg
from (
    SELECT
        project_id,
        EXTRACT(epoch FROM started_at) - EXTRACT(epoch FROM inited_at) as elapsed
    FROM sessions
    WHERE started_at is not NULL
        AND project_id != 'unknown'
        AND saved_at BETWEEN $__timeFrom() AND $__timeTo()
) as t
GROUP BY project_id
ORDER BY avg DESC, project_id ASC
