import pytest
from slack_api import SlackAPI
from slack_sdk.errors import SlackApiError

def test_get_team_name():
    api = SlackAPI()
    name = api.get_team_name()
    assert name == "forgefx"


