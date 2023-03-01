SELECT
    DISTINCT ON (project_id)
    project_id,
    first_value(substring(environment->>'python_version', '^\S+')) OVER (
        PARTITION BY project_id ORDER BY saved_at DESC
        RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as python_version,
    last_value(environment->>'vedro_version') OVER (
        PARTITION BY project_id ORDER BY saved_at DESC
        RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) as vedro_version
FROM sessions
WHERE environment->>'vedro_version' IS NOT NULL
    AND discovered IS NOT NULL
    AND project_id != 'unknown'
    AND saved_at BETWEEN $__timeFrom() AND $__timeTo()
ORDER BY project_id ASC
