from django.db import models

# Create your models here.

class Comment(models.Model):
    # Example: https://www.reddit.com/r/AskReddit/comments/8r9uz9.json
    subreddit_id = models.CharField(max_length=10)  # IE: t5_2qh1i
    subreddit = models.CharField(max_length=255)
    link_id = models.CharField(max_length=10)  # IE: t3_8r9uz9
    parent_id = models.CharField(max_length=10)  # IE: t3_8r9uz9
    name = models.CharField(max_length=10, unique=True)  # IE: t1_e0pjo47
    author = models.CharField(max_length=255)
    body = models.CharField(max_length=1000)
    score = models.SmallIntegerField()
    downs = models.SmallIntegerField()
    edited = models.BooleanField()
    permalink = models.CharField(max_length=1000)
    created_utc = models.DateTimeField()

