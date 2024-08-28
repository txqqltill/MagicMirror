from contextlib import suppress
from helpers import *
from modules import *
from ui_texts import *

path_to_images = "../modules/MMM-Face-Recognition-SMAI/public/"
path_to_config_js = "../config/config.js"

modules = {}
users = []
# Saves the current modules object to modules.pkl using Pickle, and compiles the corresponding config.js file.
def save():
    global modules
    global users

    # Delete users that don't exist (have no image associated with them)
    users_to_delete = []
    for user in modules:
        if(user not in users):
            users_to_delete.append(user)
    for user in users_to_delete:
        del modules[user]

    # Add users that should exist (have an image)
    for user in users:
        if(user not in modules):
            modules[user] = []

    # Sort users alphabetically
    modules = dict(sorted(modules.items(), key=lambda x: x[0].lower()))

    # Sort modules for each user by module name
    for user in modules:
        modules[user] = sorted(modules[user], key=lambda x: x.__class__.__name__.lower())

    # Do the actual saving
    save_modules(modules, "modules.pkl")
    compile_js()
def main_menu():
    while True:
        cls()
        command = input(main_menu_text)
        cls()
        match command:
            case "exit":
                exit()
            case "modules":
                modules_command()
            case "users":
                users_command()

            case _:
                print("This is not a valid command. Press Enter to return to the main menu.")
                input()
                
# Functions to run commands from main menu
def add_module_command(user):
    if(user not in modules):
        input("This user doesn't exist. Use the users command from the main menu to list all available users.")
        return
    cls()
    success = False
    while(not success):
        module = input(add_module_text)
        cls()
        match(module):
            case "calendar":
                add_calendar_module(user)
            case "MMM-Face-Recognition-SMAI":
                add_facerec_module(user)
            case "MMM-FlipClock":
                add_flipclock_module(user)
            case "newsfeed":
                add_newsfeed_module(user)
            case "weather":
                add_weather_module(user)
            case "weatherforecast":
                add_weather_forecast_module(user)

            case _:
                input("This module doesn't exist. Press Enter to select a module from the list.")
                continue
        save()
        input("Successfully added module\nPress Enter to return to the main menu.")
        success = True
def modules_command():
    want_exit = False
    while not want_exit:
        cls()
        if(len(modules) == 0):
            input("No users. Press Enter to return to the main menu.")
            return
        
        mcount = 0
        for user, user_modules in modules.items():
            if(len(user_modules) > 0):
                print("Modules for user " + user + ":")
            for module in user_modules:
                print("[" + str(mcount) + "] ", end="")
                match(module.__class__.__name__):
                    case "Calendar":
                        print("calendar:\n\tposition: " + module.position + "\n\theader: " + module.header + "\n\tmaximumEntries: " + module.maximumEntries + "\n\tsymbol: " + module.symbol + "\n\turl: " + module.url)
                    case "FaceRecognitionSMAI":
                        print("MMM-Face-Recognition-SMAI:\n\tposition: " + module.position)
                    case "FlipClock":
                        print("MMM-FlipClock:\n\tposition: " + module.position)
                    case "NewsFeed":
                        print("NewsFeed:\n\tposition: " + module.position + "\n\tsources: " + str(module.sources))
                    case "Weather":
                        print("weather:\n\tposition: " + module.position + "\n\theader: " + module.header + "\n\tlocation: " + module.location + "\n\tlocationID: " + module.locationID)
                    case "WeatherForecast":
                        print("weatherforecast:\n\tposition: " + module.position + "\n\theader: " + module.header + "\n\tlocation: " + module.location + "\n\tlocationID: " + module.locationID + "\n\tcolored: " + module.colored)

                    case _:
                        print("Unknown module (" + module.__class__.__name__ + ")")
                print()
                mcount += 1
        cmd = input(modules_menu_text).split(" ")
        match(cmd[0]):
            case "add":
                add_module_command(cmd[1])
            
            case "delete":
                try:
                    id = int(cmd[1])
                except:
                    input("Please enter a valid ID.")
                    continue
                count = 0
                for user in modules:
                    for module in modules[user]:
                        if(id == count):
                            modules[user].remove(module)
                            save()
                            input("Module successfully deleted")
                        count += 1
                if(id > count):
                    input("This module doesn't exist")
            
            case _:
                want_exit = True
