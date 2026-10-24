
SELECT
    d.dept_name,
    COUNT(DISTINCT s.student_id) AS student_count,
    ROUND(AVG(e.marks), 2) AS average_marks
FROM departments AS d
JOIN students AS s
    ON s.dept_id = d.dept_id
JOIN enrollments AS e
    ON e.student_id = s.student_id
WHERE e.course = 'DBMS'
GROUP BY d.dept_id, d.dept_name
HAVING COUNT(DISTINCT s.student_id) >= 3
ORDER BY average_marks DESC, d.dept_name ASC;
