from core.module_manager import ModuleManager
from core.user_manager import find_users
from modules.registry import get_module_class, get_available_modules
import os

class App:
    def __init__(self, image_path):
        self.image_path = image_path
        self.users = find_users(self.image_path)
        self.manager = ModuleManager()
        self.manager.load()
        self.manager.sync_users(self.users)

    def run(self):
        while True:
            self._cls()
            self.show_main_menu()

    def show_main_menu(self):
        print("Remote Config Editor for the Magic Mirror\nThe following commands are available:\n")
        print("modules - lists all avalabel modules you have added to the script")
        print("users - lists all detected users form the Face-Recodnition folder") 
        print("edit - edit the configuation of the Magic Mirror")
        print("exit - Exit the editor")
        match input("> ").strip().lower():
            case "modules":
                self.modules()
            case "users":
                print("\n".join(self.users))
            case "edit":
                self.manage_modules()
            case "exit":
                self.manager.save()
                self._cls()
                exit()
            case "":
                self.manager.save()
                exit()
            case _:
                input("Invalid command.")
        
    def modules(self):
        modules = get_available_modules()
        print("available modules:")
        for module in modules:
            print(f"- {module.get_display_name()}")

    def manage_modules(self):
        while True:
            for user, mods in self.manager.get_all_modules().items():
                print(f"{user}: {[m.__class__.__name__ for m in mods]}")
            cmd = input("add <user> | delete <id> | back\n> ").split()
            if not cmd:
                continue
            match cmd[0]:
                case "add" if len(cmd) > 1:
                    self.add_module(cmd[1])
                case "delete" if len(cmd) > 1 and cmd[1].isdigit():
                    if self.manager.delete_module_by_id(int(cmd[1])):
                        print("Deleted.")
                    else:
                        print("ID not found.")
                case "back":
                    break

    def add_module(self, user):
        print("Available modules:")
        self.get_available_modules_with_id()
        module_name = input("Module ID:\n> ").strip()
        mod_class = get_module_class(module_name)
        print(mod_class)
        if not mod_class:
            print("Invalid module.")
            return
        params = mod_class.required_params()
        data = self.request_data(params)
        module = mod_class(user, user + " default", **data)
        self.manager.add_module(user, module)
        print("Module added.")
        
    def get_available_modules_with_id(self):
        modules = get_available_modules()
        for module in modules:
            print(f"- {module.get_info()}")

    def request_data(self, param_schema):
        result = {}
        for key, typ in param_schema.items():
            while True:
                val = input(f"{key} ({typ}): ").strip()
                try:
                    result[key] = self.cast_value(val, typ)
                    break
                except Exception:
                    print("Invalid input.")
        return result

    def cast_value(self, value, typ):
        match typ:
            case "str": return value
            case "int": return int(value)
            case "bool": return value.lower() in ["true", "1"]
            case _: raise ValueError("Unsupported type")
            
    def _cls(self):
        os.system('cls' if os.name=='nt' else 'clear')
