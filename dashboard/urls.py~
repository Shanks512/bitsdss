from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views

app_name = 'dashboard'
urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/login/'), name='go-to-login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^dashboard/admin/$', views.admin, name='admin'),
    url(r'^dashboard/hod/$', views.hod, name='hod'),
    url(r'^dashboard/faculty/$', views.faculty, name='faculty'),
    url(r'^dashboard/faculty/current-courses/(?P<course_num>\w+)/$', views.current_sem_course_details, name='current_sem_course_details'),
    url(r'^dashboard/faculty/current-courses/(?P<course_num>\w+)/add/$', views.course_add, name='add-course'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]