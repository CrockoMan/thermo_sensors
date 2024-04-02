from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.context_processors import csrf


def render_to_response(param, args):
    pass


def register(request):
    return render(request, 'users/register.html')


def login(request, user=None):
    args = {}
#    args.update(csrf(request))
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "Пользователь не найден"
            return render(request, 'users/login.html', args)
    else:
        return render(request, 'users/login.html', args)

def logout(request):
    auth.logout(request)
    return redirect("/")
