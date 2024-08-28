from fastapi import FastAPI
from slack_api import SlackAPI

app = FastAPI()
slack_api = SlackAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/team-name")
async def get_team_name():
    try:
        team_name = slack_api.get_team_name()
        return {"team_name": team_name}
    except Exception as e:
        return {"error": str(e)}

