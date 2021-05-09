SELECT 
    c.hash,
    c.author_date,
    c.no_of_modifications,
    sum(e.total_added_lines) as lines_added,
    sum(e.total_removed_lines) as lines_removed
FROM commits c
    INNER JOIN edits e on (c.hash = e.commit_hash)
GROUP BY
    c.hash,
    c.author_date,
    c.no_of_modifications;