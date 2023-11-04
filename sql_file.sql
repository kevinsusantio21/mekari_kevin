SELECT
    r.year,
    r.month,
    r.branch_id,
    ROUND(SUM(r.salary) / SUM(r.hours_worked)) AS salary_per_hour
FROM
(
    SELECT 
        t.employee_id,
        e.branch_id,
        CASE WHEN t.employee_id = '218078'
			THEN 13000000
            ELSE e.salary
		END AS salary,
        LEFT(t.date, 4) AS year,
        SUBSTRING(t.date, 6, 2) AS month,
        SUM(TIME_TO_SEC(IFNULL(t.checkout, '17:00:00')) - TIME_TO_SEC(IFNULL(t.checkin, '09:00:00')))/3600.0 AS hours_worked,
        e.salary / (SUM(TIME_TO_SEC(IFNULL(t.checkout, '17:00:00')) - TIME_TO_SEC(IFNULL(t.checkin, '09:00:00')))/3600.0) AS salary_per_hour
    FROM timesheets t
    INNER JOIN employees e
    ON t.employee_id = e.employe_id
    GROUP BY t.employee_id, e.branch_id, year, month, e.salary
) r
GROUP BY r.branch_id, r.year, r.month
ORDER BY r.year, r.month, r.branch_id;