from django.shortcuts import render

def nosotros(request):
    return render(request, 'nosotros/nosotros.html')