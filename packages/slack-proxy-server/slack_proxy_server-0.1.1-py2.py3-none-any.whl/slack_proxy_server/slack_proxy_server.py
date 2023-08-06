# -*- coding: utf-8 -*-

import asyncio

from sanic import Sanic
from sanic import response
from sanic_cors import CORS

import slack

app = Sanic(__name__)
CORS(app)
client = slack.WebClient(
    token='xoxb-50275696609-803865662656-QfgheBrmqLdiOCQAnhFYAqA8',
    run_async=True,
)


@app.route("/post-message", methods=["POST"])
async def post_message(request):

    if request.json:
        slack_response = await client.chat_postMessage(
            channel='#robot_notify',
            text=request.json['text']
        )

    else:
        return response.json({}, status=400)

    if slack_response["ok"]:
        return response.json({}, status=200)
    else:
        return response.json({}, status=400)


@app.route("/post-file", methods=["POST"])
async def post_file(request):

    if request.files:
        log_file = request.files.get('upload_file')
        slack_response = await client.files_upload(
            channels='#robot_notify',
            filename=log_file.name,
            file=log_file.body,
            initial_comment='Log is successfully uploaded!',
        )
    else:
        return response.json({}, status=400)

    if slack_response["ok"]:
        return response.json({}, status=200)
    else:
        return response.json({}, status=400)
