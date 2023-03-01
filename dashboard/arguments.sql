SELECT
    name,
    count(*) as count
FROM sessions as s
JOIN arguments as e
    ON s.id = e.session_id
WHERE saved_at BETWEEN $__timeFrom() AND $__timeTo()
GROUP BY name
ORDER BY count DESC, name ASC
