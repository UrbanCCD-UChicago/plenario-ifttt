import json
import requests
import time
import uuid

from datetime import datetime, timedelta
from django.http import HttpResponse
from plenario_ifttt import settings


def model(dictionary) -> dict:
    """Format a single data observation into a format ifttt expects"""

    dictionary['meta'] = {
        'id': uuid.uuid1().hex,
        'timestamp': int(time.time())
    }

    dictionary['value'] = dictionary['results']

    return dictionary


def query(node, feat, prop, val, dt, op) -> dict:
    """Send a request to plenario with a simple comparison filter"""

    condition_tree = '"col": "{}", "val": "{}", "op": "{}"'
    condition_tree = '{' + condition_tree.format(prop, val, op) + '}'

    url = settings.PLENARIO_URL
    url += '/v1/api/sensor-networks/array_of_things_chicago/query'
    url += '?node={}&feature={}&start_datetime={}&filter={}'
    url = url.format(node, feat, dt, condition_tree)

    return requests.get(url).json()


def trigger(fn):
    """Decorator for ifttt triggers, which all have to go through the motions
    of extracting the query arguments and encoding the results"""

    def wrapper(request):

        # Values sent along with a polling request from ifttt
        args = json.loads(request.body.decode('utf-8'))
        node = args['triggerFields']['node']
        feature = args['triggerFields']['feature']
        value = args['triggerFields']['value']

        # Queries will ask from fifteen minutes ago
        fifteen_minutes_ago = datetime.utcnow() - timedelta(minutes=15)

        results = fn(node, feature, feature, value, fifteen_minutes_ago)

        # Retrieve up to three of the results
        payload = json.dumps({
            'data': [model(o) for o in results['data']][:3]
        }).encode('uft-8')
        
        return HttpResponse(payload)

    return wrapper


@trigger
def above(*args):
    """For receiving alerts when some property goes above a certain value"""
    return query(*args, 'ge')


@trigger
def below(*args):
    """For receiving alerts when some property goes below a certain value"""
    return query(*args, 'le')


@trigger
def equal(*args):
    """For receiving alerts when some property is equal to a certain value"""
    return query(*args, 'eq')
