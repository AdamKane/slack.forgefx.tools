import pytest_asyncio
import slack_api
import pytest



# make an async test for say_hello
@pytest.mark.asyncio
async def test_say_hello():
    response = await slack_api.say_hello("foo")
    print(f"response: {response}")
    assert response == {"message": "Hello foo"}

# make an async test for get_team_name
@pytest.mark.asyncio
async def test_get_team_name():
    response = await slack_api.get_team_name()
    print(f"response: {response}")
    assert response == "forgefx"
