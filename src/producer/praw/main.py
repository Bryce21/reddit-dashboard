import praw
from classes import Post, Comment
from kafka import ProducerWrapper
import HealthCheck
import atexit
import os
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()
    producer = ProducerWrapper.ProducerWrapper(
        host=os.getenv("KAFKA_HOST"),
        port=os.getenv("KAFKA_PORT")
    )
    atexit.register(producer.close_producer)

    health_check = HealthCheck.HealthCheck(
        producer, float(str(os.getenv("HEALTHCHECK_INTERVAL")))
    )
    health_check.start()


    reddit = praw.Reddit(
        client_id=str(os.getenv("CLIENT_ID")),
        client_secret=str(os.getenv("CLIENT_SECRET")),
        user_agent=str(os.getenv("USER_AGENT"))
    )

    subreddit = reddit.subreddit("all")
    print("Starting consumption")
    for submission in subreddit.stream.submissions():
        submission.comments.replace_more(limit=None)
        sub = Post.Post.createFromPost(submission)
        producer.produce(topic="dirty_posts", key=sub.subredditName, value=sub.getJSON())

        for comment in submission.comments.list():
            c = Comment.Comment.createFromComment(comment, sub.id)
            producer.produce("dirty_comments", key=c.postID, value=c.getJSON())
