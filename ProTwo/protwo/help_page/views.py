from django.shortcuts import render

# Create your views here.

def help(request):
    my_dict={'help_me':'I am here to help you!!'}
    return render(request, 'help_page/help.html', context=my_dict)
