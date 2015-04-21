from urllib2 import urlopen
import json

from django.http import HttpResponse
from django.shortcuts import render


def ynmp_get_constituency_from_postcode(postcode):
    if postcode:
        postcode = postcode.replace(' ', '').lower()
        url = 'http://mapit.mysociety.org/postcode/%s' % postcode
        response = urlopen(url).read()
        json_data = json.loads(response)
        constituency_id = str(json_data['shortcuts']['WMC'])
        constituency_name = json_data['areas'][constituency_id]['name']
        return(constituency_name)
    else:
        return('')

def HomePageView(request):
    postcode = request.POST.get('postcode', '')
    constituency = ynmp_get_constituency_from_postcode(postcode)

    return render(request, 'home.html', {
        'constituency': constituency
    })
