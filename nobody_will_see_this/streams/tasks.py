from __future__ import absolute_import
from django.conf import settings
from celery import shared_task
from .models import Comment

import praw
import regex as regex
import time
import os
import sys


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def begin_process(is_true=True):
    while is_true:
        reddit = praw.Reddit(username=settings.PRAW_USERNAME,
                             password=settings.PRAW_PASSWORD,
                             client_id=settings.PRAW_CLIENT_ID,
                             client_secret=settings.PRAW_CLIENT_SECRET,
                             user_agent=settings.PRAW_USER_AGENT)

        subreddit = reddit.subreddit('all')

        run_num = 0

        while True:
            for comments in subreddit.stream.comments():
                run_num = run_num + 1
                if run_num % 1000 == 0:
                    print('Still running (currently on run ' + str(run_num) + ')')
                    print('Most recent comment: ' + comments.name + ': ' + comments.body)
                # print('Run #: ' + str(run_num))
                process_comment(comments)


def process_comment(comments):
    ''' Processes each comment, looking for fuzzy matches in the comment body. '''

    if not Comment.objects.filter(name=comments.name).exists() and not comments.author == settings.PRAW_USERNAME:

        for sentence in regex.split(r'(?<=[.?!;])\s+(?=\p{Lu})', comments.body.lower()):
            # Performs matching within the comment body text
            pat = regex.compile(r'one will see |one will ever see |body will see |body will ever see ')
            pos = 0
            m = pat.search(sentence, pos)

            if m:
                print('Comment identified. comment_id: ' + comments.id)

                Comment.objects.create(subreddit_id=comments.subreddit_id,
                    subreddit=comments.subreddit,
                    link_id=comments.link_id,
                    parent_id=comments.parent_id,
                    name=comments.name,
                    author=comments.author,
                    body=comments.body,
                    score=comments.score,
                    downs=comments.downs,
                    edited=comments.edited,
                    permalink=comments.permalink,
                    created_utc=comments.created_utc,)


def remove_non_ascii(text):
    return regex.sub(r'[^\x20-\x7E]', ' ', text)


