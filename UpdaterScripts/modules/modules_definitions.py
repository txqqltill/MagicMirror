class Calendar:
    def __init__(self, user, classes, header, position, maximumEntries, symbol, url):
        self.user = user
        self.classes = classes
        self.header = header
        self.position = position
        self.maximumEntries = maximumEntries
        self.symbol = symbol
        self.url = url

    @staticmethod
    def required_params():
        return {
            "header": "str",
            "position": "str",
            "maximumEntries": "int",
            "symbol": "str",
            "url": "str"
        }

class FaceRecognitionSMAI:
    def __init__(self, user, classes, position, prompt):
        self.user = user
        self.classes = classes
        self.position = position
        self.prompt = prompt

    @staticmethod
    def required_params():
        return {
            "position": "str",
            "prompt": "str"
        }

class FlipClock:
    def __init__(self, user, classes, position):
        self.user = user
        self.classes = classes
        self.position = position

    @staticmethod
    def required_params():
        return {
            "position": "str"
        }

class NewsFeed:
    def __init__(self, user, classes, position, sources):
        self.user = user
        self.classes = classes
        self.position = position
        self.sources = sources

    @staticmethod
    def required_params():
        return {
            "position": "str",
            "sources": "news_sources"
        }

class Weather:
    def __init__(self, user, classes, position, header, location, locationID):
        self.user = user
        self.classes = classes
        self.position = position
        self.header = header
        self.location = location
        self.locationID = locationID

    @staticmethod
    def required_params():
        return {
            "position": "str",
            "header": "str",
            "location": "str",
            "locationID": "int"
        }

class WeatherForecast:
    def __init__(self, user, classes, position, header, location, locationID, colored):
        self.user = user
        self.classes = classes
        self.position = position
        self.header = header
        self.location = location
        self.locationID = locationID
        self.colored = colored

    @staticmethod
    def required_params():
        return {
            "position": "str",
            "header": "str",
            "location": "str",
            "locationID": "int",
            "colored": "bool"
        }
