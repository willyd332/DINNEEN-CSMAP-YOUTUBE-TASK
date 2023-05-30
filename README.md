# DINNEEN-CSMAP-YOUTUBE-TASK

## Limitations & Next Steps
> Given the time constraints on this project there are features that I would have liked to implement but did not have the time to do. Additionally, there were several bugs that could not be resolved in the allotted time.

**1. Issues with nextPageToken**
  - For some reason, the API was not returning an object that included a "nextPageToken" and so the number of videos returned is limited.
  - There might have been an issue with how I was accessing the API, however, I did not have enough time to resolve this issue, and so my results are limited to the first returned page.
  - Given more time, I would have read the documentation more closely/experimented to resolve this issue.
> After some research, it looks like this is a common problem [For Example](https://issuetracker.google.com/issues/35177262).

**2. Sampling Frame**
  - While the task asked for 100 videos and <500 comments, it did not specify the sampling frame.
  - If this were a real task, I would have made sure to understand how the researcher would like the videos to be sampled.

**3. Save Meta-Data About The Request Itself (e.g. Date Accessed)**
  - Given more time, I would have saved more data about the request itself, not only the results from the api
  - For example, I would store Date Accessed, the search query itself, who ran the query, etc. 

**4. Save in Database, not in CSV file**
  - A CSV output, while very easy to use for any researcher, is not the ideal output for this project
  - If this were to be scaled, I would likely switch to a semi-structured approach, storing the data in something like an S3 bucket
  - This would allow for more robust data collection down-the-road

**5. More video data**
  - Finally, there is plenty of other video data I could have captured given the time.
  - Some examples include:n suggested/related videos, information about the channel, video transcripts, etc.

## Documentation

### Overview
This module queries the [YouTube API](https://developers.google.com/youtube/v3) to gather video metadata and related comments given a keyword. Please see `Demo.ipynb` for an example use-case and the `data` folder for example outputs.

The module was created on May 26, 2023 by Will Dinneen.

#### `YouTube.get_videos()`
`get_videos` takes in a keyword and returns a list of videos from the YouTube Search API. By default, it searches for videos from 01/7/2021, however, this date value can also be specified as an argument.

The output of the function is a Pandas Dataframe which can be converted into a csv file with the following code:
`DataFrame.to_csv('./path/to/file.csv')`

The structure of the DataFrame is as follows (for more info on all values, please visit the [YouTube API Video Documentation](https://developers-dot-devsite-v2-prod.appspot.com/youtube/v3/docs/videos)):
- `kind`
  - Defaults to `youtube#video`
- `videoId`
  - Video Id string (e.g., `C2npCYNnV18`)
- `title`
  - Title of the video
- `description`
  - Description of the video
- `thumbnail`
  - Url to the video thumbnail
- `channelId`
  - Channel Id String for the channel which posted video (e.g., `UCUmEPYxmnyQDeRUcFkslmQw`)
- `channelTitle`
  - Title of the channel
- `liveBroadcastContent`
  - Whether the video is/was a live broadcast ('none' if not)
- `publishTime`
  - The time and date of the video's publication on YouTube

#### `YouTube.get_comments()`
`get_comments` takes in a a list of video Ids (likely from `get_videos`) and returns a list of comments (max defualts to 500) for those videos.

The output of the function is a Pandas Dataframe with all of the comments from all of the videos. This can be joined with the Video Metadata by using the `videoId` column in both datasets.

It can be converted into a csv file with the following code:
`DataFrame.to_csv('./path/to/file.csv')`

The structure of the DataFrame is as follows (for more info on all values, please visit the [YouTube API Comment Documentation](https://developers-dot-devsite-v2-prod.appspot.com/youtube/v3/docs/comments)):
- `kind`
  - Defaults to `youtube#commentThread`
- `etag`
  - the etag of the comment. Internal tag for YouTube API
- `id`
  - A unique comment id
- `videoId`
  - Video Id string (e.g., `C2npCYNnV18`)
- `textDisplay`
  - The display comment text (includes HTML formatting)
- `textOriginal`
  - The raw text of the comment (no HTML)
- `authorDisplayName`
  - The display name of the user who posted the comment
- `authorProfileImageUrl`
  - The profile photo url of the user who posted the comment
- `authorChannelId`
  - The channel url of the user who posted the comment
- `canRate`
  - Indicated whether current viewer can rate the comment
- `canReply`
  - Indicated whether current viewer can reply to the comment
- `isPublic`
  - Indicated whether the comment is public
- `viewerRating`
  - Indicates rating viewer has given comment. ('none' if there is no rating)
- `channelTitle`
  - Title of the channel
- `likeCount`
  - The number of likes the comment has received
- `publishedAt`
  - Date and time that the comment was originally published
- `updatedAt`
  - Date and time that the comment was last updated (it is the same as `publishedAt` if there have been no later updates)