import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

class SlackAPI:
    
    def __init__(self):
        self.token = os.getenv("SLACK_BOT_USER_OAUTH_TOKEN")
        self.client = WebClient(token=self.token)

    def get_team_name(self):
        response = self.client.team_info()
        team_name = response["team"]["name"]
        return team_name

