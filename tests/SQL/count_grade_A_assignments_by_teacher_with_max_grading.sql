-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH teacher_grades AS (
    SELECT 
        teacher_id, 
        COUNT(*) as total_assignments,
        SUM(CASE WHEN grade = 'A' THEN 1 ELSE 0 END) as grade_a_count
    FROM 
        assignments
    WHERE 
        state = 'GRADED'
    GROUP BY 
        teacher_id
),
max_grading_teacher AS (
    SELECT 
        teacher_id
    FROM 
        teacher_grades
    ORDER BY 
        total_assignments DESC
    LIMIT 1
)
SELECT 
    grade_a_count
FROM 
    teacher_grades
WHERE 
    teacher_id = (SELECT teacher_id FROM max_grading_teacher);
