#!/usr/bin/env python3
# coding: utf-8
#
#	File = karma_calculator.py
#
#	   Copyright 2023 Rob Curtis
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

	activity = activity_summary(user)

	for sub_id in sub_ids:
		try:
			karma += activity[sub_id]['karma']
			num_submissions += activity[sub_id]['post_count']
			num_comments += activity[sub_id]['comment_count']
		except KeyError:
			logging.debug('No activity by user {} in sub_id {}'.format(user.name, sub_id))

	return karma, num_submissions, num_comments

def activity_summary(user):
	logging.info('Building 90-day activity history for user %s', user.name)
	activity = {}

	karma = 0
	num_submissions = 0
	num_comments = 0
	ninety_days_ago = time.time() - 90 * 86400

	try:
		# Calculate the karma of all submissions.
		for submission in user.submissions.new(limit=1000):
			sub_id = submission.subreddit.display_name.lower()
			try:
				if submission.created_utc < ninety_days_ago:
					continue
				elif sub_id in activity:
					activity[sub_id]['post_count'] += 1
					activity[sub_id]['karma'] += submission.score
				else:
					activity[sub_id] = {}
					activity[sub_id]['karma'] = submission.score
					activity[sub_id]['post_count'] = 1
					activity[sub_id]['comment_count'] = 0
			except:
				logging.exception('Failed to get karma for submision: [%s]', submission.id)
				continue

		# Calculate the karma of all comments.
		for comment in user.comments.new(limit=1000):
			sub_id = comment.subreddit.display_name.lower()
			try:
				if comment.created_utc < ninety_days_ago:
					continue
				elif sub_id in activity:
					activity[sub_id]['karma'] += comment.score
					activity[sub_id]['comment_count'] += 1
				else:
					activity[sub_id] = {}
					activity[sub_id]['karma'] = comment.score
					activity[sub_id]['post_count'] = 0
					activity[sub_id]['comment_count'] = 1
			except:
				logging.exception('Failed to get karma for comment: [%s]', comment.id)
				continue
	except:
		logging.exception('Failed to get karma for user %s', user.name)

	return activity

def formatted_karma(user):
	activity = calculate_karma(user)
	response = karma_template.format(user.name, activity[1], activity[2], activity[0])

	return response
