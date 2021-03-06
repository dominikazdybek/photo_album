from django.shortcuts import render_to_response, render, redirect
from django.views import View
from .models import Photo, Like, Comment
from .forms import UploadFileForm, CommentForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
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
            instance = Photo(image=request.FILES['image'], user=user)
            instance.save()
            return HttpResponseRedirect("/")
        return render(request, 'main.html', {'photos': photos,
                                             'form': form})


class UserView(View):
    def get(self, request, name):
        user = request.user
        user1 = User.objects.get(username=name)
        like_dislike_user = Like.objects.filter(author=user)
        photos = Photo.objects.filter(user=user1).order_by('-creation_date')
        for photo in photos:
            like_dislike = photo.like_set.filter(author=user).last()
            if like_dislike is not None:
                photo.like_dislike_user = like_dislike.liked
            else:
                photo.like_dislike_user = False
        form = UploadFileForm()
        return render(request, 'user.html', {'photos': photos,
                                             'user': user,
                                             'form': form,
                                             'user1': user1})

    def post(self, request, name):
        form = UploadFileForm(request.POST, request.FILES)
        photos = Photo.objects.all()
        user = request.user
        if form.is_valid():
            instance = Photo(image=request.FILES['image'], user=user)
            instance.save()
            return HttpResponseRedirect("/")
        return render(request, 'main.html', {'photos': photos,
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


class PhotoView(View):
    def get(self, request, my_id):
        user = request.user
        form = CommentForm()
        photo = Photo.objects.get(pk=my_id)
        like_dislike_user = Like.objects.filter(author=user)
        # for photo in photos:
        like_dislike = photo.like_set.filter(author=user).last()
        if like_dislike is not None:
            photo.like_dislike_user = like_dislike.liked
        else:
            photo.like_dislike_user = False
        comment_user = Comment.objects.filter(author=request.user)
        comments = Comment.objects.filter(photo=photo).order_by('-date')
        return render_to_response('photo.html', {'photo': photo,
                                                 'comments': comments,
                                                 'user': user,
                                                 'form': form})


class PhotoCommentView(View):
    def post(self, request, my_id):
        photo = Photo.objects.get(pk=my_id)
        comment = request.body
        user = request.user
        if comment:
            # content = form.cleaned_data['content']
            new_comment = Comment.objects.create(content=comment, author=user, photo=photo)
            return JsonResponse({
                'author': new_comment.author.username,
                'date': new_comment.date,
                'comment': str(new_comment.content.decode('utf-8')),
                'id': new_comment.id
            })


class DeleteCommentView(View):
    def delete(self, request, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
        return HttpResponse(status=204)

    def put(self, request, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        comment.content = request.body
        comment.save()
        return HttpResponse(status=204)
