from flask import Flask, json
import openai_service
from flask_cors import CORS

api = Flask(__name__)
CORS(api)


@api.route('/api/v1/is-fake-news/<id>', methods=['GET'])
async def is_fakenews(id):
    title = openai_service.get_youtube_title(id)
    transcript = openai_service.get_youtube_transcript(id)
    comments = openai_service.get_youtube_comments(id)
    result = await openai_service.process_fakenews(title, transcript, comments)

    split_index = result.index(".") + 1
    conclusion = result[:split_index].strip()  
    reasoning = result[split_index:].strip()
    print("conclusion " + conclusion)
    is_faknews_result = { "result": conclusion.lower() == 'yes', "reason": reasoning }
    
    return json.dumps(is_faknews_result)


@api.route('/api/v1/transcript/<id>', methods=['GET'])
def get_transcript(id):
    transcript = openai_service.get_youtube_transcript(id)
    return json.dumps({ "transcript": transcript })


@api.route('/api/v1/comments/<id>', methods=['GET'])
def get_comments(id):
    comment = openai_service.get_youtube_comments(id)
    
    print(comment)

    is_fakenews_result = { "result": "\n".join(comment) }
    
    return json.dumps(is_fakenews_result)

if __name__ == '__main__':
    api.run(host='0.0.0.0',port=5100)