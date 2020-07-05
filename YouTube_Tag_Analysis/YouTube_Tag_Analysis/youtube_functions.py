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


def get_top_tags(df, num):
  """get the list of top tags 

  Args:
      df (DataFrame): DataFrame with videos to get tags from)

  Returns:
      DataFrame : the top tags of 'num' length
      
  """
  video_tags = values_from_list_of_list(df[df.tags.notnull()].tags)

  top_tags_count = Counter(video_tags)
  top_tags = [item[0] for item in top_tags_count.most_common(num)]
  print(f"top_tags: {top_tags}")
  return top_tags

def get_videos(chan_id):
  """get the list of videos for channel id (up to 50)

  Args:
     chan_id, channel ID
  Returns:
      video_id (string) : list of video IDs
  """
      
  videos_request = youtube.search().list(
    part='snippet', 
    q=search_phrase,
    channelId= chan_id,
    order='date',
    type='video',
    maxResults=50)

  videos_results = videos_request.execute()
  
  with open('videos_results.json', 'w') as outfile:
    json.dump(videos_results, outfile, indent=2)

  return videos_results

def videos_to_update(vid_df):
  videos_to_update = []

  #Get a list of videos to update the tags based on
  for item in vid_df["items"]:
    #print(f"video title: {item['snippet']['title']}")
    videos_to_update.append(item['id']['videoId'])

  video_ids = ",".join(videos_to_update)

  return video_ids

def get_old_tags(video_id):
  """get the list of old tags based on video id list 

  Args:
      video_id (DataFrame): DataFrame with videos to update

  Returns:
      vid_tags_df (DataFrame) : df of videos to update tags
  """
  
  videos_details = youtube.videos().list(
    part='snippet,contentDetails,statistics,topicDetails',
    id = video_id
  )


  videos_details_results = videos_details.execute()

  with open('videos_details_results.json', 'w') as outfile:
    json.dump(videos_details_results, outfile, indent=2)


  l_of_responses = []

  for item in videos_details_results['items']:
      try:
          #print(f"Old Tags: {item['snippet']['tags']}")
      
          ID = item['id']
          title = item['snippet']['title']
          catID = item['snippet']['categoryId']
          tags = item['snippet']['tags']
          l_of_responses.append([ID, title, catID, tags])
      except:
          continue
          #print("No tags")

  vid_tags_df = pd.DataFrame(
      l_of_responses,
      columns=[
          "vidId", "vidTitle","categoryId", "tags"]
          )

  return vid_tags_df

def get_top_tag_info(tag_list, top_tags):
  #number of videos with a top tag
  top_tag_vid_count = 0
  #number of top tags used in most recent videos
  top_tag_count = 0
  
  tag_list = tag_list.dropna()

  for tags in tag_list:

    if len(tags)>1:
      
      lower_tags = [t.lower() for t in tags]

      vid_has_top_10_tag = False
      for top_tag in top_tags:
        if top_tag in lower_tags:
          vid_has_top_10_tag = True
          top_tag_count = top_tag_count + 1
      if vid_has_top_10_tag:
        top_tag_vid_count = top_tag_vid_count + 1

  return (top_tag_count, top_tag_vid_count)

def tag_finder_main(search_phrase):
	full_vid_response = get_top_50_vids_details(search_phrase)
	competitor_num_vid = len(full_vid_response.tags)
	top_tags = get_top_tags(full_vid_response, 10)
	return {'top_tags':top_tags, }

#	vids = get_videos(chan_id)
#	vid_ids = videos_to_update(vids)
#	vid_tags_df = get_old_tags(vid_ids)
#	num_vids = len(vids["items"])
#	top_tag_count, top_tag_vid_count = get_top_tag_info(vid_tags_df.tags, top_tags)
#	competitor_top_tag_count, competitor_top_tag_vid_count = get_top_tag_info(full_vid_response.tags, top_tags)
#	return {'vids':vids, 'vid_ids':vid_ids, 'vid_tags_df':vid_tags_df, 'num_vids':num_vids, 
#		    'top_tag_count':top_tag_count, 'top_tag_vid_count':top_tag_vid_count, 
#			'competitor_top_tag_count':competitor_top_tag_count, 
#			'competitor_top_tag_vid_count':competitor_top_tag_vid_count}
	
#count_of_top_tag = f"There are {top_tag_vid_count}/{num_vids} videos with a top tag."
#top_tag_score = f"Your top tag score is {(top_tag_count/(num_vids*10))*100}%."


#competitor_count f"There are {competitor_top_tag_vid_count}/{competitor_num_vid} videos with a top tag.")
#print(f"Competitor top tag score is {competitor_top_tag_count/(competitor_num_vid*10)*100}%.")



