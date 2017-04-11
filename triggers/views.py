import json
import requests
import time
import uuid

from datetime import datetime, timedelta
from django.http import HttpResponse


def model(dictionary):

    dictionary['meta'] = {
        'id': uuid.uuid1().hex,
        'timestamp': int(time.time())
    }

    dictionary['value'] = dictionary['results']

    return dictionary


def above(request):

    args = json.loads(request.body.decode('utf-8'))

    node = args['triggerFields']['node']
    feature = args['triggerFields']['feature']
    value = args['triggerFields']['value']

    condition_tree = '"col": "{0}", "val": "{1}", "op": "ge"'
    condition_tree = '{' + condition_tree.format(feature, value) + '}'
    
    plenario_url = 'http://plenario-private.us-east-1.elasticbeanstalk.com'
    plenario_url += '/v1/api/sensor-networks/array_of_things_chicago/'
    plenario_url += 'query?node={node}&feature={feature}&start_datetime={datetime}'
    plenario_url += '&filter={condition_tree}'

    plenario_url = plenario_url.format(
        node=node,
        feature=feature,
        condition_tree=condition_tree,
        datetime=datetime.utcnow() - timedelta(minutes=6)
    )

    plenario_response = requests.get(plenario_url)

    response = json.dumps({
        'data': [model(o) for o in plenario_response.json()['data']]
    })

    return HttpResponse(response)

