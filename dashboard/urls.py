from django.conf.urls import url

from . import views

app_name = 'dashboard'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^dashboard/admin/$', views.admin, name='admin'),
    url(r'^dashboard/hod/$', views.hod, name='hod'),
    url(r'^dashboard/faculty/$', views.faculty, name='faculty')
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]