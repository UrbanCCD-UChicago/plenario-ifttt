import json
import requests
import time
import uuid

from datetime import datetime, timedelta
from django.http import HttpResponse
from plenario_ifttt import settings
from plenario_ifttt.response import error


def fmt(dictionary, prop) -> dict:
    """Format a single data observation into a format ifttt expects"""

    dictionary['meta'] = {
        'id': uuid.uuid1().hex,
        'timestamp': int(time.time())
    }

    # Would be nice to have a better way of formatting this to utc
    dictionary['created_at'] = dictionary['datetime'] + 'Z'
    dictionary['value'] = dictionary['results'][prop]

    return dictionary


def query(node, feat, prop, val, dt, op) -> dict:
    """Send a request to plenario with a simple comparison filter"""

    condition_tree = '"col": "{}", "val": "{}", "op": "{}"'
    condition_tree = '{' + condition_tree.format(prop, val, op) + '}'

    url = settings.PLENARIO_URL
    url += '/v1/api/sensor-networks/array_of_things_chicago/query'
    url += '?node={}&feature={}&start_datetime={}&filter={}&limit=5'
    url = url.format(node, feat, dt, condition_tree)

    print(url)

    return requests.get(url).json()


def trigger(fn):
    """Decorator for ifttt triggers, which all have to go through the motions
    of extracting the query arguments and encoding the results"""

    def wrapper(request):

        # Values sent along with a polling request from ifttt
        args = json.loads(request.body.decode('utf-8'))

        trigger_fields = args.get('triggerFields')
        if not trigger_fields:
            return HttpResponse(error('Missing trigger fields'), status=400)

        # It might be a bit confusing to see the feature extracted from
        # 'property', and to see 'property' extracted from feature. This
        # is intentional, my reasoning being that users will probably only
        # think of sensors in terms of what they report - I was hoping
        # this would make it more intuitive
        node = args['triggerFields'].get('node')
        feature = args['triggerFields'].get('sensor')
        prop = args['triggerFields'].get('feature')
        value = args['triggerFields'].get('value')

        if not all({node, feature, prop, value}):
            return HttpResponse(error('Invalid trigger fields'), status=400)

        # Set up the query and only ask for the top n values from 15 minutes ago
        limit = args['limit'] if args.get('limit') is not None else 3
        fifteen_minutes_ago = datetime.utcnow() - timedelta(minutes=15)
        results = fn(node, feature, prop, value, fifteen_minutes_ago)

        payload = json.dumps({
            'data': [fmt(o, prop) for o in results['data']][:limit]
        })
        
        return HttpResponse(payload)

    return wrapper


@trigger
def above(*args):
    """For receiving alerts when some property goes above a certain value"""
    return query(*args, op='ge')


@trigger
def below(*args):
    """For receiving alerts when some property goes below a certain value"""
    return query(*args, op='le')


@trigger
def equal(*args):
    """For receiving alerts when some property is equal to a certain value"""
    return query(*args, op='eq')
