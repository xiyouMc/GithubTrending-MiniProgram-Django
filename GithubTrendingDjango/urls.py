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
from . import github_star_status
from . import github_unstar
import settings
from GithubModel import views as Github_views
from . import image
from . from smzdm
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'v1/login', login.login),
    url(r'v1/trending', trending.Trending),
    url(r'v2/follow', follow.GithubFollow),
    url(r'v1/star/$', star.GithubStar),
    url(r'v1/repos/search', search.GithubSearch),
    url(r'v1/repos', query_repo.GithubRepo),
    url(r'v1/star/status', github_star_status.GithubStarStatus),
    url(r'v1/unstar', github_unstar.GithubUnStar),
    url(r'v1/index.html', Github_views.index),
    url(r'v1/image/', image.Image),
    url(r'wx/',smzdm.Coupon)
]
