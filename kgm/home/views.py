from django.shortcuts import render
from home.models import Event, GalleryImage


# Create your views here.

def home(request):
    events = Event.objects.order_by('date')[:3]
    images = GalleryImage.objects.all()
    return render(request, 'home/home.html', {'events': events, 'images': images})

def about(request):
    return render(request, "home/about.html")

def events(request):
    return render(request, "home/events.html")

def gallery(request):
    images = GalleryImage.objects.all()
    return render(request, "home/gallery.html", {"images": images})

def donations(request):
    return render(request, "home/donations.html")

def contact(request):
    return render(request, "home/contact.html")