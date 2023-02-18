import requests
import json
import base64

def get_content(yyyymmdd):
    """1日分の日記を行単位に分けたlistで返す"""
    url = f'https://api.kagasan.com/ray45422/v2/get?yyyymmdd={yyyymmdd}'
    res = requests.get(url)
    json_dict2 = json.loads(res.text)
    content_b64 = json_dict2['content']
    content = base64.b64decode(content_b64).decode()
    return [{
        "row_num": idx,
        "content": line.replace(',', '，')
    }for idx, line in enumerate(content.split('\n'))]

