from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import User, Course, Section, Application, Expertise, PrevAssignment, Tag, TimeWindow
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import *
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.forms import modelformset_factory
from django.utils.decorators import method_decorator
from datetime import date
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum

def window_dec(name):
    def window():
        w = TimeWindow.objects.get(name=name)
        if (w.start_date is None) or (w.end_date is None):
            return False
        return w.start_date <= date.today() <= w.end_date
    return window

is_selection_window = window_dec("course_selection_window")
is_application_window = window_dec("course_application_window")
is_assignment_window = window_dec("course_assignment_window")

def is_app_or_ass_window():
    print "njjnsdfjsdnsjdnsj"
    return (is_application_window() or is_assignment_window())

def time_check(window_check):
    print "kjadaskjbdasndfb"
    def wind_check(func):
       def func_wrapper(*args, **kwargs):
            if window_check():
                print "kjasdjdnas"
                return func(*args, **kwargs)
            else:
                return redirect('/time-error/')
       return func_wrapper
    return wind_check



@login_required()
def home(request):
    if is_admin(request.user):
        return redirect('/dashboard/admin/')
    if is_hod(request.user):
        return redirect('/dashboard/hod/')
    if is_faculty(request.user):
        return redirect('/dashboard/faculty/')

@require_http_methods(["GET", "POST"])
def login(request):
    logout(request)
    username = password = ''
    state = ""
    username = password = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                if is_faculty(user):
                    return HttpResponseRedirect('/dashboard/faculty/')
                if is_hod(user):
                    return HttpResponseRedirect('/dashboard/hod/')
                if is_admin(user):
                    return HttpResponseRedirect('/dashboard/admin/')
            else:
                state = "Account is not active"
        else:
            state = "Incorrect username/password"
    return render(request, 'login.html', {'state' : state})


@require_http_methods(["GET", "POST"])
def register(request): 
    if request.method=='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data["password"])
                user.first_name = form.cleaned_data["firstname"]
                user.last_name = form.cleaned_data["lastname"]
                user.save()
                if form.cleaned_data["designation"] == 'faculty':
                    g = Group.objects.get(name='faculty')
                else:
                    g = Group.objects.get(name='hod')
                g.user_set.add(user)
                Expertise.objects.create(user = user, course = form.cleaned_data["course_name"], num_years = form.cleaned_data["exp_years"])
                return HttpResponseRedirect('/login/')
    else:   
        form = RegisterForm()
    return render(request, 'register.html', {'form':form })


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login/')

def is_faculty(user):
    return user.groups.filter(name='faculty').exists()

def is_hod(user):
    return user.groups.filter(name='hod').exists()

def is_admin(user):
    return user.groups.filter(name='admin').exists()

@user_passes_test(is_admin)
def admin(request):
    course_list = Course.objects.all()
    return render(request, 'admin_department_courses.html', {'course_list':course_list})

def admin_faculty_list(request):
    user_list = User.objects.filter(groups__name='faculty') | User.objects.filter(groups__name='hod')
    return render(request, 'admin_faculty_list.html', {'user_list':user_list})

@user_passes_test(is_admin)
def edit_faculty_profile(request, faculty_user_name):
    faculty = User.objects.filter(username=faculty_user_name).first()
    expertise = Expertise.objects.filter(user=faculty).first()
    if request.method=='POST':
    	user = User.objects.filter(username=faculty_user_name).first()
        form = EditProfile(request.POST, instance=user)
        if form.is_valid():
        	form.save(commit=False)
	        user.first_name = form.cleaned_data["firstname"]
	        user.last_name = form.cleaned_data["lastname"]
	        user.save()
	        if form.cleaned_data["designation"] == 'faculty':
	            g = Group.objects.get(name='faculty')
	        else:
	            g = Group.objects.get(name='hod')
	        g.user_set.add(user)
	        g.save()
	        expertise.course = form.cleaned_data["course_name"]
	        expertise.num_years = form.cleaned_data["exp_years"]
	        '''Expertise.objects.create(user = user, course = form.cleaned_data["course_name"], num_years = form.cleaned_data["exp_years"])'''
	        expertise.save()
	        return HttpResponseRedirect('/dashboard/admin/')
    else:   
        form = EditProfile(initial={'firstname':faculty.first_name, 'lastname':faculty.last_name, 'username':faculty.username, 
    	'designation':faculty.groups.first(), 'course_name':expertise.course, 'exp_years':expertise.num_years})
    return render(request, 'admin_edit_faculty_profile.html', {'faculty': faculty, 'form':form})

