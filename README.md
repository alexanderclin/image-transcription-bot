# image-transcription-bot

A bot for Reddit that attempts to transcribe image submissions by converting them to text using OCR.

# Installation

First, set up a virtualenv:
```
$ virtualenv -p python3 img_transcriber
```

Then clone the repository:
```
$ git clone https://github.com/alexanderclin/image-transcription-bot.git
```

Install requirements:
```
$ source img_transcriber/bin/activate
$ pip install -r requirements.txt
```

# Usage

Create a file `img_transcriber/config.py` which contains the following, and change variables accordingly:
```python
username      = YOUR_USERNAME
password      = YOUR_PASSWORD
client_id     = YOUR_CLIENT_ID
client_secret = YOUR_CLIENT_SECRET

subreddit_name = YOUR_SUBREDDIT
```
