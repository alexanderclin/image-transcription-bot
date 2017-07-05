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
		process_submission(r, submission)

def process_submission(r, submission):
	print()
	print("Found submission: {}".format(submission.title))
	print("  Submission url: {}".format(submission.url))

	try:
		imgt = ImageTranscriber(submission.url)
		usernames = [comment.author for comment in submission.comments.list()]

		# Don't reply if already replied
		if r.user.me() in usernames:
			print("  Already commented, skipping".format(config.username))
			return

		# Only reply if text found
		if imgt.text and imgt.text.strip():
			print(imgt.text)
			reply_comment = reply_with_text(imgt.text)
			submission.reply(reply_comment)
	except:
		print("  Could not transcribe, skipping")

def reply_with_text(text):
	quoted_text = text.replace("\n", "\n\n>")
	reply_text = "Attempted transcription:\n>{}".format(quoted_text)
	reply_text += "    \n    \n*****\n" + "I am a bot!"
	return reply_text

def main():
	r = bot_login()
	run_bot(r)

if __name__ == '__main__':
	main()