def admin_add_new_course(request):
    if request.method=='POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
                course = form.save(commit=False)
                course.save()
                return HttpResponseRedirect('/dashboard/admin/')
    else:   
        form = AddCourseForm()
    return render(request, 'admin_add_course.html', {'form':form})


@user_passes_test(is_hod)
@time_check(is_app_or_ass_window)
def hod(request):
    course_list = Course.objects.all()
    return render(request, 'hod_department_courses.html', {'course_list':course_list})

@user_passes_test(is_faculty)
@login_required
@time_check(is_app_or_ass_window)
def faculty(request):
    course_list = Course.objects.filter(is_current_sem=True)
    section_list = Section.objects.filter(course__is_current_sem=True)
    return render(request, 'faculty_current_sem_courses.html', {'course_list':course_list, 'section_list':section_list})

@user_passes_test(is_faculty)
@login_required
@time_check(is_app_or_ass_window)
def faculty_current_courses(request):
    course_list = Course.objects.filter(is_current_sem=True)
    return render(request, 'faculty_current_sem_courses.html', {'course_list':course_list})

@user_passes_test(is_faculty)
@login_required
@time_check(is_app_or_ass_window)
def faculty_department_courses(request):
    course_list = Course.objects.all()
    return render(request, 'faculty_department_courses.html', {'course_list':course_list})

@user_passes_test(is_hod)
@login_required
@time_check(is_app_or_ass_window)
def hod_current_courses(request):
    course_list = Course.objects.filter(is_current_sem=True)
    section_list = Section.objects.filter(course__is_current_sem=True)
    return render(request, 'hod_current_sem_courses.html', {'course_list':course_list, 'section_list':section_list})

@user_passes_test(is_hod)
@login_required
@time_check(is_app_or_ass_window)
def hod_current_sem_course_details(request, course_num):
    course = Course.objects.get(course_code=course_num)
    sections = Section.objects.filter(course__course_code=course_num)
    prev_faculty = PrevAssignment.objects.filter(course__course_code=course_num)
    applications = Application.objects.filter(section__course = course).filter(is_assigned=False)
    faculty = User.objects.exclude(groups__name='admin').annotate(total_hours=Sum('application__section__num_hours'))
    return render(request, 'hod_current_sem_course_detail.html', {'course':course, 'sections':sections, 'prev_faculty':prev_faculty, 'applications':applications, 'faculty':faculty})

@time_check(is_assignment_window)
def assign(request, application_id):
	application = get_object_or_404(Application, pk = application_id)
	course_num = application.section.course.course_code
	application.is_assigned = True
	application.save()
	return redirect('/dashboard/hod/current-courses/' + course_num + '/')

@user_passes_test(is_hod)
@login_required
@time_check(is_selection_window)
def hod_department_courses(request):
    course_list = Course.objects.all()
    return render(request, 'hod_department_courses.html', {'course_list':course_list})

@user_passes_test(is_hod)
@login_required
@time_check(is_selection_window)
def department_course_details(request, course_num):
    course = Course.objects.get(course_code=course_num)
    return render(request, 'hod_dept_course_detail.html', {'course':course})

@user_passes_test(is_admin)
@login_required
def admin_department_courses(request):
    course_list = Course.objects.all()
    return render(request, 'admin_department_courses.html', {'course_list':course_list})

@user_passes_test(is_faculty)
@time_check(is_app_or_ass_window)
def faculty_current_sem_course_details(request, course_num):
    course = Course.objects.get(course_code=course_num)
    sections = Section.objects.filter(course__course_code=course_num)
    prev_faculty = PrevAssignment.objects.filter(course__course_code=course_num)
    return render(request, 'faculty_current_sem_course_detail.html', {'course':course, 'sections':sections, 'prev_faculty':prev_faculty})

@login_required
@time_check(is_app_or_ass_window)
def faculty_course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'dashboard/faculty_course_detail.html', {'course': course})

@user_passes_test(is_hod)
@login_required
def hod_course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'dashboard/hod_course_detail.html', {'course': course})

@user_passes_test(is_admin)
@login_required
def admin_course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'dashboard/admin_course_detail.html', {'course': course})

@user_passes_test(is_faculty)
@login_required
@time_check(is_app_or_ass_window)
def faculty_applied_sections(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'dashboard/faculty_course_detail.html', {'course': course})

