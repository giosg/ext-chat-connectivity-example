import json


def pretty_print_response(method, url, data):
    print("{} {}".format(method.upper(), url))
    if isinstance(data, dict):
        print(json.dumps(data, indent=4))
    elif isinstance(data, str) or isinstance(data, bytes):
        print(json.dumps(json.loads(data), indent=4))
