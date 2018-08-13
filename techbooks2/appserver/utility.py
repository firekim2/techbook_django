import json, urllib


def make_json(input):
    json_result = json.dumps(input, ensure_ascii=False, indent='')
    return json_result


def load_json(input):
    json_result = json.loads(input, encoding='UTF-8')
    return json_result

def request_parse(request, quote=True):
    request_data = request.body.decode('utf-8')
    request_data = request_data.replace('status=', '')
    if quote:
        request_data = urllib.parse.unquote_plus(request_data)
    request_data = request_data.replace(chr(13),"").replace(chr(10),"\\n")
    request_data = request_data.replace("quote\"","\\\"")
    return request_data
