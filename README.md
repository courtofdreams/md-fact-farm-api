## How to start this api server
0. Clone the repository
1. (Optional) Create a  python virtual environment, use what ever tool you like, I use anaconda
2. Install the required packages
```bash
pip install youtube-transcript-api
pip install openai
pip install flask
pip install flask-cors
pip install uagents-ai-engine
pip install uagents    
```
4. add your openai api key and youtube key to the api.py file
5. run python
```bash
python api.py
```
6. The server should be running on localhost:5100, please validate by visiting the url in your browser
```bash
http://localhost:5100/api/v1/is-fake-news/sAmwIKTx9hs
```

## How it works
- API will receive youtube video id from client and return if the video is fake news or not. 
- For now it determine if the video is fake news by checking transcript and title of the video
- (Incoming) I'll use try analyze thumbnail too, if i have time lol


## Frontend
- In my computer, ugly af but it works 
- (Incoming) generate image with thumbnail (Overlay, whatever)
- (Issue) Apparently youtube have forbidden other websites to download their thumbnail image directly (CORS issue - -), you might need to find a new way to get the thumbnail image