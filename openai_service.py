from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
import requests
import os
from uagents.query import query
from uagents import Model
import json
from uagents.envelope import Envelope 

## Tmr change the prompt to be more specific on fake news and determine frontend
AGENT_ADDRESS = ""

class Request(Model):
    transcript: str
    title: str
    comments: list[str]

def get_youtube_transcript(url):
    print(url)
    video_id = url.replace('https://www.youtube.com/watch?v=', '')
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    output = ''
    for x in transcript:
        sentence = x['text']
        output += f' {sentence}\n'
    return output

def get_youtube_title(url):
    video_id = url.replace('https://www.youtube.com/watch?v=', '')
    api_url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=snippet&key={youtube_api_key}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        title = data['items'][0]['snippet']['title']
        return title
    else:
        print("Error fetching video information: ", response.status_code)
        return None

def get_youtube_comments(url):
    video_id = url.replace('https://www.youtube.com/watch?v=', '')
    api_url = f"https://www.googleapis.com/youtube/v3/commentThreads?videoId={video_id}&part=snippet&key={youtube_api_key}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        comments = []
    
        for item in data['items']:
            text_display = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(text_display)
        return comments;    
    else:
        print("Error fetching video information: ", response.status_code)
        return None


# Function to send a query to the agent
async def agent_query(req):
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=15)
    if isinstance(response, Envelope):
        data = json.loads(response.decode_payload())
        print(data)
        return data
    return response
    
async def process_fakenews(title, transcript, comments):
    print(f"processing video: {title}")
    response = await agent_query(Request(transcript=transcript, title=title, comments=comments))
    return response['text']    