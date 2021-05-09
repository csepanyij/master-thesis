SELECT
    rel.name,
    rel.tag_name,
    rel.created_at
FROM releases rel
    INNER JOIN repositories rep ON (rel.repo_id = rep.id)
WHERE
    rep.owner = {owner} AND
    rep.name = {repo_name};