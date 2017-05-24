import json

from django.http import HttpResponse
from plenario_ifttt.utils import JsonUtf8Response


# https://platform.ifttt.com/docs#2-create-your-service-and-connect-to-ifttt
def status(request):
    return HttpResponse()


# https://platform.ifttt.com/docs#2-create-your-service-and-connect-to-ifttt
def setup(request):

    above_fixture = {
        'network': 'array_of_things_chicago',
        'node': '0000001e0610ba72',
        'sensor': 'temperature',
        'feature': 'temperature',
        'value': '0'
    }

    below_fixture = {
        'network': 'array_of_things_chicago',
        'node': '0000001e0610ba72',
        'sensor': 'temperature',
        'feature': 'temperature',
        'value': '100'
    }

    equal_fixture = {
        'network': 'array_of_things_chicago',
        'node': '0000001e0610ba72',
        'sensor': 'orientation',
        'feature': 'x',
        'value': '3'
    }

    triggers = {
        'above': above_fixture,
        'below': below_fixture,
        'equal': equal_fixture
    }

    samples = {
        'triggers': triggers
    }

    data = {
        'samples': samples
    }

    return JsonUtf8Response({'data': data})
