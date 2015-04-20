from django.http import HttpResponse
from django.shortcuts import render

def HomePageView(request):
    if request.method == 'POST':
        return render(request, 'home.html', {'constituency': 'Brighton Pavilion'})
    return render(request, 'home.html')
