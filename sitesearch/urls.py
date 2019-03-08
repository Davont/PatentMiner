from django.conf.urls import url

from . import views

app_name = 'law_regulate'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^word_search$', views.word_search, name='word_search'),
    url(r'^detail$', views.detail, name='detail'),
    url(r'^collect$', views.collect, name='collect'),
    url(r'^collection$', views.collection, name='collection'),
    url(r'^excel_export$', views.excel_export, name='excel_export'),

]