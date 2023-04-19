from django.shortcuts import render
# from django.http import HttpResponseRedirect

from .models import Profile


# Create your views here.

def profile_page(request):
    qs = Profile.objects.all()
    return render(request, 'profile_page.html', {'data': qs})

