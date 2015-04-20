from django.http import HttpResponse
from django.shortcuts import render

def ynmp_get_constituency_from_postcode(postcode):
    if postcode:
        return('Brighton Pavilion') 
    else:
        return('')

def HomePageView(request):
    postcode = request.POST.get('postcode', '')
    constituency = ynmp_get_constituency_from_postcode(postcode)

    return render(request, 'home.html', {
        'constituency': constituency
    })
