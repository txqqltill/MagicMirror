class API:
    def __init__(self):
        self.modules = {}
        self._next_id = 1

    def add_module(self, display_name, module_class):
        if not isinstance(module_class, type):
            raise TypeError("You must pass a class.")

        module_id = self._next_id
        self._next_id += 1

        module = _Module(module_id, display_name, module_class)
        self.modules[module_id] = module

        return self

    def list_modules(self):
        return list(self.modules.values())

    def get_module_by_id(self, module_id):
        return self.modules.get(module_id, None)

class _Module:
    def __init__(self, module_id, display_name, module_class):
        self.id = module_id
        self.display_name = display_name
        self.module_class = module_class

    def get_display_name(self):
        return self.display_name

    def get_info(self):
        return f"ID: {self.id}, Name: {self.display_name}"
