import diary_module
import json
import os
from jinja2 import Environment, FileSystemLoader


SETTINGS_FILENAME = 'settings.json'
DST_PATH = 'dst/'
TEMPLATE_FILENAME = 'template.html.j2'
OUTPUT_FILENAME = 'output.html'

def dl():
    settings_dict = json.load(open(SETTINGS_FILENAME, 'r'))
    for setting in settings_dict['targets']:
        detail = setting['detail']
        yyyymmdd = setting['yyyymmdd']
        csv_filename = DST_PATH + yyyymmdd + '.csv'
        if os.path.isfile(csv_filename):
            continue
        print(csv_filename)
        contents = diary_module.get_content(yyyymmdd)
        with open(csv_filename, mode='w') as f:
            f.write('\n'.join([
                f'{yyyymmdd},{detail},{x["row_num"]},{x["content"]}' for x in contents
            ]))

def compile():
    compiled_dict = {'rows':[]}
    settings_dict = json.load(open(SETTINGS_FILENAME, 'r'))
    for setting in settings_dict['targets']:
        yyyymmdd = setting['yyyymmdd']
        csv_filename = DST_PATH + yyyymmdd + '.csv'
        with open(csv_filename) as f:
            compiled_dict['rows'].extend([{
                "yyyymmdd": x[0],
                "detail": x[1],
                "row_num": x[2],
                "content": x[3]
            } for x in [s.strip().split(',') for s in f.readlines() if s.strip() != '']])
    return compiled_dict

def generate():
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(TEMPLATE_FILENAME)
    rendered = template.render(compile())
    with open(OUTPUT_FILENAME, mode='w') as f:
        f.write(rendered)

dl()
generate()

