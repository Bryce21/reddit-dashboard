import praw
from classes import Post, Comment
from confluent_kafka import Producer
import socket
import atexit
from confluent_kafka import Producer
import socket
import asyncio
import json

from threading import Timer


class Repeat(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

conf = {'bootstrap.servers': "localhost:29092",
        'client.id': socket.gethostname(),
        }


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))


def delivery_callback(err, msg):
    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
    else:
        print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
            topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))




producer = Producer(conf)


class Healthcheck():
    def __init__(self, producerID, postCount, commentCount):
        self.producerID = producerID
        self.postCount = postCount
        self.commentCount = commentCount

    def getJSON(self):
        return json.dumps(vars(self))


def healthcheck():
    producer.produce("healthcheck", value=Healthcheck(
        "prawProducer",
        str(Post.Post.postCounter),
        str(Comment.Comment.commentCounter)
    ).getJSON())
    producer.poll(1000)


healthCheck = Repeat(30.0, healthcheck)
healthCheck.start()

reddit = praw.Reddit(
    client_id="1lb14v6vpEASB83rdUeAGg",
    client_secret="XFJourPG18yjLhwxMTeUnfMgWCYQFA",
    user_agent="praw_reddit_producer"
)


def closeProducer():
    print("Forcing producer flush on shutdown: ")
    producer.flush()


if __name__ == '__main__':
    atexit.register(closeProducer)



    subreddit = reddit.subreddit("all")
    for submission in subreddit.stream.submissions():
        submission.comments.replace_more(limit=None)
        sub = Post.Post.createFromPost(submission)
        producer.produce("dirty_posts", key=sub.subredditName, value=sub.getJSON(), callback=delivery_callback)

        #print(sub.getJSON())
        for comment in submission.comments.list():
            c = Comment.Comment.createFromComment(comment, sub.id)
            #print(c.getJSON())
            producer.produce("dirty_comments", key=c.postID, value=c.getJSON(), callback=delivery_callback)
            # print("Post id: " + sub.id + ", Author: " + c.author + ", Parent id: " + c.parent_id, "Subreddit: " + c.subredditName)




        # print("Have made: " + str(Comment.Comment.getCount()) + " comments")
        # print("Have made: " + str(Post.Post.getCount()) + " posts")





