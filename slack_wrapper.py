import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import List


class SlackWrapper:

    def __init__(self):
        load_dotenv()
        token = os.getenv("SLACK_BOT_USER_OAUTH_TOKEN")
        self.client = WebClient(token=token)

    def get_all_channels(self):
        all_channels = []
        cursor = None
        while True:
            response = self.client.conversations_list(cursor=cursor)
            all_channels.extend(response['channels'])
            cursor = response.get('response_metadata', {}).get('next_cursor')
            if not cursor:
                break
        return all_channels

    def get_channel_bookmarks(self, channel_id: str):
        try:
            response = self.client.bookmarks_list(channel_id=channel_id)
            return response.get("bookmarks", [])
        except SlackApiError:
            # Skip channels where we don't have permission to list bookmarks
            return []

    def find_matching_bookmarks(self, bookmarks: List[dict], url: str, channel_id: str):
        return [
            {**bookmark, 'channel_id': channel_id}
            for bookmark in bookmarks
            if bookmark.get("link") == url
        ]

    def find_bookmarks_by_url(self, url: str):
        try:
            all_bookmarks = []
            channels = self.get_all_channels()
            
            for channel in channels:
                channel_id = channel['id']
                channel_bookmarks = self.get_channel_bookmarks(channel_id)
                matching_bookmarks = self.find_matching_bookmarks(channel_bookmarks, url, channel_id)
                all_bookmarks.extend(matching_bookmarks)
            
            return all_bookmarks
        except SlackApiError as e:
            raise HTTPException(status_code=400, detail=f"Error listing bookmarks: {str(e)}")

    def delete_bookmarks(self, channel_id: str, bookmark_ids: List[str]):
        results = []
        for bookmark_id in bookmark_ids:
            try:
                self.client.bookmarks_remove(channel_id=channel_id, bookmark_id=bookmark_id)
                results.append({"bookmark_id": bookmark_id, "status": "deleted"})
            except SlackApiError as e:
                results.append({"bookmark_id": bookmark_id, "status": "error", "message": str(e)})
        return results




# If we run this file by itself, create a new instance of SlackWrapper
if __name__ == "__main__":
    slack = SlackWrapper()
    
