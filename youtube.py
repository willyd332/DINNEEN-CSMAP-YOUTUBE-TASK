import requests
import time
import pandas as pd
import json

# Task is to perform Keyword Search
  # Retrieve 100 Videos' Metadata
    # From January 7th, 2021
  # Extract Comments from videos
  # Provide documentation for the data
    # Overview of the process
    # Description of data format
    # Structure of data fields
    # Any necessary details

class YouTube:
    '''
    Description
    '''
    def __init__(api_key):
        '''
        Description
        '''
        self.api_key = api_key

    def get_keyword_data(self, keyword, date, n = 100):
        '''
        Description

        :param x:
        :type x:

        :returns:
        :rtype:
        '''
        return

    def get_videos(self, keyword, date, n = 100):
        '''
        Description

        Search API URL: https://www.googleapis.com/youtube/v3/search
          q — string (Your request can also use the Boolean NOT (-) and OR (|) operators to exclude videos or to find videos that are associated with one of several search terms.)
          publishedAfter — datetime
          publishedBefore — datetime
          type — string (video)

        Response:  
          {
            "kind": "youtube#searchListResponse",
            "etag": etag,
            "nextPageToken": string,
            "prevPageToken": string,
            "regionCode": string,
            "pageInfo": {
              "totalResults": integer,
              "resultsPerPage": integer
            },
            "items": [
              search Resource
            ]
          }

        :param x:
        :type x:

        :returns:
        :rtype:
        '''
        return
    
    def get_metadata(self, video_id):
        '''
        Description

        :param x:
        :type x:

        :returns:
        :rtype:
        '''
        return
    
    def get_comments(self, video_id, max = 500):
        '''
        Description

        :param x:
        :type x:

        :returns:
        :rtype:
        '''
        return