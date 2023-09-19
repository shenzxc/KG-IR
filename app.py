#!/usr/bin/env python
from json import dumps
import logging
import os
from flask import (
    Flask,
    request,
    Response,
)

app = Flask(__name__, static_url_path="/static/")
port = os.getenv("PORT", 8085)

from chatbot_graph import ChatBotGraph

handler = ChatBotGraph()


@app.route("/")
def get_index():
    return app.send_static_file("index.html")


@app.route("/search")
def get_search():
    try:
        q = request.args["q"]
    except KeyError:
        return []
    else:

        results = handler.chat_main(q)
        print(results)
        json_data = dumps(results)
        print('json_data = ', json_data)
        return Response(json_data, mimetype="application/json")


if __name__ == "__main__":
    logging.root.setLevel(logging.INFO)
    app.run(port=port)
