from django.shortcuts import render_to_response, render, redirect
from django.views import View
from .models import Photo, Like
from .forms import UploadFileForm
from django.http import HttpResponseRedirect, HttpResponse
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
                return HttpResponseRedirect("/")

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
        photos = Photo.objects.all().order_by('-creation_date')
        user = request.user
        like_dislike_user = Like.objects.filter(author=user)
        for photo in photos:
            like_dislike = photo.like_set.filter(author=user).last()
            if like_dislike is not None:
                photo.like_dislike_user = like_dislike.liked
            else:
                photo.like_dislike_user = False
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
            return HttpResponseRedirect("/")
        return render(request, 'main.html', {'photos': photos,
                                             'form': form})


class UserView(View):

    def get(self, request):
        user = request.user
        photos = Photo.objects.filter(user=user).order_by('-creation_date')
        form = UploadFileForm()
        return render(request, 'main.html', {'photos': photos,
                                             'user': user,
                                             'form': form})

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        photos = Photo.objects.all()
        user = request.user
        if form.is_valid():
            instance = Photo(image=request.FILES['image'], user=user)
            instance.save()
            return HttpResponseRedirect("/")
        return render(request, 'user.html', {'photos': photos,
                                             'form': form})


class LikeView(View):

    def post(self, request, my_id):
        photo = Photo.objects.get(pk=my_id)
        user = request.user

        toggled_like = True
        try:
            like = Like.objects.get(author=user, photo=photo)
            toggled_like = not like.liked
        except Like.DoesNotExist:
            pass

        obj, created = Like.objects.update_or_create(author=user, photo=photo,
                                                     defaults={'liked': toggled_like})
        create = HttpResponse(toggled_like)
        return create






