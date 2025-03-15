from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

client = MongoClient("mongodb://root:example@mongodb:27017/")
db = client.social_media

users_collection = db.users
communities_collection = db.communities
posts_collection = db.posts
comments_collection = db.comments
likes_collection = db.likes
follows_collection = db.follows
messages_collection = db.messages

users_collection.delete_many({})
communities_collection.delete_many({})
posts_collection.delete_many({})
comments_collection.delete_many({})
likes_collection.delete_many({})
follows_collection.delete_many({})
messages_collection.delete_many({})

def generate_users(num_users=100):
    users = []
    for _ in range(num_users):
        user = {
            "user_id": fake.uuid4(),
            "username": fake.user_name(),
            "email": fake.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "bio": fake.text(max_nb_chars=200),
            "joined_at": fake.date_time_between(start_date="-2y", end_date="now"),
        }
        users.append(user)
    users_collection.insert_many(users)
    print(f"Generated {num_users} users.")

def generate_communities(num_communities=20):
    users = list(users_collection.find({}, {"user_id": 1}))
    communities = []
    for _ in range(num_communities):
        community = {
            "community_id": fake.uuid4(),
            "name": fake.company(),
            "description": fake.text(max_nb_chars=300),
            "created_by": random.choice(users)["user_id"],
            "created_at": fake.date_time_between(start_date="-1y", end_date="now"),
        }
        communities.append(community)
    communities_collection.insert_many(communities)
    print(f"Generated {num_communities} communities.")

def generate_posts(num_posts=500):
    users = list(users_collection.find({}, {"user_id": 1}))
    communities = list(communities_collection.find({}, {"community_id": 1}))
    posts = []
    for _ in range(num_posts):
        if random.choice([True, False]):
            post = {
                "post_id": fake.uuid4(),
                "user_id": random.choice(users)["user_id"],
                "community_id": None,
                "content": fake.text(max_nb_chars=500),
                "created_at": fake.date_time_between(start_date="-1y", end_date="now"),
            }
        else:
            post = {
                "post_id": fake.uuid4(),
                "user_id": None,
                "community_id": random.choice(communities)["community_id"],
                "content": fake.text(max_nb_chars=500),
                "created_at": fake.date_time_between(start_date="-1y", end_date="now"),
            }
        posts.append(post)
    posts_collection.insert_many(posts)
    print(f"Generated {num_posts} posts.")

def generate_comments(num_comments=2000):
    users = list(users_collection.find({}, {"user_id": 1}))
    posts = list(posts_collection.find({}, {"post_id": 1}))
    comments = []
    for _ in range(num_comments):
        comment = {
            "comment_id": fake.uuid4(),
            "user_id": random.choice(users)["user_id"],
            "post_id": random.choice(posts)["post_id"],
            "content": fake.text(max_nb_chars=200),
            "created_at": fake.date_time_between(start_date="-1y", end_date="now"),
        }
        comments.append(comment)
    comments_collection.insert_many(comments)
    print(f"Generated {num_comments} comments.")

def generate_likes(num_likes=3000):
    users = list(users_collection.find({}, {"user_id": 1}))
    posts = list(posts_collection.find({}, {"post_id": 1}))
    comments = list(comments_collection.find({}, {"comment_id": 1}))
    likes = []
    for _ in range(num_likes):
        if random.choice([True, False]):
            like = {
                "user_id": random.choice(users)["user_id"],
                "target_type": "post",
                "target_id": random.choice(posts)["post_id"],
                "created_at": fake.date_time_between(start_date="-1y", end_date="now"),
            }
        else:
            like = {
                "user_id": random.choice(users)["user_id"],
                "target_type": "comment",
                "target_id": random.choice(comments)["comment_id"],
                "created_at": fake.date_time_between(start_date="-1y", end_date="now"),
            }
        likes.append(like)
    likes_collection.insert_many(likes)
    print(f"Generated {num_likes} likes.")

def generate_follows(num_follows=1000):
    users = list(users_collection.find({}, {"user_id": 1}))
    communities = list(communities_collection.find({}, {"community_id": 1}))
    follows = []
    for _ in range(num_follows):
        if random.choice([True, False]):
            follower, followee = random.sample(users, 2)
            follow = {
                "follower_id": follower["user_id"],
                "followee_id": followee["user_id"],
                "community_id": None,
                "created_at": fake.date_time_between(start_date="-1y", end_date="now"),
            }
        else:
            follower = random.choice(users)
            community = random.choice(communities)
            follow = {
                "follower_id": follower["user_id"],
                "followee_id": None,
                "community_id": community["community_id"],
                "created_at": fake.date_time_between(start_date="-1y", end_date="now"),
            }
        follows.append(follow)
    follows_collection.insert_many(follows)
    print(f"Generated {num_follows} follows.")

def generate_messages(num_messages=1500):
    users = list(users_collection.find({}, {"user_id": 1}))
    messages = []
    for _ in range(num_messages):
        sender, receiver = random.sample(users, 2)
        message = {
            "sender_id": sender["user_id"],
            "receiver_id": receiver["user_id"],
            "content": fake.text(max_nb_chars=200),
            "created_at": fake.date_time_between(start_date="-1y", end_date="now"),
            "is_read": random.choice([True, False]),
        }
        messages.append(message)
    messages_collection.insert_many(messages)
    print(f"Generated {num_messages} messages.")

# Основная функция
if __name__ == "__main__":
    generate_users()
    generate_communities()
    generate_posts()
    generate_comments()
    generate_likes()
    generate_follows()
    generate_messages()
    print("Data generation complete.")