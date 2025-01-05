import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import dotenv

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)

client = WebClient(token=os.environ['API_KEY'])

app = FastAPI()

class AlertMessage(BaseModel):
    message: str

async def send_message_to_private_channel(message):
    try:
        response = client.chat_postMessage(
            channel=os.environ['CHANNEL_ID'],
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "🚨 *확인 필요* \n 확인이 필요한 Exception이 발생하였습니다 확인 부탁 드립니다"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Exception : {message}"
                    }
                }
            ]
        )

        return {"status": "success", "message": response["message"][message]}
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

@app.post("/send-alert")
async def send_alert(alert: AlertMessage):
    result = await send_message_to_private_channel(alert)
    return result
