SELECT
    issues.issue_title,
    issues.issue_number,
    issues.created_at,
    issues.closed_at

FROM issues
    INNER JOIN repositories rep ON (issues.repo_id = rep.id)
    
WHERE
    rep.owner = {owner} AND
    rep.name = {repo_name};
