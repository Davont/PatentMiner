from django.conf.urls import url

from . import views

app_name = 'law_regulate'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^law_index$', views.law_index, name='law_index'),
    url(r'^law_detail$', views.law_detail, name='law_detail'),
    url(r'^law_search$', views.law_search, name='law_search'),

]