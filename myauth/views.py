from django.shortcuts import render

def login(request):
    context = {}
    return render(request, 'myauth/login.html', context)