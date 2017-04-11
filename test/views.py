from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# https://platform.ifttt.com/docs#2-create-your-service-and-connect-to-ifttt
@csrf_exempt
def setup(request):
    data = {}

    triggers = {
        'above': {}
    }

    samples = {
        'triggers': triggers
    }

    response = {
        'data': data,
        'samples': samples
    }

    return JsonResponse(response)