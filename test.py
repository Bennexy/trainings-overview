import os, yaml
import regex as re

def get_regex(template_path=None, extraction_file=None):
    if template_path == None:
        template_path = os.path.abspath(os.path.join("app", "endpoints", "exercise", "helper", "templates"))

    onlyfiles = [f for f in os.listdir(template_path) if os.path.isfile(os.path.join(template_path, f)) and f.endswith(".yaml") or f.endswith(".yml")]

    for file in onlyfiles:
        extract_dict = []
        if extraction_file != None:
            if file in onlyfiles:
                items = yaml.load(open(os.path.abspath(os.path.join("app", "endpoints", "exercise", "helper", "templates", extraction_file))), Loader=yaml.FullLoader)
                extract_dict.append(items)
                
            else:
                print("not foundss")
                #raise ExtractionTemplateNotFound(f"error no such extraction_file '{extraction_file}' found in dir")
        else:
            for file in onlyfiles:
                items = yaml.load(open(os.path.abspath(os.path.join("app", "endpoints", "exercise", "helper", "templates", file))), Loader=yaml.FullLoader)
                extract_dict.append(items)

    return extract_dict

def get_file():
    file_path = os.path.abspath(os.path.join("app", "endpoints", "exercise", "helper", "demo-file.txt"))
    file_data = []
    with open(file_path, "r") as file:
        for line in file:
            file_data.append(line)
    
    return file_data


def get_match(regex_patterns, string):
    for key, pattern in regex_patterns['template']['regex'].items():
        ergeb = re.search(pattern, string)
        if ergeb != None:
            print(key, ergeb.groups())

a = get_regex()[0]

print(type(a))

file = get_file()

for line in file:
    get_match(a, line)





