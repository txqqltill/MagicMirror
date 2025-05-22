import pickle

class ModuleManager:
    def __init__(self, path="data/modules.pkl"):
        self.path = path
        self.modules = {}

    def load(self):
        try:
            with open(self.path, "rb") as f:
                self.modules = pickle.load(f)
        except FileNotFoundError:
            self.modules = {}

    def save(self):
        with open(self.path, "wb") as f:
            pickle.dump(self.modules, f, pickle.HIGHEST_PROTOCOL)

    def sync_users(self, users):
        self.modules = {u: self.modules.get(u, []) for u in users}

    def add_module(self, user, module):
        self.modules.setdefault(user, []).append(module)

    def delete_module_by_id(self, module_id):
        idx = 0
        for user, mod_list in self.modules.items():
            for m in mod_list:
                if idx == module_id:
                    mod_list.remove(m)
                    return True
                idx += 1
        return False

    def get_all_modules(self):
        return self.modules
