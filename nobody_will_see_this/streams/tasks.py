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
                # print('Run #: ' + str(run_num))
                process_comment(comments, conn)


def process_comment(comments, conn):
    ''' Processes each comment, looking for fuzzy matches in the comment body. '''
    comments_saved = read_comment_ids(conn)

    if comments.id not in comments_saved and not comments.author == 'i_saw_your_post':
        for sentence in regex.split(r'(?<=[.?!;])\s+(?=\p{Lu})', comments.body.lower()):
            # Performs matching within the comment body text
            pat = regex.compile(r'one will see |one will ever see |body will see |body will ever see ')
            pos = 0
            m = pat.search(sentence, pos)

            if m:
                print('Comment identified. comment_if: ' + comments.id)

                global comment_count
                comment_count = comment_count + 1

                with conn:
                    new_comment = (
                    float(comments.created), str(comments.id), str(comments.link_id), str(comments.author),
                    str(remove_non_ascii(comments.body)), str(comments.permalink), str(comments.subreddit))
                    new_comment_id = add_comment(conn, new_comment)
                    conn.commit()


def remove_non_ascii(text):
    return regex.sub(r'[^\x20-\x7E]',' ', text)


def add_comment(conn, comment):
    ''' '''
    sql = ''' INSERT INTO comments(created, comment_id, submission_id, author, comment_body, permalink, subreddit)
              VALUES(?, ?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, comment)
    return cur.lastrowid


def read_comment_ids(conn):
    ''' Reads list of comment IDs from the database '''
    cur = conn.cursor()
    cur.execute("SELECT comment_id FROM comments")

    rows = cur.fetchall()

    return rows


