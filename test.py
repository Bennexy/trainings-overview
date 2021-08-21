import os, yaml

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


a = get_regex()

print(a)



