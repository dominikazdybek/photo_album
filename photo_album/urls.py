"""photo_album URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app_photoalbum.views import (MainView, UserLoginView, RegisterView, LogoutView, \
                                  UserView, LikeView)
# to moje,
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', MainView.as_view(), name="main"),
    url(r'^user_login', UserLoginView.as_view(), name="user_login"),
    url(r'^register', RegisterView.as_view(), name='register'),
    url(r'^logout', LogoutView.as_view(), name="logout"),
    url(r'^user', UserView.as_view(), name="user"),
    url(r'^photo/like/(?P<my_id>(\d)+)/$', LikeView.as_view(), name='like_product'),

]

# to moje
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)