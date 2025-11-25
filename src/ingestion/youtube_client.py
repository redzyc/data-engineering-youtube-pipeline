import os
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv


load_dotenv()

class YouTubeClient:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY not found in environment variables.")
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    def search_videos(self, query, max_results=5):
        try:
            request = self.youtube.search().list(
                q=query,
                part='snippet',
                type='video',
                maxResults=max_results
            )
            response = request.execute()
            return response.get('items', [])
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return []
    def get_video_details(self, video_id):
        if not video_id:
            return [] 
        try:
            request = self.youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=','.join([video_id])
            )
            response = request.execute()
            return response.get('items', [])
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return []
        
if __name__ == "__main__":
    try:
        client = YouTubeClient()
        ids = client.search_videos("Data Engineering", max_results=3)

        if ids:
            details = client.get_video_details(ids[0]['id']['videoId'])
            os.makedirs('data/raw', exist_ok=True)
            with open(f'data/raw/youtube_sample.json', 'w', encoding='utf-8') as f:
                json.dump(details, f, indent=4, ensure_ascii=False)
    except ValueError as ve:
        print(ve)