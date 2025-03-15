DROP TABLE IF EXISTS community_activity;

CREATE TABLE community_activity AS
SELECT
    c.community_id,
    COUNT(DISTINCT p.post_id) as posts,
    COUNT(DISTINCT f.follower_id) as follows
FROM
    communities c
LEFT JOIN
    posts p ON p.community_id = c.community_id
LEFT JOIN 
    follows f ON f.community_id = c.community_id
GROUP BY c.community_id;