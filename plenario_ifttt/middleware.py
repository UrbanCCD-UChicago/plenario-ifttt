from django.http import HttpResponse
from plenario_ifttt import settings
from plenario_ifttt.response import error


class IftttTokenAuthMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ifttt_channel_key = request.META.get('HTTP_IFTTT_CHANNEL_KEY')
        if ifttt_channel_key != settings.CHANNEL_KEY:
            return HttpResponse(error('Invalid channel key'), status=401)
        response = self.get_response(request)
        return response
