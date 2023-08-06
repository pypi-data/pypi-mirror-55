import json
from pathlib import Path
from ge_sm.common.secrets import *


pathname = Path(os.path.join(os.path.abspath('')))

channelsdict = {
	os.environ.get('YT_CHANNEL', ''): {
		'name': 'Chajaa',
		'analyticsdat': 'analytics_CJ.dat',
		'playlist': os.environ.get('YT_PLAYLIST', ''),
		'youtubedat':  'youtube_CJdat.dat'
	}
}

#Metric details
std_metric_details = {'Views': ['views','1a','Metric'],
'Watch time':['watchtime',1,None], ## views * avg view time
'Avg view duration':['averageViewDuration',1,'Metric'],
'Avg view percentage':['averageViewPercentage',2,'Metric'],
'Comments':['comments',3,'Metric'],
'Likes':['likes',4,'Metric'],
'Dislikes':['dislikes',5,'Metric'],
'Shares':['shares',6,'Metric'],
'Subscribers':['subscribers',7, None], ## subs gained - subs lost
'Subscribers gained':['subscribersGained',7,'Metric'], 
'Subscribers lost':['subscribersLost',8,'Metric'], 
'Annotation Clicks':['annotationClicks',9,'Metric'], 
'Annotation clickable impressions':['annotationClickableImpressions',10,'Metric'],
'Annotation click through rate':['annotationClickThroughRate',11,'Metric']}

vid_details = [('ChName','Channel name'), ('ChId', 'Channel ID'), ('video', 'Video Id'), 
('videoname','Video name'), ('videourl', 'URL'), ('videopub','Date published'), ('estimatedMinutesWatched', 'Est Minutes Watched')]


secrets = {
	"installed": {
		"client_id": os.environ.get('YT_CLIENT_ID', ''),
		"project_id": os.environ.get('YT_PROJECT_ID', ''),
		"auth_uri": "https://accounts.google.com/o/oauth2/auth",
		"token_uri": "https://oauth2.googleapis.com/token",
		"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
		"client_secret": os.environ.get('YT_CLIENT_SECRET', ''),
		"redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
	}
}

yt = {
	"access_token": os.environ.get('YOUTUBE_ACCESS_TOKEN', ''),
	"client_id": os.environ.get('YOUTUBE_CLIENT_ID', ''),
	"client_secret": os.environ.get('YOUTUBE_CLIENT_SECRET', ''),
	"refresh_token": os.environ.get('YOUTUBE_REFRESH_TOKEN', ''),
	"token_expiry": os.environ.get('YOUTUBE_TOKEN_EXPIRY', ''),
	"token_uri": "https://oauth2.googleapis.com/token",
	"user_agent": None,
	"revoke_uri": "https://oauth2.googleapis.com/revoke",
	"id_token": None,
	"id_token_jwt": None,
	"token_response": {
		"access_token": os.environ.get('YOUTUBE_TOKEN_RESPONSE_ACCESS_TOKEN', ''),
		"expires_in": 3600,
		"scope": "https://www.googleapis.com/auth/yt-analytics.readonly https://www.googleapis.com/auth/youtube.readonly",
		"token_type": "Bearer"
	},
	"scopes": ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/yt-analytics.readonly"],
	"token_info_uri": "https://oauth2.googleapis.com/tokeninfo",
	"invalid": False,
	"_class": "OAuth2Credentials",
	"_module": "oauth2client.client"
}

yt_analytics = {
	"access_token": os.environ.get('YT_ANALYTICS_ACCESS_TOKEN'),
	"client_id": os.environ.get('YT_ANALYTICS_CLIENT_ID'),
	"client_secret": os.environ.get('YT_ANALYTICS_CLIENT_SECRET'),
	"refresh_token": os.environ.get('YT_ANALYTICS_REFRESH_TOKEN'),
	"token_expiry": os.environ.get('YT_ANALYTICS_TOKEN_EXPIRY'),
	"token_uri": "https://oauth2.googleapis.com/token",
	"user_agent": None,
	"revoke_uri": "https://oauth2.googleapis.com/revoke",
	"id_token": None,
	"id_token_jwt": None,
	"token_response": {
		"access_token": os.environ.get('YT_ANALYTICS_RESPONSE_ACCESS_TOKEN'),
		"expires_in": 3600,
		"refresh_token": os.environ.get('YT_ANALYTICS_RESPONSE_REFRESH_TOKEN'),
		"scope": "https://www.googleapis.com/auth/yt-analytics.readonly",
		"token_type": "Bearer"
	},
	"scopes": ["https://www.googleapis.com/auth/yt-analytics.readonly"],
	"token_info_uri": "https://oauth2.googleapis.com/tokeninfo",
	"invalid": False,
	"_class": "OAuth2Credentials",
	"_module": "oauth2client.client"
}

with open(pathname / 'youtube_secrets_details.json', 'w') as f:
	f.write(json.dumps(secrets))
	f.close()

with open(pathname / 'youtube_CJdat.dat', 'w') as f:
	f.write(json.dumps(yt))
	f.close()

with open(pathname / 'YTanalytics.dat', 'w') as f:
	f.write(json.dumps(yt_analytics))
	f.close()
