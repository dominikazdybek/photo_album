from django.shortcuts import render_to_response, render, redirect
from django.views import View
from .models import Photo
from .forms import UploadFileForm
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import RequestContext
from django.views.generic.edit import FormView


# Create your views here.
class UserLoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "user_login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"],
                                password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                # return HttpResponseRedirect('/logout')
                return HttpResponseRedirect("/main")

        return render(request, "user_login.html", {"form": form, "blad": True})



class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/user_login")


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = "/user_login"

    def form_valid(self, form):
        # dodawanie
        u = User()
        u.username = form.cleaned_data['username']
        u.first_name = form.cleaned_data['first_name']
        u.last_name = form.cleaned_data['last_name']
        u.email = form.cleaned_data['email']
        u.set_password(form.cleaned_data["password1"])
        u.save()

        return super(RegisterView, self).form_valid(form)


class MainView(View):

    def get(self, request):
        photos = Photo.objects.all()
        user = request.user
        form = UploadFileForm()
        return render(request, 'main.html', {'photos': photos,
                                             'user': user,
                                             'form': form})

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        photos = Photo.objects.all()
        user = request.user
        if form.is_valid():
            instance = Photo(image = request.FILES['image'], user=user)
            instance.save()
            return HttpResponseRedirect("/main/")
        return render(request, 'main.html', {'photos': photos,
                                             'form': form})
