from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views

app_name = 'dashboard'
urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/login/'), name='go-to-login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^dashboard/admin/$', views.admin, name='admin'),
    # url(r'^dashboard/admin/time-windows/$', views.set_time_windows, name='set-time-windows'),

    url(r'^dashboard/hod/$', views.hod, name='hod'),

    url(r'^dashboard/faculty/$', views.faculty, name='faculty'),
    url(r'^dashboard/faculty/current-courses/(?P<course_num>\w+)/$', views.faculty_current_sem_course_details, name='faculty_current_sem_course_details'),
    url(r'^dashboard/faculty/current-courses/(?P<course_num>\w+)/add/$', views.course_add, name='add-course'),
    url(r'^dashboard/faculty/course-cart/$', views.faculty_course_cart, name='faculty_course_cart'),
    
    url(r'^dashboard/hod/$', views.hod, name='hod'),
    url(r'^dashboard/hod/dept-courses/(?P<course_num>\w+)/$', views.department_course_details, name='dept_course_details'),
    url(r'^dashboard/hod/current-courses/$', views.hod_current_courses),
    url(r'^dashboard/hod/current-courses/(?P<course_num>\w+)/$', views.hod_current_sem_course_details, name='hod_current_sem_course_details'),
    url(r'^dashboard/hod/faculty-detail/$', views.hod_faculty_detail, name='hod_faculty_detail'),
    url(r'^dashboard/hod/course-cart/$', views.hod_course_cart, name='hod_course_cart'),
    url(r'^dashboard/faculty/applied-sections/$', views.ApplicationList.as_view(), name='applied-sections'),
    
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
