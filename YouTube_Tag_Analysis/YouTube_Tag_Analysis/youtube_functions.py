import pandas as pd
from collections import Counter
import json
from apiclient.discovery import build

api_key = "AIzaSyD5m5y0gw8l23ZLUYIlRJi0_MkDHeiv9E4"  #MHR

youtube = build("youtube", "v3", developerKey=api_key)	

def search_get_top_50_vids(search_phrase):
	  """returns 50 YouTube results for a search_phrase`.`

	  Args:
	  search_phrase (String): The phrase to search YouTube.

	  Returns:
		  string: a comma separated string of video ids 
	  """

	  #----------------------------Search for top 50 videos based on search_phrase-------------#
	  top_videos = youtube.search().list(
		  part= 'snippet', 
		  q=search_phrase, 
		  type='video',
		  maxResults=50)

	  top_videos_results = top_videos.execute()

	 
	  l_of_responses = []

	  # get the required values from key "item"
	  for item in top_videos_results['items']:
		  channel_id = item['snippet']["channelId"]
		  channel_title = item['snippet']["channelTitle"]
		  vid_title = item['snippet']["title"]
		  vid_description = item['snippet']["description"]
		  vid_live = item['snippet']["liveBroadcastContent"]
		  vid_id = item["id"]['videoId']

		  #   Append to list
		  l_of_responses.append([
			  channel_id, channel_title, vid_title, vid_description, vid_live, vid_id
		  ])

	  #   Build DF from list, set columns.
	  df_response = pd.DataFrame(
		  l_of_responses,
		  columns=[
			  "channelId", "channelTitle", "vidTitle", "vidDesc", "vidLive", "vidId"
		  ])

	  #   Top 50  unique videos based on search query
	  s_vid_id = ','.join(df_response.vidId.unique().tolist())  
	  
	  return s_vid_id


def get_top_50_vids_details(search_phrase):
	  """returns details of top 50 YouTube results for a search_phrase`.`

		Args:
		search_phrase (String): The phrase to search YouTube.

		Returns:
			full_vid_response (DataFrame): top 50 video details 
		"""

	  
	  #Gets the top 50 video IDs
	  s_vid_id = search_get_top_50_vids(search_phrase)
		
	  #------------------------------Get Details of the top 50 videos--------------------------#
	  top_videos_details = youtube.videos().list(
		part='snippet,contentDetails,statistics,topicDetails',
		id = s_vid_id
	  )

	  top_videos_details_results = top_videos_details.execute()
	  


		#  Each video has different information in the json data  
		#  We used "try-except" but had trouble and had to check if values existed.
		#  Instead, create three DFs based on the current video, merge them together then
		#  Concat to the running list.
		#  The concat takes care of the mismatch of columns
		
		#TODO: Limit the # of columns used
		#TODO: replace all NaN with 0.
	  full_vid_response = pd.DataFrame()
		
	  for row in top_videos_details_results["items"]:
		  s_df = pd.DataFrame({row["id"]: row["snippet"]}).T
		  s_df["id"] = row["id"]
		  st_df = pd.DataFrame({row["id"]: row["statistics"]}).T
		  st_df["id"] = row["id"]
		  cd_df = pd.DataFrame({row["id"]: row["contentDetails"]}).T
		  cd_df["id"] = row["id"]
		  temp_df = pd.merge(s_df, st_df, on="id")
		  temp_df = pd.merge(temp_df, cd_df, on="id")
		  full_vid_response = pd.concat([full_vid_response, temp_df], axis=0)
	  return full_vid_response

def color_negative_red(val):
	"""
	Takes a scalar and returns a string with
	the css property `'color: red'` for negative
	strings, black otherwise.
	"""
	color = 'red' if val < 0 else 'black'
	return 'color: %s' % color

