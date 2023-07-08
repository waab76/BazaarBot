#!/usr/bin/env python3
# coding: utf-8
#
#   File = karma_calculator.py
#
#      Copyright 2023 Rob Curtis
#
############################################################################

import logging
import time

# id for r/WetShaving is 2rb88
# id for r/Shave_Bazaar is 2srzg
# id for r/Wicked_Edge is 2s46m
sub_ids = ['2rb88', '2srzg', '2s46m']

karma_template = '''
Shaving subreddit overview for /u/{} for the last 90 days:

* {} Submissions
* {} Comments
* {} Karma
'''

def calculate_karma(user):
    logging.info('Calculating karma for user %s', user.name)
    karma = 0
    num_submissions = 0
    num_comments = 0
    ninety_days_ago = time.time() - 90 * 86400

    try:
        # Calculate the karma of all submissions.
        for submission in user.submissions.new(limit=1000):
            try:
                if submission.created_utc < ninety_days_ago:
                    continue
                elif submission.subreddit_id[3:] in sub_ids:
                    num_submissions += 1
                    karma += submission.score
            except:
                logging.exception('Failed to get karma for submision: [%s]', submission.id)
                continue

        # Calculate the karma of all comments.
        for comment in user.comments.new(limit=1000):
            try:
                if comment.created_utc < ninety_days_ago:
                    continue
                elif comment.subreddit_id[3:] in sub_ids:
                    num_comments += 1
                    karma += comment.score
            except:
                logging.exception('Failed to get karma for comment: [%s]', comment.id)
                continue
    except:
        logging.exception('Failed to get karma for user %s', user.name)

    logging.info('User %s has %s karma', user.name, karma)

    return karma, num_submissions, num_comments

def formatted_karma(user):
    activity = calculate_karma(user)
    response = karma_template.format(user.name, activity[1], activity[2], activity[0])

    return response
