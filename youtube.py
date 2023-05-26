import requests
import pandas as pd
from datetime import datetime, timedelta, timezone

class YouTube:
    '''
    Description
    '''
    def __init__(self, api_key):
        '''
        Description
        '''
        self.api_key = api_key

    def http_query(self, url):
        '''
        Run HTTP query given a certain url. Trys three times before failing.

        :param url: URL to query
        :type url: string

        :returns: JSON response as a dict 
        :rtype: dict
        '''
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
          try:
            response = requests.get(url)
            response.raise_for_status()
            json_data = response.json()
            return json_data
          except requests.RequestException as e:
            retry_count += 1
            print(f"Request failed: {e}. Retrying ({retry_count}/{max_retries})")
        
        print(f"Request Failed: {url}")
        return None

    def get_keyword_data(self, keyword, date, n = 100):
        '''
        Description

        :param x:
        :type x:

        :returns:
        :rtype:
        '''
        return
    
    def clean_metadata(self, input_json):
        output_json = {
            "kind": input_json["id"]["kind"],
            "videoId": input_json["id"]["videoId"],
            "publishedAt": input_json["snippet"]["publishedAt"],
            "channelId": input_json["snippet"]["channelId"],
            "title": input_json["snippet"]["title"],
            "description": input_json["snippet"]["description"],
            "thumbnail": input_json["snippet"]["thumbnails"]["default"]["url"],
            "channelTitle": input_json["snippet"]["channelTitle"],
            "liveBroadcastContent": input_json["snippet"]["liveBroadcastContent"],
            "publishTime": input_json["snippet"]["publishTime"],
        }
        return output_json
    

    def clean_comments(self, input_json):
        output_json = {
            "kind": input_json["kind"],
            "etag": input_json["etag"],
            "id": input_json["id"],
            "videoId": input_json["snippet"]["videoId"],
            "textDisplay": input_json["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
            "textOriginal": input_json["snippet"]["topLevelComment"]["snippet"]["textOriginal"],
            "authorDisplayName": input_json["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
            "authorProfileImageUrl": input_json["snippet"]["topLevelComment"]["snippet"]["authorProfileImageUrl"],
            "authorChannelUrl": input_json["snippet"]["topLevelComment"]["snippet"]["authorChannelUrl"],
            "authorChannelId": input_json["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"],
            "canRate": input_json["snippet"]["topLevelComment"]["snippet"]["canRate"],
            "viewerRating": input_json["snippet"]["topLevelComment"]["snippet"]["viewerRating"],
            "likeCount": input_json["snippet"]["topLevelComment"]["snippet"]["likeCount"],
            "publishedAt": input_json["snippet"]["topLevelComment"]["snippet"]["publishedAt"],
            "updatedAt": input_json["snippet"]["topLevelComment"]["snippet"]["updatedAt"],
            "canReply": input_json["snippet"]["canReply"],
            "totalReplyCount": input_json["snippet"]["totalReplyCount"],
            "isPublic": input_json["snippet"]["isPublic"]
        }
        return output_json
        

    def get_videos(self, keyword, date=datetime(2021, 1, 7, tzinfo=timezone.utc), n = 100):
        '''
        Description

        :param keyword: The keyword to search
        :type keyword: string
        :param date: The date in which to search (default 1/7/2021)
        :type keyword: datetime
        :param n: Number of videos to get (default 100)
        :type keyword: int

        :returns: Pandas DataFrame of video Metadata
        :rtype: DataFrame
        '''
        date_start = date.replace(hour=0, minute=0, second=0)
        date_start = date_start.isoformat().replace("+00:00", "Z")
        date_end = date.replace(hour=0, minute=0, second=0) + timedelta(days=1)
        date_end = date_end.isoformat().replace("+00:00", "Z")
        base_url = f"https://www.googleapis.com/youtube/v3/search"
        params = f"?key={self.api_key}&q={keyword}&publishedAfter={date_start}&publishedBefore={date_end}&type=video&maxResults={n}&part=snippet"
        full_url = base_url + params
        
        video_list = []
        data = self.http_query(full_url)
        video_list.extend(data["items"])
        
        formatted_list = list(map(self.clean_metadata, video_list))

        return pd.DataFrame(formatted_list)
    
    def get_comments(self, video_ids, max = 500):
        '''
        Description

        :param video_ids: A list video IDs to get comments for
        :type video_ids: list
        :param max: Maximum comments to get per video (default 500)
        :type max: int

        :returns:
        :rtype:
        '''
        base_url = f"https://www.googleapis.com/youtube/v3/commentThreads"

        comment_data = []
        for video_id in video_ids:
          params = f"?key={self.api_key}&part=snippet&maxResults={max}&videoId={video_id}&maxResults={max}"
          this_url = base_url + params
          data = self.http_query(this_url)
          if data is not None and 'items' in data:
            comment_data.extend(data['items'])
          else:
             print(f"Failed to retrieve comments for: {video_id} — Comments are turned off for the video.")
        
        formatted_list = list(map(self.clean_comments, comment_data))

        return pd.DataFrame(formatted_list)