"""Twitter Mentions"""
import requests

from django.conf import settings
from django.utils.translation import gettext as _

class TwitterMentions(object):
    def __init__(self, account_name):
        self.account_name = account_name
        self.request_message = None
        self.mentions = None
        self.url = "https://api.twitter.com/1.1/tweets/search/30day/production.json"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + settings.TWITTER_AUTH
        }

    def get_tweets(self):
        """Make HTTPS requests to Twitter API to retrieve mentions from a certain user

        If request is successful, payload is saved into self.mentions
        
        Returns TRUE if request is successful and there is tweets returned, False otherwise
        """
        payload = {
            "query": "from:" + self.account_name
        }
        twitter_request = requests.post(self.url, json=payload, headers=self.headers)
        if twitter_request.status_code != 200:
            self.request_message = _("There was a problem while accessing the API")
            return False
        data = twitter_request.json()
        if not data:
            self.request_message = _("There was a problem while accessing the API")
            return False
        self.request_message = _("Success")
        self.mentions = data["results"]
        return True
        