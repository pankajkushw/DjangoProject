from django.shortcuts import render


# Create your views here.

def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, "home/about.html")

def events(request):
    return render(request, "home/events.html")

def gallery(request):
    return render(request, "home/gallery.html")

def donations(request):
    return render(request, "home/donations.html")

def contact(request):
    return render(request, "home/contact.html")