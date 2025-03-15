BEGIN;

DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    user_id UUID,
    username TEXT,
    email TEXT,
    first_name TEXT,
    last_name TEXT,
    bio TEXT,
    joined_at TIMESTAMP
);

DROP TABLE IF EXISTS posts CASCADE;
CREATE TABLE posts (
    post_id UUID,
    user_id UUID,
    community_id UUID,
    content TEXT,
    created_at TIMESTAMP
);

DROP TABLE IF EXISTS comments CASCADE;
CREATE TABLE comments (
    comment_id UUID,
    user_id UUID,
    post_id UUID,
    content TEXT,
    created_at TIMESTAMP
);

DROP TABLE IF EXISTS likes CASCADE;
CREATE TABLE likes (
    user_id UUID,
    target_type TEXT,
    target_id UUID,
    created_at TIMESTAMP
);

DROP TABLE IF EXISTS follows CASCADE;
CREATE TABLE follows (
    follower_id UUID,
    followee_id UUID,
    community_id UUID,
    created_at TIMESTAMP
);

DROP TABLE IF EXISTS messages CASCADE;
CREATE TABLE messages (
    sender_id UUID,
    receiver_id UUID,
    content TEXT,
    created_at TIMESTAMP,
    is_read BOOLEAN
);

DROP TABLE IF EXISTS communities CASCADE;
CREATE TABLE communities (
    community_id UUID,
    name TEXT,
    description TEXT,
    created_by TEXT,
    created_at TIMESTAMP
);