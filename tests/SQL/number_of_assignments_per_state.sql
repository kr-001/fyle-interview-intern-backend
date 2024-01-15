-- Write query to get number of assignments for each state

SELECT 
    state, 
    COUNT(*) as number_of_assignments
FROM 
    assignments
GROUP BY 
    state;