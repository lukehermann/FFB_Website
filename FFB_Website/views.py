from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')  # show the page with all the submissions
    # return HttpResponse("Hello, Django!")