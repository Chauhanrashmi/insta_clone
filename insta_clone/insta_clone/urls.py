'''insta_clone URL Configuration

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
'''
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import *
from django.contrib.auth.views import logout
from myapp.views import signup_view, login_view, feed_view, post_view, like_view, comment_view, logout_view, upvote_view
import django.contrib.auth.views
admin.autodiscover()


#urls for views
urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^upvote/',upvote_view),
    url(r'^post/', post_view),
    url(r'^feed/', feed_view),
    url(r'^like/', like_view),
    url(r'^comment/', comment_view),
    url(r'^login/', login_view),
    url(r'^$',signup_view)
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)