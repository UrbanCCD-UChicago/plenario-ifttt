import json

from django.http import HttpResponse
from django.shortcuts import render


# https://platform.ifttt.com/docs#2-create-your-service-and-connect-to-ifttt
def setup(request):

    above = {
        'node': '0000001e0610ba72',
        'feature': 'temperature',
        'value': '0'
    }

    property_comparison = {
        'node': 'foo',
        'curated_property': 'foo',
        'op': 'foo',
        'val': 'foo'
    }

    triggers = {
        'above': above,
        'property_comparison': property_comparison
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
