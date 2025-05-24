import modules.api as API
import modules.modules_definitions as modules

__added_modules = API.API()
__added_modules.add_module("Calendar", modules.Calendar) \
             .add_module("MMM-Face-Recognition-SMAI", modules.FaceRecognitionSMAI) \
             .add_module("MMM-Flipclock", modules.FlipClock) \
             .add_module("Newsfeed", modules.NewsFeed) \
             .add_module("Weather", modules.Weather) \
             .add_module("Weatherforecast", modules.WeatherForecast)

def get_module_class(id):
    return __added_modules.get_module_by_id(id)

def get_available_modules():
    return __added_modules.list_modules()
