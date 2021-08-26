import sys
sys.path.append('.')
import os, yaml
import regex as re

class Extractor:

    def __init__(self, template_folder: str = "default") -> None:

        self.template_folder = template_folder
        self.templates_raw = []

        # chosen template data
        self.name = None
        self.documentation = None
        self.date_regex = None
        self.exercise_regex = None


        if template_folder == "default":
            self.template_folder = os.path.abspath(os.path.join("app", "endpoints", "exercise", "helper", "templates"))
    
    def template_load(self, template_name: str = "default"):

        files = [f for f in os.listdir(self.template_folder) if os.path.isfile(os.path.join(self.template_folder, f)) and f.endswith(".yaml") or f.endswith(".yml")]

        for file in files:
            items = yaml.load(open(os.path.join(self.template_folder, file)), Loader=yaml.FullLoader)
            self.templates_raw.append(items)

        for temp in self.templates_raw:
            if temp['name'] == template_name:
                reg = temp['template']['regex']
                self.name = temp['name']
                self.documentation = temp['template']['format']
                self.date_regex = reg['date']
                self.exercise_regex = reg['exercise']

        print(self.name)
        print(self.documentation)
        print(self.date_regex)
        print(self.exercise_regex)


extrator = Extractor()
extrator.template_load()





