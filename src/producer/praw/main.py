import praw
from classes import Post, Comment
from kafka import ProducerWrapper
import HealthCheck
import atexit
import configparser


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read("./src/producer/praw/env.producer")

    producer = ProducerWrapper.ProducerWrapper()
    atexit.register(producer.close_producer)

    health_check = HealthCheck.HealthCheck(producer, float(str(config["PRAW_PRODUCER"]["HEALTHCHECK_INTERVAL"])))
    health_check.start()


    reddit = praw.Reddit(
        client_id=str(config["PRAW_PRODUCER"]["CLIENT_ID"]),
        client_secret=str(config["PRAW_PRODUCER"]["CLIENT_SECRET"]),
        user_agent=str(config["PRAW_PRODUCER"]["USER_AGENT"])
    )

    subreddit = reddit.subreddit("all")
    for submission in subreddit.stream.submissions():
        submission.comments.replace_more(limit=None)
        sub = Post.Post.createFromPost(submission)
        producer.produce(topic="dirty_posts", key=sub.subredditName, value=sub.getJSON())

        for comment in submission.comments.list():
            c = Comment.Comment.createFromComment(comment, sub.id)
            producer.produce("dirty_comments", key=c.postID, value=c.getJSON())
