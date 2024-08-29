from slack_wrapper import SlackWrapper

def test_get_all_channels():
    slack_wrapper = SlackWrapper()
    channels = slack_wrapper.get_all_channels()
    assert channels is not None
