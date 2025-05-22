import modules_definitions as modules

module_registry = {
    "calendar": modules.Calendar,
    "mmm-face-recognition-smai": modules.FaceRecognitionSMAI,
    "mmm-flipclock": modules.FlipClock,
    "newsfeed": modules.NewsFeed,
    "weather": modules.Weather,
    "weatherforecast": modules.WeatherForecast
}

def get_module_class(name):
    return module_registry.get(name.lower())

def get_available_modules():
    return list(module_registry.keys())
