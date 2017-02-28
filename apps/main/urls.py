from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^$',views.index),
    url(r'^success$', views.success),
    url(r'^create$', views.create),
    url(r'^login$', views.login),
    url(r'^create_quote$', views.create_quote),
    url(r'^user_page/(?P<id>\d+)$', views.user_page),
    url(r'^add_favorite/(?P<id>\d+)$', views.add_favorite),
    url(r'^logout$',views.logout),
    url(r'^del_favorites/(?P<id>\d+)$', views.del_favorites)
]
