import os
import pickle

# clear screen
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# load modules from save file
def load_modules(filename):
    with open(filename, "rb") as objFile:
        return pickle.load(objFile)

# write modules to save file
def save_modules(obj, filename):
    with open(filename, "wb") as objFile:
        pickle.dump(obj, objFile, pickle.HIGHEST_PROTOCOL)

def request_data(params):
    data = {}
    for param in params:
        success = False
        while not success:
            value = input("Set " + param + " (" + params[param] + "): ")
            match(params[param]):
                case "str":
                    data[param] = value
                    success = True
                
                case "int":
                    try:
                        int(value)
                        data[param] = value
                        success = True
                    except:
                        print("Wrong data type (expected was \"" + params[param] + "\")")
                
                case "bool":
                    value_lower = value.lower()
                    if(value_lower == "true" or value_lower == "false"):
                        data[param] = value_lower
                        success = True
                    else:
                        print("Wrong data type (expected was \"" + params[param] + "\")")
                
                case _:
                    print("Wrong data type (expected was \"" + params[param] + "\")")
    return data

def request_news_sources():
    sources = []
    stop = False
    while not stop:
        cls()
        title = input("Set source title (str): ")
        url = input("Set source url (str): ")
        sources.append({"title": title, "url": url})
        if(input("Press Enter to continue, or type anything and press Enter to add another source.")) == "":
            stop = True
    return sources

api_key = ""
with open("weather_api_key.txt", "r") as api_file:
    api_key = api_file.read()