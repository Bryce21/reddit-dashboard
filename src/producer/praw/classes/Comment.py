from datetime import datetime, timezone
from .CommonRedditProperties import CommonRedditProperties
import json

class Comment(CommonRedditProperties):

    commentCounter = 0

    @staticmethod
    def getCount():
        return Comment.commentCounter

    def getJSON(self):
        return json.dumps(vars(self))

    @staticmethod
    def createFromComment(comment, postID):
        fullName = "xNAx"
        try:
            fullName = comment.author_fullname
        except AttributeError:
            print("Comment with id: " + comment.id + "has no author_fullname property")

        return Comment(
            comment.id,
            comment.body,
            comment.score,
            comment.created_utc,
            comment.ups,
            comment.downs,
            comment.parent_id,
            comment.depth,
            "xNAx" if comment.author is None else comment.author.name,
            comment.archived,
            comment.total_awards_received,
            comment.subreddit_id,
            comment.stickied,
            comment.is_submitter,
            fullName,
            comment.subreddit.display_name,
            postID
        )

    def __init__(self, id, body, score, created_utc, ups, downs, parent_id, depth, author, archived,
                 total_awards_received, subreddit_id, stickied, is_submitter, authorID, subredditName, postID):
        super().__init__(id, ups, downs, author, created_utc, score, archived, subredditName)
        self.id = id
        self.body = body
        self.score = score
        self.created_utc = str(created_utc)
        self.ups = ups
        self.downs = downs
        self.parent_id = parent_id
        self.depth = depth
        self.author = author
        self.archived = archived
        self.total_awards_received = total_awards_received
        self.subreddit_id = subreddit_id
        self.stickied = stickied
        self.is_submitter = is_submitter
        self.authorID = authorID
        self.subredditName = subredditName
        self.postID = postID

        Comment.commentCounter += 1

        self.receivedFromReddit = str(datetime.now(timezone.utc))
