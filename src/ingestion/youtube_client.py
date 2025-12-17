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
    def get_video_details(self, video_ids):
        if not video_ids:
            return [] 
        try:
            request = self.youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=','.join(video_ids)
            )
            response = request.execute()
            return response.get('items', [])
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return []
        
if __name__ == "__main__":
        try:
            client = YouTubeClient()
            search_items = ["Data Engineering", "Machine Learning", "Artificial Intelligence", "Big Data", "Cloud Computing", "Data Science", "Deep Learning", "Neural Networks", "Python Programming", "Statistics"]

            all_videos = []
            for item in search_items:
                ids = client.search_videos(item, max_results=5)
                if ids:
                    video_ids = [
                        video["id"].get("videoId")
                        for video in ids
                        if 'videoId' in video['id']
                    ]
                    details = client.get_video_details(video_ids)
                    all_videos.extend(details)
            if all_videos:
                timestamp = int(__import__('time').time())
                filename = f'youtube_videos_{timestamp}.json'

                base_path = '/opt/airflow/data/ingestion'
                output_path = os.path.join(base_path, filename)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'w') as f:
                    json.dump(all_videos, f, indent=4)
                try:
                    os.chmod(output_path, 0o666)
                except Exception as e:
                    print(f"Warning: Could not change permissions: {e}")

                print(f"Video details saved to {output_path}")
            else:
                print("No video details found.")
        except Exception as e:
            print(f"An error occurred during ingestion: {e}")
            exit(1)