DROP TABLE IF EXISTS user_activity;

CREATE TABLE user_activity AS
SELECT
    u.user_id,
    u.joined_at,
    COUNT(DISTINCT p.post_id) as posts,
    COUNT(DISTINCT c.comment_id) as comments,
    COUNT(DISTINCT l.target_id) as likes,
    COUNT(DISTINCT f.followee_id) as follows
FROM
    users u
LEFT JOIN
    posts p ON p.user_id = u.user_id
LEFT JOIN
    comments c ON c.user_id = u.user_id
LEFT JOIN
    likes l ON l.user_id = u.user_id
LEFT JOIN 
    follows f ON f.follower_id = u.user_id
GROUP BY u.user_id, u.joined_at;