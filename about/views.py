from django.shortcuts import render
from .models import About
# Create your views here.
def about(request):
    about = About.objects.get()

    data = {
        'about': about
    }
    return render(request, 'about/about.html', data)


def pricing(request):
    return render(request, 'about/licencing.html')
