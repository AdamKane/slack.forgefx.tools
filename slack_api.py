import os
from dotenv import load_dotenv
from fastapi import FastAPI
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

app = FastAPI()

token = os.getenv("SLACK_BOT_USER_OAUTH_TOKEN")
slack_api = WebClient(token=token)





@app.get("/")
async def root():
    return {"message": "Hello World?"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/team-name")
async def get_team_name():
    try:
        response = slack_api.team_info()
        team_name = response["team"]["name"]
        return team_name
        return {"team_name": team_name}
    except Exception as e:
        return {"error": str(e)}


