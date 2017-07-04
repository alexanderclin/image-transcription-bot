import praw
import config
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
		print()
		print("Found submission: {}".format(submission.title))
		print("  Submission url: {}".format(submission.url))

		try:
			imgt = ImageTranscriber(submission.url)
			usernames = [comment.author for comment in submission.comments.list()]

			# Don't reply if already replied
			if r.user.me() in usernames:
				print("  Found {} in comments, skipping".format(config.username))
				continue

			# Only reply if text found
			if imgt.text and imgt.text.strip():
				print(imgt.text)
				reply_comment = reply_with_text(imgt.text)
				submission.reply(reply_comment)
		except:
			print("  Could not transcribe")

def reply_with_text(text):
	quoted_text = text.replace("\n", "\n\n>")
	return "Attempted transcription:\n>{}".format(quoted_text)


r = bot_login()
run_bot(r)