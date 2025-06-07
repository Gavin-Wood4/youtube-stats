from googleapiclient.discovery import build
import os
import argparse
import sys

def get_subscriber_count(api_key, channel_id):
    try:
        youtube = build('youtube', 'v3', developerKey = api_key)
        request = youtube.channels().list(part='statistics', id=channel_id)
        response = request.execute()    # Requests statistics for specified YouTube channel ID.

        if 'items' in response:
            statistics = response['items'][0]['statistics']     # Parses for items within requested statistics.
            if 'subscriberCount' in statistics:
                subscriber_count = statistics['subscriberCount']
                print(f"Subscriber count for Channel ID {channel_id} is {subscriber_count}")
            else:
                print(f"Subscriber count is hidden for channel ID {channel_id}")
        else:
            print(f"Could not find channel with ID {channel_id}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        print("Error: YOUTUBE_API_KEY environment variable is missing.")
        sysexit(1)

    parser = argparse.ArgumentParser(description="Collect the subscriber count for a YouTube channel.")
    parser.add_argument("channel_id", help="The ID of the YouTube channel to check.")
    args = parser.parse_args()

    get_subscriber_count(api_key, args.channel_id)