def users_command():
    print("Current users:\n")
    for user in modules:
        if(user != "everyone"):
            print(user)
    input("\nPress Enter to return to the main menu.")

# Functions for adding modules
def add_calendar_module(user):
    data = request_data({"header": "str", "position": "str", "maximumEntries": "int", "symbol": "str", "url": "str"})
    calendar = Calendar(user, user + " default", data["header"], data["position"], data["maximumEntries"], data["symbol"], data["url"])
    modules[user].append(calendar)
def add_facerec_module(user):
    data = request_data({"position": "str"})
    facerec = FaceRecognitionSMAI(user, user + " default", data["position"])
    modules[user].append(facerec)
def add_flipclock_module(user):
    data = request_data({"position": "str"})
    flipclock = FlipClock(user, user + " default", data["position"])
    modules[user].append(flipclock)
def add_newsfeed_module(user):
    data = request_data({"position": "str"})
    newsfeed = NewsFeed(user, user + " default", data["position"], request_news_sources())
    modules[user].append(newsfeed)
def add_weather_module(user):
    data = request_data({"position": "str", "header": "str", "location": "str", "locationID": "int"})
    weather = Weather(user, user + " default", data["position"], data["header"], data["location"], data["locationID"])
    modules[user].append(weather)
def add_weather_forecast_module(user):
    data = request_data({"position": "str", "header": "str", "location": "str", "locationID": "int", "colored": "bool"})
    weather_forecast = WeatherForecast(user, user + " default", data["position"], data["header"], data["location"], data["locationID"], data["colored"])
    modules[user].append(weather_forecast)

# Compile whole config js with all modules
def compile_js():
    module_code = ""
    for user in modules:
        module_code += "        //" + user + "\n"
        for module in modules[user]:
            module_code += compile_module(module)
    with open("templates/config.txt", "r") as js_template_file:
        js_template = js_template_file.read()
        js_template = js_template.replace("//modules", module_code)
        with open(path_to_config_js, "w") as config_js:
            config_js.write(js_template)

# Compile js for any single module
def compile_module(module):
    filename = "templates/" + module.__class__.__name__.lower() + ".txt"
    with open(filename, "r") as file:
        template = file.read()
        with suppress(AttributeError): template = template.replace("//classes", module.classes)
        with suppress(AttributeError): template = template.replace("//header", module.header)
        with suppress(AttributeError): template = template.replace("//position", module.position)
        with suppress(AttributeError): template = template.replace("//fetchInterval", module.fetchInterval)
        with suppress(AttributeError): template = template.replace("//symbol", module.symbol)
        with suppress(AttributeError): template = template.replace("//url", module.url)
        with suppress(AttributeError): template = template.replace("//sources", compile_sources(module.sources))
        with suppress(AttributeError): template = template.replace("//showSourceTitle", module.showSourceTitle)
        with suppress(AttributeError): template = template.replace("//showPublishDate", module.showPublishDate)
        with suppress(AttributeError): template = template.replace("//broadcastNewsFeed", module.broadcastNewsFeed)
        with suppress(AttributeError): template = template.replace("//broadcastNewsUpdates", module.broadcastNewsUpdates)
        with suppress(AttributeError): template = template.replace("//weatherProvider", module.weatherProvider)
        with suppress(AttributeError): template = template.replace("//type", module.type)
        with suppress(AttributeError): template = template.replace("//locationID", module.locationID)
        with suppress(AttributeError): template = template.replace("//location", module.location)
        with suppress(AttributeError): template = template.replace("//colored", module.colored)
        with suppress(AttributeError): template = template.replace("//maximumEntries", module.maximumEntries)
        with suppress(AttributeError): template = template.replace("//apiKey", api_key)
    return template

# Compile js for news feed sources
def compile_sources(sources):
    result = ""
    with open("templates/newsfeedsource.txt", "r") as file:
        source_template = file.read()
    for source in sources:
        result += source_template.replace("//title", source["title"]).replace("//url", source["url"])
    return result

# Load modules and users
try:
    modules = load_modules("modules.pkl")
except:
    pass

for file in os.listdir(path_to_images):
    if(file.endswith("-id.jpg")):
        users.append(file.removesuffix("-id.jpg"))

# Run app
save()
main_menu()
