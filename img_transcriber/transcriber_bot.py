import praw
import config
from requests import head
from image_transcriber import ImageTranscriber

def bot_login():
	print("Logging in")
	return praw.Reddit(username      = config.username,
					   password      = config.password,
					   client_id 	 = config.client_id,
					   client_secret = config.client_secret,
					   user_agent    = "Image Transcription Bot v0.1")

def run_bot(r):
	subreddit = r.subreddit(config.subreddit_name)

	for submission in subreddit.stream.submissions():

		response = head(submission.url)
		content_type = response.headers.get('content-type')

		# Found an image
		if "image" in str(content_type):
			usernames = [comment.author for comment in submission.comments.list()]
			# Don't reply if already replied
			if r.user.me() in usernames:
				print("Found {} in comments, skipping".format(config.username))
				continue

			print("Found image: {}".format(submission.url))
			
			imgt = ImageTranscriber(submission.url)
			reply_comment = reply_with_text(imgt.text)
			# Don't reply if no text found
			if reply_comment and not reply_comment.isspace():
				print(imgt.text)
				submission.reply(reply_comment)

def reply_with_text(text):
	quoted_text = text.replace("\n", "\n\n>")
	return "Attempted transcription:\n>{}".format(quoted_text)


r = bot_login()
run_bot(r)