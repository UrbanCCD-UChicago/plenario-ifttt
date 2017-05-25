import json
import requests
import time
import uuid

from datetime import datetime, timedelta
from django.http import HttpResponse
from plenario_ifttt import settings
from plenario_ifttt.response import error
from plenario_ifttt.utils import JsonUtf8Response


def fmt(dictionary, prop) -> dict:
    """Format a single data observation into a format ifttt expects"""

    dictionary['meta'] = {
        'id': uuid.uuid1().hex,
        'timestamp': int(time.time())
    }

    # Would be nice to have a better way of formatting this to utc
    dictionary['created_at'] = dictionary['datetime'] + 'Z'
    dictionary['sensor'] = dictionary['feature']
    dictionary['feature'] = prop
    dictionary['value'] = dictionary['results'][prop]

    return dictionary


def query(node, feat, dt, val, op, limit) -> dict:
    """Send a request to plenario with a simple comparison filter"""

    prop = feat.rsplit('.', 1)[-1]

    condition_tree = '"col": "{}", "val": "{}", "op": "{}"'
    condition_tree = '{' + condition_tree.format(prop, val, op) + '}'

    url = settings.PLENARIO_URL
    url += '/v1/api/sensor-networks/array_of_things_chicago/query'
    url += '?node={}&feature={}&start_datetime={}&filter={}&limit={}'
    url = url.format(node, feat, dt, condition_tree)

    return requests.get(url).json()


def alert(request):

    # Values sent along with a polling request from ifttt
    args = json.loads(request.body.decode('utf-8'))

    trigger_fields = args.get('triggerFields')
    if not trigger_fields:
        return HttpResponse(error('Missing trigger fields'), status=400)

    node = args['triggerFields'].get('node')
    feature = args['triggerFields'].get('feature')
    op = args['triggerFields'].get('operator')
    value = args['triggerFields'].get('value')

    if not all({node, prop, op, value}):
        return HttpResponse(error('Invalid trigger fields'), status=400)

    # Set up the query and only ask for the top n values from 15 minutes ago
    limit = args['limit'] if args.get('limit') is not None else 3
    fifteen_minutes_ago = datetime.utcnow() - timedelta(minutes=15)
    results = query(node, feature, fifteen_minutes_ago, value, op, limit)

    payload = json.dumps({
        'data': [fmt(o, prop) for o in results['data']]
    })

    return HttpResponse(payload)


# https://platform.ifttt.com/docs/api_reference#trigger-field-dynamic-options
def options(request, field):
    """Returns json data used to populate drop down lists during the creation
    of IFTTT applets."""

    field_to_api = {
        'node': 'nodes',
        'sensor': 'sensors',
        'feature': 'features'
    }

    api_endpoint = field_to_api[field]

    url = settings.PLENARIO_URL
    url += '/v1/api/sensor-networks/array_of_things_chicago/{}'
    url = url.format(api_endpoint)

    response = requests.get(url).json()

    data = []
    for e in response['data']:
        result = {}
        if field == 'node':
            result['label'] = e['properties']['id']
            result['value'] = e['properties']['id']
        else:
            result['label'] = e['name']
            result['value'] = e['name']
        data.append(result)

    return JsonUtf8Response({'data': data})
