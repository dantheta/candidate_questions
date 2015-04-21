from urllib2 import urlopen, HTTPError, URLError
import json

from django.shortcuts import render, redirect
from django.db import IntegrityError

from voters.models import Constituency


def ynmp_get_constituency_from_postcode(postcode):
    postcode = postcode.replace(' ', '').lower()
    url = 'http://mapit.mysociety.org/postcode/%s' % postcode
    wmc_id = None
    wmc_name = None
    try:
        response = urlopen(url)
        status_code = response.getcode()
        page_data = response.read()
        json_data = json.loads(page_data)
        wmc_id = json_data['shortcuts']['WMC']
        wmc_name = json_data['areas'][str(wmc_id)]['name']
    except HTTPError as e:
        status_code = e.code
    return({
        'status_code': status_code,
        'constituency_id': wmc_id,
        'name': wmc_name,
    })

def HomePageView(request):
    if request.method == 'POST':
        postcode = request.POST['postcode']
        wmc_data = ynmp_get_constituency_from_postcode(postcode)
        if wmc_data['status_code'] == 200:
            try:
                wmc = Constituency.objects.get(
                    constituency_id=wmc_data['constituency_id']
                )
            except Constituency.DoesNotExist:
                wmc = Constituency.objects.create(
                    constituency_id=wmc_data['constituency_id'],
                    name=wmc_data['name']
                )
            return redirect('/constituencies/%d/' % (wmc.constituency_id,))
        else:
            return redirect('/')

    return render(request, 'home.html')

def ConstituencyView(request, wmc_id):
    wmc_name = Constituency.objects.get(constituency_id=wmc_id).name
    return render(request, 'constituency.html', {'constituency': wmc_name})
