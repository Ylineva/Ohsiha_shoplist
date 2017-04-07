from django.conf.urls import url, include

from .views import *
from .ingredient_views import *


urlpatterns = [
    url(r'^add/$', list_view),
    url(r'^delete/(?P<pk>[0-9]+)/', delete, name='delete'),
    url(r'^edit/(?P<pk>[0-9]+)/', edit_page, name='edit'),
    url(r'^home/$', home_page),
    url(r'^$', login_page),
    url(r'^logout/$', logout_page),
    url(r'^register/$', register),
    url(r'^oauth/', include('social_django.urls', namespace='social')),

]