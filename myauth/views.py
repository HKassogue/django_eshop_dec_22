from django.shortcuts import render, redirect
from .forms import LoginForm

def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        from django.contrib.auth import authenticate, login
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
           context['errors'] = True
    return render(request, 'myauth/login.html', context)