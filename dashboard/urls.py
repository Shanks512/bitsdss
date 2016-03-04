from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views

app_name = 'dashboard'
urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/login/'), name='go-to-login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^home/$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    
    url(r'^dashboard/admin/$', views.admin, name='admin'),
    url(r'^dashboard/admin/time-windows/$', views.set_time_windows, name='set-time-windows'),
    url(r'^dashboard/admin/faculty-list/$', views.admin_faculty_list, name='faculty_list'),
    url(r'^dashboard/admin/add-new-course/$', views.admin_add_new_course, name='add-new-course'),

    url(r'^dashboard/admin/faculty-list/(?P<faculty_user_name>\w+)/$', views.edit_faculty_profile, name='edit-faculty-profile'),

    url(r'^dashboard/faculty/$', views.faculty, name='faculty'),
    url(r'^dashboard/faculty/current-courses/(?P<course_num>\w+)/$', views.faculty_current_sem_course_details),
    url(r'^dashboard/faculty/course-cart/$', views.FacultyApplicationList.as_view(), name='faculty-applied-sections'),
    
    # url(r'^dashboard/faculty/sections/(?P<section_id>\w+)/add/$', views.faculty_add_section, name='faculty-add-section'),
    # url(r'^dashboard/faculty/sections/(?P<section_id>\w+)/remove/$', views.faculty_remove_section, name='faculty-remove-section'),
    
    url(r'^dashboard/hod/$', views.hod, name='hod'),
    url(r'^dashboard/hod/dept-courses/(?P<course_num>\w+)/$', views.department_course_details, name='dept_course_details'),
    url(r'^dashboard/hod/current-courses/$', views.hod_current_courses),
    url(r'^dashboard/hod/current-courses/(?P<course_num>\w+)/$', views.hod_current_sem_course_details, name='hod_current_sem_course_details'),
    url(r'^dashboard/hod/course-cart/$',views.HodApplicationList.as_view(), name='hod-applied-sections'),
    url(r'^dashboard/hod/faculty-detail/$', views.hod_faculty_detail, name='hod_faculty_detail'),
    
    url(r'^applications/(?P<application_id>\w+)/assign/$', views.assign, name = 'assign-course'),
    
    url(r'^sections/(?P<section_id>\w+)/add/$', views.add_section, name='add-section'),
    url(r'^sections/(?P<section_id>\w+)/remove/$', views.remove_section, name='remove-section'),
    # url(r'^dashboard/hod/sections/(?P<section_id>\w+)/remove/$', views.hod_remove_section, name='hod-remove-section'),
    
    url(r'^dashboard/hod/sem-courses/(?P<course_num>\w+)/add/$', views.hod_add_course_to_semester, name='hod-add-course-to-semester'),
    url(r'^dashboard/hod/sem-courses/(?P<course_num>\w+)/remove/$', views.hod_remove_course_from_semester, name='hod-remove-course-from-semester'),

    url(r'^time-error/$', views.time_error, name='time_error')
]
