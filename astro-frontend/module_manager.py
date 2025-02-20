import os
import json

MODULES_DIR = "/mnt/ASTRO/modules"
REGISTRY_FILE = "/mnt/ASTRO/storage/modules_registry.json"

class ModuleManager:
    def __init__(self):
        self.modules = {}
        self.load_modules()

    def load_modules(self):
        """ Charge les modules disponibles et met à jour le registre """
        self.modules = {}
        for module_name in os.listdir(MODULES_DIR):
            module_path = os.path.join(MODULES_DIR, module_name, "config.json")
            if os.path.exists(module_path):
                with open(module_path, "r") as f:
                    module_config = json.load(f)
                    self.modules[module_name] = module_config

        # Mettre à jour le registre
        with open(REGISTRY_FILE, "w") as f:
            json.dump(self.modules, f, indent=4)

    def get_route_for_command(self, command):
        """ Associe une commande à un module et une route """
        for module_name, config in self.modules.items():
            for route in config["routes"]:
                if command in route:  # Améliorer avec NLP plus tard
                    return module_name, route
        return None, None

# Instance du Module Manager
module_manager = ModuleManager()
