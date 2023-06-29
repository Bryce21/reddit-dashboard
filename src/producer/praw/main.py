import praw
from classes import Post, Comment
from kafka import ProducerWrapper
import HealthCheck
from confluent_kafka import Producer
import socket
import atexit
from confluent_kafka import Producer
import socket
import asyncio
import json



reddit = praw.Reddit(
    client_id="1lb14v6vpEASB83rdUeAGg",
    client_secret="XFJourPG18yjLhwxMTeUnfMgWCYQFA",
    user_agent="praw_reddit_producer"
)


if __name__ == '__main__':
    producer = ProducerWrapper.ProducerWrapper()
    atexit.register(producer.close_producer)

    health_check = HealthCheck.HealthCheck(producer, 5.0)
    health_check.start()




    subreddit = reddit.subreddit("all")
    for submission in subreddit.stream.submissions():
        submission.comments.replace_more(limit=None)
        sub = Post.Post.createFromPost(submission)
        producer.produce(topic="dirty_posts", key=sub.subredditName, value=sub.getJSON())

        #print(sub.getJSON())
        for comment in submission.comments.list():
            c = Comment.Comment.createFromComment(comment, sub.id)
            #print(c.getJSON())
            producer.produce("dirty_comments", key=c.postID, value=c.getJSON())
            # print("Post id: " + sub.id + ", Author: " + c.author + ", Parent id: " + c.parent_id, "Subreddit: " + c.subredditName)


