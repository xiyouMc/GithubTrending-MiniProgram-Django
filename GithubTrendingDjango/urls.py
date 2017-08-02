"""GithubTrendingDjango URL Configuration

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
from . import login
from . import trending
from . import follow
from . import star
from . import search
from . import query_repo

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'login', login.login),
    url(r'trending', trending.Trending),
    url(r'follow', follow.GithubFollow),
    url(r'star', star.GithubStar),
    url(r'search', search.GithubSearch),
    url(r'repos', query_repo.GithubRepo)
]
