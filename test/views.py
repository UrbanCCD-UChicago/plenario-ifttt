import json

from django.http import HttpResponse


# https://platform.ifttt.com/docs#2-create-your-service-and-connect-to-ifttt
def setup(request):

    above_fixture = {
        'node': '0000001e0610ba72',
        'sensor': 'temperature',
        'feature': 'temperature',
        'value': '0'
    }

    below_fixture = {
        'node': '0000001e0610ba72',
        'sensor': 'temperature',
        'feature': 'temperature',
        'value': '100'
    }

    equal_fixture = {
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

    response = json.dumps({
        'data': data
    })

    return HttpResponse(response)
