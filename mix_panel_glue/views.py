import json

from django.http import HttpResponse
from django.shortcuts import render
from mixpanel import Mixpanel, Consumer

import requests
from requests.auth import HTTPBasicAuth

def view_home(request):
    template = 'home.html'

    return render(request, template, {})

class LoggingConsumer(object):
    def __init__(self):
        self.mp_log = open("MIXPANEL_LOG.txt", "w+")

    def send(self, endpoint, json_message):
        self.mp_log.write("{0}::{1}\n".format(endpoint, json_message))

def mix_panel(request):
    # Since all User IDs are anonymous, do we create this using like an MD5 algorithm based on their IP, location, etc. ?
    test_user_id = '198909127'
    project_token = 'a386ab7d6aaff75a01f364c63cb681c3'

    mp = Mixpanel(project_token)
    # mp = Mixpanel(project_token, LoggingConsumer())

    # Tracks an event, 'Sent Message',
    # with distinct_id user_id
    mp.track(test_user_id, 'Sent Message')

    # You can also include properties to describe
    # the circumstances of the event
    mp.track(test_user_id, 'Plan Upgraded', {
        'Old Plan': 'Business',
        'New Plan': 'Premium'
    })

    mp.people_set(test_user_id, {
        '$first_name': 'Jane',
        '$last_name': 'Doe',
        '$email': 'jdoe@gmail.com',
        '$phone': '1112224444',
        'Favorite Color': 'blue'
    }, meta={'$ignore_time': 'true'})

    mp.people_append(test_user_id, {
        'Favorite Fruits': 'Apples'
    })

    # Are we going to be able to track this ourselves ? Or do we need to relate our data to final checkout data
    # on some related unique identifier that WalMart has ?

    # Records a charge of $9.99 from user '12345'
    mp.people_track_charge(test_user_id, 9.99)

    # records a charge of $30.50 on the 2nd of January
    mp.people_track_charge(test_user_id, 30.50, {
        '$time': '2013-01-02T09:32:00'
    })

    return HttpResponse(json.dumps({'success': True}), content_type='application/json')


def mix_panel_queue(request):
    # The default Mixpanel consumer will take
    # endpoints and messages and send them to Mixpanel
    consumer = Consumer()

    with open("MIXPANEL_LOG.txt", "r+") as read_log:
        for line in read_log:
            (endpoint, message) = line.split('::', 1)
            consumer.send(endpoint, message)

    return HttpResponse(json.dumps({'success': True}), content_type='application/json')

def mix_panel_query(request):
    data = {
        'params': '{"from_date":"2016-01-01", "to_date": "2016-01-07"}',
        'script': '\'function main(){ return Events(params).groupBy(["name"], mixpanel.reducer.count()) }\''
    }

    response = requests.post('https://mixpanel.com/api/2.0/jql', data=data, auth=HTTPBasicAuth(username='450e678a456f8ea6bda0d31b168990d9', password=''))

    x = 5

    return HttpResponse(json.dumps({'success': True}), content_type='application/json')

# def mix_pane_queue_queue(request):
#     # In your time-sensitive process
#     class EnqueueingConsumer(object):
#         def send(self, endpoint, json_message):
#             YOUR_QUEUE.set('mixpanel_queue', JSON.dumps([endpoint, json_message]))
#
#     mp = mixpanel.Mixpanel(YOUR_TOKEN, EnqueueingConsumer())
#
#     # Track just like you would in any other situation
#     mp.track(user_id, 'Sent Message')
#     mp.people_increment(user_id, {
#         'Messages Sent': 1
#     })
#
#     # In a worker process on another machine
#     consumer = mixpanel.Consumer()
#     while True:
#         job = YOUR_QUEUE.get('mixpanel_queue')
#         consumer.send(*JSON.loads(job))
#
#     return HttpResponse(json.dumps({}), content_type='application/json')