"""
This agent can respond to plain text questions with data from an AI model and convert it into a machine readable format.
"""
from uagents import Agent, Context, Model
import json
import os
from openai import OpenAI

agent = Agent(
    name="your_agent_name_here",
    seed="your_agent_seed_here",
    port=8001,
    endpoint="http://localhost:8001/submit",
)

os.environ["OPENAI_API_KEY"] = "" # your openai api key
youtube_api_key = "" # your youtube api key
client = OpenAI()

class Request(Model):
    transcript: str
    title: str
    comments: list[str]

class Error(Model):
    text: str

class Data(Model):
    value: int
    unit: str
    timestamp: str
    confidence: float
    source: str
    notes: str

class Response(Model):
    text: str  


def process_fakenews(transcript: str, title: str, comments: list[str], max_tokens: int = 1024):
    """Send a prompt and context to the AI model and return the content of the completion"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "assistant", "content": "Determine whether the following transcript and its title are fake news. Start the answer with 'Yes.' or 'No.' first, followed by a new line and the reasoning"},
                {"role": "user", "content": f'transcript: {transcript} video title: {title} comments: {",".join(comments)}'},
            ]
        )
        message = response.choices[0].message.content
    except Exception as ex:
        print(f"An error occurred retrieving data from the OpenAI: {ex}")
        return None

    print("Got response from AI model: " + message)
    return message


def get_data(ctx: Context, request: Request):
    message_content = process_fakenews(request.transcript, request.title, request.comments, max_tokens=2048)
    try:
        msg = Response(text=message_content)
        return msg
    except Exception as ex:
        ctx.logger.exception(f"An error occurred retrieving data from the AI model: {ex}")
        return Error(text="Sorry, I wasn't able to answer your request this time. Feel free to try again.")


@agent.on_event("startup")
async def hi(ctx: Context):
    ctx.logger.info(f"Starting up {agent.name}")
    ctx.logger.info(f"With address: {agent.address}")
    ctx.logger.info(f"And wallet address: {agent.wallet.address()}")
    

@agent.on_query(model=Request, replies={Response})
async def query_handler(ctx: Context, sender: str, request: Request):
    ctx.logger.info("Query received")
    try:
        response = get_data(ctx, request) 
        ctx.logger.info(f"Response: {response}")
        await ctx.send(sender, response)
    except Exception as e:
        error_message = f"Error fetching job details: {str(e)}"
        ctx.logger.error(error_message)
        await ctx.send(sender, Error(text=str(error_message)))

if __name__ == "__main__":
    agent.run()