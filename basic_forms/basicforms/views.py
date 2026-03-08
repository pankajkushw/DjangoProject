from django.shortcuts import render
from . import forms
# Create your views here.

def index(request):
    return render (request, 'basicforms/index.html')


def form_name_view(request):
    form = forms.FormName()
    if request.method== 'POST':
        form = forms.FormName(request.POST)

        if form.is_valid():
            print("validation sucess")
            print("Name: " + form.cleaned_data['name'])
            print("Email: " + form.cleaned_data['email'])
            print("Text Area: " + form.cleaned_data['text'])
    return render(request, 'basicforms/form_page.html', {'form':form})
