from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import argparse
import sys

def get_channel_stats(api_key: str, channel_id: str):
    try:
        youtube = build('youtube', 'v3', developerKey = api_key)

        request = youtube.channels().list(part='statistics', id=channel_id)

        response = request.execute()    # Requests statistics for specified YouTube channel ID.
        if not response.get('items'):
            print(f"Error: Could not not find a channel with ID {channel_id}")
            return

        stats = response['items'][0].get('statistics')  # stats contains the channel data.
        if not stats:
            print(f"Error: Statistics are not available for channel ID {channel_id}")
            return

        print(f"Statistics for Channel ID {channel_id}\n")

        metrics = {     # Pairs API item name with command line output.
            'viewCount': 'Total View Count',
            'subscriberCount': 'Subscriber Count',
            'videoCount': 'Total Video Count'
        }

        for key, title, in metrics.items():
            if key in stats:
                stat_value = int(stats[key])
                print(f"{title:<25}: {stat_value:,}") # Formatting >1000 with commas for readibility.

        if stats.get('hiddenSubscriberCount', False):
            printf(f"{'Subscriber Count':<25}: Hidden")

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        print("Error: YOUTUBE_API_KEY environment variable is missing.")
        sysexit(1)

    parser = argparse.ArgumentParser(description="Collect the subscriber count for a YouTube channel.")
    parser.add_argument("channel_id", help="The ID of the YouTube channel to check.")
    args = parser.parse_args()

    get_channel_stats(api_key, args.channel_id)

if __name__ == '__main__':
    main()

