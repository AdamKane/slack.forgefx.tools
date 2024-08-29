import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import List
from datetime import datetime, timedelta

class SlackWrapper:

    def __init__(self):
        
        # Load environment variables and initialize Slack client
        load_dotenv()
        token = os.getenv("SLACK_BOT_USER_OAUTH_TOKEN")
        self.client = WebClient(token=token)

    def get_channel(self, channel_id: str):
        
        # Get information about a specific channel
        try:
            response = self.client.conversations_info(channel=channel_id)
            return response.get("channel", {})
        except SlackApiError as e:
            raise HTTPException(status_code=400, detail=f"Error getting channel info: {str(e)}")

    def get_channel_age_in_days(self, channel_id: str):
        
        # Get the age of a channel in days
        channel = self.get_channel(channel_id)
        created = channel.get('created')
        age = (datetime.now() - datetime.fromtimestamp(created)).days
        return age

    def get_all_channels(self):
        
        # Retrieve all (public and private) channels in the Slack workspace
        all_channels = []
        cursor = None

        while True:
            try:
                # Get all public and private channels, 1000 at a time
                response = self.client.conversations_list(
                    types="public_channel,private_channel",
                    limit=1000,
                    cursor=cursor
                )
                all_channels.extend(response['channels'])
                
                # Check if there are more channels to fetch
                cursor = response['response_metadata'].get('next_cursor')
                if not cursor:
                    break
                
            except SlackApiError as e:
                raise HTTPException(status_code=400, detail=f"Error getting channels: {str(e)}")

        
        count = len(all_channels)
        print(f"Total channels: {count}")

        return all_channels

        
    
    def get_all_recently_created_channels(self, days_ago: int = 30):
        
        # Get all channels created on or after a specified number of days ago.
        all_channels = self.get_all_channels()
        recently_created_channels = []
        
        # Walk through all channels and get the age in days
        for channel in all_channels:
            created = channel.get('created')
            age = (datetime.now() - datetime.fromtimestamp(created)).days
            channel['age_in_days'] = age

            # If age <== days_ago, add to list
            if age <= days_ago:
                recently_created_channels.append(channel)
        
        return recently_created_channels


    def get_channel_bookmarks(self, channel_id: str):
        
        # Get all bookmarks for a specific channel
        try:
            response = self.client.bookmarks_list(channel_id=channel_id)
            return response.get("bookmarks", [])
        except SlackApiError:
            
            # Skip channels where we don't have permission to list bookmarks
            return []

    def find_matching_bookmarks(self, bookmarks: List[dict], url: str, channel_id: str):
        
        # Find bookmarks in a channel that match a specific URL
        return [
            {**bookmark, 'channel_id': channel_id}
            for bookmark in bookmarks
            if bookmark.get("link") == url
        ]

    def find_bookmarks_by_url(self, url: str):
        
        # Find all bookmarks across all channels that match a specific URL
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
        
        # Delete multiple bookmarks from a specific channel
        results = []
        for bookmark_id in bookmark_ids:
            try:
                self.client.bookmarks_remove(channel_id=channel_id, bookmark_id=bookmark_id)
                results.append({"bookmark_id": bookmark_id, "status": "deleted"})
            except SlackApiError as e:
                results.append({"bookmark_id": bookmark_id, "status": "error", "message": str(e)})
        return results

    def get_all_channels_with_placeholder_bookmark_link_urls(self):
        # Find all channels with bookmarks that have a placeholder URL (www.google.com)
        channels_with_bookmarks = []
        
        # Retrieve all channels in the Slack workspace
        all_channels = self.get_all_recently_created_channels(days_ago=30)
        channel_count = len(all_channels)
        
        # Iterate through each channel
        for channel in all_channels:
            channel_id = channel['id']
            channel_name = channel.get('name')

            # Print something like: Checking channel 1 of 300: #general
            print(f"Checking channel {all_channels.index(channel) + 1} of {channel_count}: {channel_name}")
            
            # Get all bookmarks for the current channel
            bookmarks = self.get_channel_bookmarks(channel_id)
            
            # Check each bookmark in the channel
            for bookmark in bookmarks:
                # Look for bookmarks with the placeholder URL 'www.google.com'
                link = bookmark.get('link')
                if link and 'google.com' in link:
                    # If found, add channel and bookmark info to the result list
                    channels_with_bookmarks.append({
                        'channel_id': channel_id,
                        'channel_name': channel_name,
                        'bookmark': bookmark
                    })
                    
                    # Print the channel_id, channel_name, bookmark title, and link
                    print(f"Channel ID: {channel_id}, Channel Name: {channel_name}, Bookmark Title: {bookmark.get('title')}, Bookmark Link: {link}")
                    
                    # Exit the loop after finding one matching bookmark
                    # This ensures we only report each channel once
                    break
        
        # Sort the list of channels by channel_name
        channels_with_bookmarks.sort(key=lambda x: x['channel_name'])
        
        # Return the list of channels with placeholder bookmarks
        return channels_with_bookmarks




# If we run this file by itself, create a new instance of SlackWrapper
if __name__ == "__main__":
    slack = SlackWrapper()
    
