from django.shortcuts import render, redirect
from .forms import LoginForm

def login(request):
    form = LoginForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        print('is here')
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        from django.contrib.auth import authenticate, login
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home', context)
        else:
           context['erreur'] = True
           context['userlog'] = user
    return render(request, 'myauth/login.html', context)