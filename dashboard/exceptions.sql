SELECT
    type,
    count(*) as count
FROM sessions as s
JOIN exceptions as e
    ON s.id = e.session_id
WHERE saved_at BETWEEN $__timeFrom() AND $__timeTo()
GROUP BY type
ORDER BY count DESC, type ASC
