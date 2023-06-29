from collections import Callable
from threading import Timer
import json
from typing import Any

from classes import Post, Comment


class HealthcheckValue():
    def __init__(self, producerID, postCount, commentCount):
        self.producerID = producerID
        self.postCount = postCount
        self.commentCount = commentCount

    def getJSON(self):
        return json.dumps(vars(self))


class HealthCheck(Timer):
    def __init__(self, producer_wrapper, interval):
        super().__init__(interval, self.healthcheck)
        self.producer = producer_wrapper
        self.interval = interval

    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

    def healthcheck(self):
        self.producer.produce("healthcheck", value=HealthcheckValue(
            "prawProducer",
            str(Post.Post.postCounter),
            str(Comment.Comment.commentCounter)
        ).getJSON())
        self.producer.poll(1000)
