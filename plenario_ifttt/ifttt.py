import json

from django.http import HttpResponse
from plenario_ifttt.utils import JsonUtf8Response


# https://platform.ifttt.com/docs#2-create-your-service-and-connect-to-ifttt
def status(request):
    return HttpResponse()


# https://platform.ifttt.com/docs#2-create-your-service-and-connect-to-ifttt
def setup(request):
    data = {
      "data": {
        "samples": {
          "triggers": {
            "alert": {
              "node": "0000001e0610b9fd",
              "feature": "temperature.internal_temperature",
              "operator": "gt",
              "value": "0"
            },
            "nearest": {
              "location": {
                "lat": "42",
                "lng": "-81",
                "address": "Somewhere in Chicago",
                "description": "Foobar"
              },
              "feature": "temperature.internal_temperature",
              "operator": "gt",
              "value": "0"
            }
          }
        }
      }
    }

    return JsonUtf8Response(data)
