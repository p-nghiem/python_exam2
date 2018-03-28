from django.conf.urls import url
from . import views 
from django.conf import settings
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^$', views.index),
    url(r'register$', views.register),
    url(r'login$', views.login),
    url(r'success$', views.success),
    url(r'add$', views.add),
    url(r'remove$', views.remove),
    url(r'contribute$', views.contribute),
    url(r'posts_by_user$', views.posts_by_user),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout')
]