from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'register$', views.register, name="register"),
	url(r'login$', views.login, name="login"),
	url(r'dashboard$', views.dashboard, name="home"),
	url(r'logout$', views.logout, name="logout"),
	url(r'^pokes/(?P<user_id>\d+)/$', views.poke, name="poke"),
]