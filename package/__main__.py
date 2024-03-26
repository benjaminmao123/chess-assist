from package.application import Application
from package.core import logger

import json


if __name__ == "__main__":
    with open("assets/settings.json") as settings_file:
        settings = json.load(settings_file)

    logger.init(settings["logsPath"], settings["isDebug"])

    app = Application(settings)
    app.run()
