class Calendar:
    def __init__(self, user, classes, header, position, maximumEntries, symbol, url):
        self.user = user
        self.classes = classes
        self.header = header
        self.position = position
        self.maximumEntries = maximumEntries
        self.symbol = symbol
        self.url = url

class FaceRecognitionSMAI:
    def __init__(self, user, classes, position):
        self.user = user
        self.classes = classes
        self.position = position

class FlipClock:
    def __init__(self, user, classes, position):
        self.user = user
        self.classes = classes
        self.position = position

class NewsFeed:
    def __init__(self, user, classes, position, sources):
        self.user = user
        self.classes = classes
        self.position = position
        self.sources = sources

class Weather:
    def __init__(self, user, classes, position, header, location, locationID):
        self.user = user
        self.classes = classes
        self.position = position
        self.header = header
        self.location = location
        self.locationID = locationID

class WeatherForecast:
    def __init__(self, user, classes, position, header, location, locationID, colored):
        self.user = user
        self.classes = classes
        self.position = position
        self.header = header
        self.location = location
        self.locationID = locationID
        self.colored = colored
