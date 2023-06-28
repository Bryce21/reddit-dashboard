import json
from datetime import datetime, timezone

from .CommonRedditProperties import CommonRedditProperties


class Post(CommonRedditProperties):
    postCounter = 0

    @staticmethod
    def getCount():
        return Post.postCounter

    @staticmethod
    def createFromPost(post):

        fullName = "xNAx"
        name = "xNAx"
        try:
            fullName = post.author_fullname
            name = post.author.name
        except AttributeError:
            print("Comment with id: " + post.id + "has no author_fullname property")

        return Post(
            post.id,
            post.title,
            post.selftext,
            post.url,
            name,
            post.created_utc,
            post.over_18,
            post.score,
            post.total_awards_received,
            post.upvote_ratio,
            post.stickied,
            post.archived,
            post.pinned,
            post.is_video,
            post.ups,
            post.downs,
            fullName,
            post.subreddit.display_name
        )


    def getJSON(self):
        return json.dumps(vars(self))

    def __init__(self,
                 id,
                 title,
                 body,
                 url,
                 user,
                 created_utc,
                 over_18,
                 score,
                 total_awards,
                 upvote_ratio,
                 stickied,
                 archived,
                 pinned,
                 is_video,
                 ups,
                 downs,
                 authorID,
                 subredditName
                 ):
        super().__init__(id, ups, downs, authorID, created_utc, score, archived, subredditName)
        self.id = id
        self.title = title
        self.body = body
        self.url = url
        self.user = user
        self.created_utc = str(created_utc)
        self.over_18 = over_18
        self.score = score
        self.total_awards = total_awards
        self.upvote_ratio = upvote_ratio
        self.stickied = stickied
        self.archived = archived
        self.pinned = pinned
        self.is_video = is_video
        self.ups = ups
        self.downs = downs
        self.authName = authorID
        self.subredditName = subredditName

        self.receivedFromReddit = str(datetime.now(timezone.utc))

        Post.postCounter += 1
