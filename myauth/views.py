from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm

def mylogin(request):
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
            return redirect('home')
        else:
           context['errors'] = True
        #    context['userlog'] = user
    return render(request, 'myauth/login.html', context)


def mylogout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')

def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        from eshop.models import Customer
        from django.contrib.auth import authenticate, login
        customer = Customer(user=user)
        login(request, authenticate(username=user.username, password=user.password))
        return redirect('home')
    return render(request, 'myauth/login.html', {'form': form})
    