@user_passes_test(is_hod)
@login_required
@time_check(is_app_or_ass_window)
def hod_faculty_detail(request):
    expertise = get_object_or_404(Expertise, user=request.application.user)
    return render(request, 'hod_faculty_detail.html', {'expertise':expertise})


@method_decorator(login_required, name='dispatch')
class FacultyApplicationList(ListView):
    context_object_name = 'application_list'
    template_name = 'faculty_course_cart.html'

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FacultyApplicationList, self).get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class FacultyApprovedList(ListView):
    context_object_name = 'approved_list'
    template_name = 'faculty_approved_courses.html'

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user).filter(is_assigned=True)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FacultyApprovedList, self).get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class HodApplicationList(UserPassesTestMixin, ListView):
    context_object_name = 'application_list'
    template_name = 'hod_course_cart.html'

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HodApplicationList, self).get_context_data(**kwargs)
        return context

    def test_func(self):
        return self.request.user.groups.filter(name='hod').exists()

@login_required
@time_check(is_application_window)
def add_section(request, section_id):
    sec = get_object_or_404(Section, pk=section_id)
    appl = Application.objects.get_or_create(user=request.user, section=sec)
    return redirect('/home/')

@login_required
@time_check(is_application_window)
def remove_section(request, section_id):
    sec = get_object_or_404(Section, pk=section_id)
    appl = Application.objects.get(user=request.user, section=sec)
    appl.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@user_passes_test(is_hod)
@login_required
@time_check(is_selection_window)
def hod_add_course_to_semester(request, course_num):
    course = get_object_or_404(Course, course_code=course_num)
    course.is_current_sem = True
    course.save()
    return redirect('/dashboard/hod/')

@user_passes_test(is_hod)
@login_required
@time_check(is_selection_window)
def hod_remove_course_from_semester(request, course_num):
    course = get_object_or_404(Course, course_code=course_num)
    course.is_current_sem = False
    course.save()
    return redirect('/dashboard/hod')

@user_passes_test(is_admin)
@login_required
def set_time_windows(request):
    selection_window = TimeWindow.objects.filter(name='course_selection_window').first()
    print selection_window.start_date
    application_window = TimeWindow.objects.filter(name='course_application_window').first()
    assignment_window = TimeWindow.objects.filter(name='course_assignment_window').first()
    return render(request, 'admin_set_time_windows.html', {'selection_window':selection_window, 'application_window':application_window,
    	'assignment_window':assignment_window})

@user_passes_test(is_admin)
@login_required
def set_selection_window(request):
    selection_window = TimeWindow.objects.filter(name='course_selection_window').first()
    if request.method=='POST':
        form = SetSelectionWindowForm(request.POST)
        form.save(commit=False)
        selection_window.start_date = form.cleaned_data["course_selection_start"]
        selection_window.end_date = form.cleaned_data["course_selection_end"]
        selection_window.save()
        print selection_window.start_date
        return HttpResponseRedirect('/home/')
    else:
        form = SetSelectionWindowForm()

@user_passes_test(is_admin)
@login_required
def set_application_window(request):
    application_window = TimeWindow.objects.filter(name='course_application_window').first()
    print application_window.start_date
    if request.method=='POST':
        form = SetApplicationWindowForm(request.POST)
        form.save(commit=False)
        application_window.start_date = form.cleaned_data["course_application_start"]
        print application_window.start_date
        application_window.end_date = form.cleaned_data["course_application_end"]
        application_window.save()
        print application_window.start_date
        return HttpResponseRedirect('/home/')
    else:
        form = SetSelectionWindowForm()

@user_passes_test(is_admin)
@login_required
def set_assignment_window(request):
    assignment_window = TimeWindow.objects.filter(name='course_assignment_window').first()
    if request.method=='POST':
        form = SetAssignmentWindowForm(request.POST)
        form.save(commit=False)
        assignment_window.start_date = form.cleaned_data["course_assignment_start"]
        assignment_window.end_date = form.cleaned_data["course_assignment_end"]
        assignment_window.save()
        print assignment_window.start_date
        return HttpResponseRedirect('/home/')
    else:
        form = SetSelectionWindowForm()

def time_error(request):
    return render(request, 'error_page.html')

@login_required
@time_check(is_application_window)
def multiple_add_section(request, section_id_list):
    new_list = section_id_list.split("_")
    for section_id in new_list:
        print (section_id)
        sec = get_object_or_404(Section, pk=section_id)
        appl = Application.objects.get_or_create(user=request.user, section=sec)
        print (section_id + " done")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))