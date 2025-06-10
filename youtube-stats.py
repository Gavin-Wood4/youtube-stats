from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import os
import argparse
import sys

@dataclass(slots=True)
class ChannelStats:
    id:             str
    name:           str
    publish_date:   datetime
    view_count:     int
    sub_count:      Optional[int]   # Subcount may be hidden -> None
    video_count:    int


def get_channel_stats(youtube, channel_id: str) -> ChannelStats:
    try:
        channels = youtube.channels()

        request = channels.list(part='snippet,statistics', id=channel_id)
        response = request.execute()    # Requests statistics for specified YouTube channel ID.
        if not response.get('items'):
            print(f"Error: Could not not find a channel with ID {channel_id}")
            raise ValueError(f"There is no channel with the ID {channel_id}")
            
        item = response["items"][0]
        snippet = item["snippet"]
        stats = item["statistics"]
        
        return ChannelStats(
            id              = channel_id,
            name            = snippet["title"],
            publish_date    = datetime.fromisoformat(snippet["publishedAt"]),
            view_count      = int(stats["viewCount"]),
            sub_count       = None if stats.get("hiddenSubscriberCount") else
                              int(stats["subscriberCount"]),
            video_count     = int(stats["videoCount"])
        )

    except HttpError as e:
        raise RuntimeError(f"A HTTP error {e.resp.status} ocurred: {e.content}") from e

def print_channel_stats(cs: ChannelStats) -> None:
    print("-" * 50)
    print(f"Statistics for {cs.name} ({cs.id})")
    print("-" * 50)
    print(f"{'Channel Publish Date':<25}: {cs.publish_date.date()}")
    print(f"{'Total View Count':<25}: {cs.view_count:,}")
    if cs.sub_count is None:
        print(f"{'Subscriber count':<25}: Hidden")
    else:
        print(f"{'Subscriber count':<25}: {cs.sub_count:,}")
    print(f"{'Total Video Count':<25}: {cs.video_count:,}")
    print("-" * 50)

def build_youtube_client():
    API_KEY = os.getenv("YOUTUBE_API_KEY")
    if not API_KEY:
        sys.exit("YOUTUBE_API_KEY environment variable is missing.")
    return build('youtube', 'v3', developerKey = API_KEY)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect the subscriber count for a YouTube channel.")
    parser.add_argument("channel_id", help="The ID of the YouTube channel to check.")
    return parser.parse_args()


def main(): 
    args = parse_args()
    youtube = build_youtube_client()
    stats = get_channel_stats(youtube, args.channel_id)
    print_channel_stats(stats)

if __name__ == '__main__':
    main()

