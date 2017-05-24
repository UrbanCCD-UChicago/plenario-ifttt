from django.http import HttpResponse

import json


def JsonUtf8Response(data):
    content_type = 'application/json; encoding=utf-8'
    encoded_data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(encoded_data, content_type=content_type)
