

from flask import Flask
from apis import *
import os,json
from projectC.db.daos import InitDB


def createApp():
    InitDB()
    app = Flask(__name__)
    app.register_blueprint(analysis.blueprint,url_prefix="/analysis")
    app.register_blueprint(client.blueprint,url_prefix="/client")
    app.register_blueprint(video.blueprint,url_prefix="/video")
    app.register_blueprint(videoPlay.videoPlay,url_prefix="/videoPlay")
    return app

app = createApp()

if __name__ == "__main__":
    path = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1] + ["config", "appConfig.json"])
    with open(path, "r") as file:
        config = json.load(file)
        config = config["app"]
    app.run(debug=config["debug"], host=config["host"], port=config["port"])




