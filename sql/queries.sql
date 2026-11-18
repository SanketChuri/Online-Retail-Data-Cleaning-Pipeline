-- Does any invoice appear more than once?
SELECT invoice_no, COUNT(*) AS lines
FROM sales
GROUP BY invoice_no
HAVING COUNT(*) > 1
LIMIT 5;

SELECT * FROM sales
where sale_id = "123"


