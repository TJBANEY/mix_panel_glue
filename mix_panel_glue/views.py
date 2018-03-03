import json

from django.http import HttpResponse
from django.shortcuts import render
from mixpanel import Mixpanel

def view_home(request):
    template = 'home.html'

    return render(request, template, {})

def mix_panel(request):
    test_user_id = '198909123'
    project_token = 'a386ab7d6aaff75a01f364c63cb681c3'

    mp = Mixpanel(project_token)

    # Tracks an event, 'Sent Message',
    # with distinct_id user_id
    mp.track(test_user_id, 'Sent Message')

    # You can also include properties to describe
    # the circumstances of the event
    mp.track(test_user_id, 'Plan Upgraded', {
        'Old Plan': 'Business',
        'New Plan': 'Premium'
    })

    return HttpResponse(json.dumps({'success': True}), content_type='application/json')