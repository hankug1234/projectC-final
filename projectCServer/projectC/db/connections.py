from sqlalchemy import create_engine
import json
import os

class CreateDB():
    def __init__(self):
        path = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-3] + ["config", "sqlConfig.json"])
        with open(path,"r") as file:
            config = json.load(file)
            self.user = config["user"]
            self.pwd = config["pwd"]
            self.host = config["host"]
            self.database = config["database"]
            self.url = f"mysql+pymysql://{self.user}:{self.pwd}@{self.host}"
            self.engine = create_engine(self.url,echo=True)
            self.engine.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")

class Engine():
    def __init__(self):
        path = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-3] + ["config", "sqlConfig.json"])
        with open(path,"r") as file:
            config = json.load(file)
            self.user = config["user"]
            self.pwd = config["pwd"]
            self.host = config["host"]
            self.database = config["database"]
            self.url = f"mysql+pymysql://{self.user}:{self.pwd}@{self.host}/{self.database}"
            self.engine = create_engine(self.url,echo=True)

    def getConnection(self):
        return self.engine

