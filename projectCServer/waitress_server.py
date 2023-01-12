from waitress import serve
import os,json
import app

if __name__ == "__main__":
    path = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1] + ["config", "appConfig.json"])
    with open(path, "r") as file:
        config = json.load(file)
        config = config["app"]
    serve(app.app, host=config["host"], port=config["port"] ,threads=4)
