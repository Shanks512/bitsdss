from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views

app_name = 'dashboard'
urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/login/'), name='go-to-login'),
    url(r'^register/$', views.register, name='register'),
    
    url(r'^dashboard/admin/$', views.admin, name='admin'),
    # url(r'^dashboard/admin/time-windows/$', views.set_time_windows, name='set-time-windows'),

    url(r'^dashboard/faculty/$', views.faculty, name='faculty'),
    url(r'^dashboard/faculty/current-courses/(?P<course_num>\w+)/$', views.faculty_current_sem_course_details, name='faculty_current_sem_course_details'),
    url(r'^dashboard/faculty/course-cart/$', views.FacultyApplicationList.as_view(), name='faculty-applied-sections'),
    url(r'^dashboard/faculty/sections/(?P<section_id>\w+)/add/$', views.faculty_add_section, name='faculty-add-section'),
    
    url(r'^dashboard/hod/$', views.hod, name='hod'),
    url(r'^dashboard/hod/dept-courses/(?P<course_num>\w+)/$', views.department_course_details, name='dept_course_details'),
    url(r'^dashboard/hod/current-courses/$', views.hod_current_courses),
    url(r'^dashboard/hod/current-courses/(?P<course_num>\w+)/$', views.hod_current_sem_course_details, name='hod_current_sem_course_details'),
    url(r'^dashboard/hod/faculty-detail/$', views.hod_faculty_detail, name='hod_faculty_detail'),
    url(r'^dashboard/hod/course-cart/$',views.HodApplicationList.as_view(), name='hod-applied-sections'),
    url(r'^dashboard/hod/sections/(?P<section_id>\w+)/add/$', views.hod_add_section, name='hod-add-section'),
    url(r'^dashboard/hod/add-to-sem/(?P<course_num>\w+)/$', views.hod_add_course_to_semester, name='hod-add-course-to-semester'),


    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout')
]
