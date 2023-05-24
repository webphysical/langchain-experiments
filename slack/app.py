import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk.signature import SignatureVerifier
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request
from functions import draft_email, analyze_sentiment_pt
from functions import draft_email, analyze_sentiment_pt

from flask import Flask, request, abort

import logging
from functools import wraps
import time
import sys


# Load environment variables from .env file.
load_dotenv(find_dotenv())

# Set Slack API credentials
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]

# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)

# Initialize the Flask app
# Flask is a web application framework written in Python
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@app.event("app_mention")
def handle_mentions(body, say):
    """
    Event listener for mentions in Slack.
    When the bot is mentioned, this function processes the text and sends a response.

    Args:
        body (dict): The event data received from Slack.
        say (callable): A function for sending a response to the channel.
    """
    text = body["event"]["text"]

    mention = f"<@{SLACK_BOT_USER_ID}>"
    text = text.replace(mention, "").strip()

    say("Obrigado, Já estou trabalhando no texto!")
    response = process_message(text)  # chamando a função process_message ao invés de draft_email
    
    # Envia a resposta e a análise de sentimentos
    say(response)


def process_message(message):
    # Realizar a análise de sentimento na mensagem original
    sentiment = analyze_sentiment_pt(message)

    # Criar o rascunho do email
    email_draft = draft_email(message)

    # Adicionar a análise de sentimento à resposta
    response = f"{email_draft}\n\nAnálise de Sentimento da Mensagem Original: {sentiment}"

    return response


# Run the Flask app
if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=8000)
