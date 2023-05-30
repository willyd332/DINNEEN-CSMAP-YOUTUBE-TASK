import requests
import re
import pandas as pd
from datetime import datetime, timedelta, timezone

class YouTube:
    '''
    A class to query the Youtube API to get videos and their related comments
    '''
    def __init__(self, api_key, log_file_name=None):
        '''
        Init the class with your Google Cloud API key
        See https://cloud.google.com/apis for more information
        '''
        if log_file_name is None:
            today = datetime.now().strftime("%Y-%m-%d")
            log_file_name = f"./logs/log_{today}"
        self.api_key = api_key
        self.log_file_name = log_file_name

    def log(self, message):
        log_time = datetime.now()
        # Hide API Key
        pattern = r'(?<=[\?|&]key=)[^&]*'
        message = re.sub(pattern, '[API-KEY-HIDDEN]', message)
        with open(self.log_file_name + '.txt', 'a') as f:
           f.write(f"{log_time} - Message: {message}\n")
        return True

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
            self.log(f"Successfully queried: {url}")
            return json_data
          except requests.RequestException as e:
            retry_count += 1
            print(f"Request failed: {e}. Retrying ({retry_count}/{max_retries})")
            self.log(f"Request failed: {e}. Retrying ({retry_count}/{max_retries})")
        
        print(f"Request Failed: {url}")
        self.log(f"Request Failed: {url}")
        return None

    def clean_metadata(self, input_json):
        '''
        Cleans JSON data for use in a flat CSV file

        :param input_json: A JSON dict from from the YouTube Search API
        :type input_json: dict

        :returns: A flattened dict of the relevant data
        :rtype: dict
        '''
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
        '''
        Cleans JSON data for use in a flat CSV file

        :param input_json: A JSON dict from from the YouTube CommentThreads API
        :type input_json: dict

        :returns: A flattened dict of the relevant data
        :rtype: dict
        '''
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
        

    def get_videos(self, keyword, date=datetime(2021, 1, 7, tzinfo=timezone.utc), timeframe=0, n = 100):
        '''
        Gets videos from Youtube Search API based on a keyword and returns a DataFrame of relevant data

        :param keyword: The keyword to search
        :type keyword: string
        :param date: The start date in which to search (default 1/7/2021)
        :type date: datetime
        :param timeframe: The number of days after the date to include (default 0, i.e. only a single day)
        :type timeframe: int
        :param n: Number of videos to get (default 100)
        :type n: int

        :returns: Pandas DataFrame of video Metadata
        :rtype: DataFrame
        '''
        date_start = date.replace(hour=0, minute=0, second=0)
        date_start = date_start.isoformat().replace("+00:00", "Z")
        date_end = date.replace(hour=23, minute=59, second=59) + timedelta(days=timeframe)
        date_end = date_end.isoformat().replace("+00:00", "Z")
        base_url = f"https://www.googleapis.com/youtube/v3/search"
        
        video_list = []
        page_token = ""
        while True:
            params = f"?key={self.api_key}&q={keyword}&publishedAfter={date_start}&publishedBefore={date_end}&type=video&maxResults={n}&part=snippet{page_token}"
            full_url = base_url + params
            data = self.http_query(full_url)
            video_list.extend(data["items"])
            if len(video_list) >= n or "nextPageToken" not in data:
                break
            else:
                page_token = "&pageToken=" + data["nextPageToken"]

        formatted_list = list(map(self.clean_metadata, video_list))

        return pd.DataFrame(formatted_list)
    
    def get_comments(self, video_ids, max = 500):
        '''
        Gets videos from Youtube CommentThreads API based on a list of videoIds and returns a DataFrame of relevant data

        :param video_ids: A list video IDs to get comments for
        :type video_ids: list
        :param max: Maximum comments to get per video (default 500)
        :type max: int

        :returns: Pandas DataFrame of commment data
        :rtype: DataFrame
        '''
        base_url = f"https://www.googleapis.com/youtube/v3/commentThreads"

        comment_data = []
        for video_id in video_ids:
            this_comment_data = []
            page_token=""
            while True:
                params = f"?key={self.api_key}&part=snippet&maxResults={max}&videoId={video_id}{page_token}"
                this_url = base_url + params
                data = self.http_query(this_url)
                if data is not None and 'items' in data:
                    this_comment_data.extend(data['items'])
                else:
                    print(f"Failed to retrieve comments for: {video_id} — Comments are turned off for the video.")
                    self.log(f"Failed to retrieve comments for: {video_id} — Comments are turned off for the video.")
                    break
                if len(this_comment_data) >= max or "nextPageToken" not in data:
                    break
                else:
                    page_token = "&pageToken=" + data["nextPageToken"]
            comment_data.extend(this_comment_data)
        
        formatted_list = list(map(self.clean_comments, comment_data))

        return pd.DataFrame(formatted_list)