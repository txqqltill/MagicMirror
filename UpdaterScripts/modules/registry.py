from modules_definitions import Calendar, FlipClock, FaceRecognitionSMAI, NewsFeed, Weather, WeatherForecast

module_registry = {
    "calendar": Calendar,
    "MMM-Face-Recognition-SMAI": FaceRecognitionSMAI,
    "MMM-FlipClock": FlipClock,
    "newsfeed": NewsFeed,
    "weather": Weather,
    "weatherforecast": WeatherForecast
}

def get_module_class(name):
    return module_registry.get(name.lower())

def get_available_modules():
    return list(module_registry.keys())
