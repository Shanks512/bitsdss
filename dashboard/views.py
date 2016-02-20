from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import User, Course, Section, Application, Expertise, PrevAssignment, Tag, TimeWindow
from django.contrib.auth.decorators import login_required
from django import forms
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.forms import modelformset_factory

@login_required(login_url='/login/')
def index(request):
    user_list = User.objects.all()
    context = {'user_list': user_list}
    return render(request, 'dashboard.html', context)

@require_http_methods(["GET", "POST"])
def login(request):
    logout(request)
    username = password = ''
    # if request.method == "POST":
    #     form = MyForm(request.POST)
    #     if form.is_valid():
    #         # <process for239ha3e#9943649m cleaned data>
    #         return HttpResponseRedirect('/success/')
    # else:
    #     form = MyForm(initial={'key': 'value'})

    # return render(request, 'form_template.html', {'form': form})
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
                #return HttpResponseRedirect('/')
            else:
                state = "Account is not active"
        else:
            state = "Incorrect username/password"
    return render(request, 'login.html', {'state' : state})


@require_http_methods(["GET", "POST"])
def register(request):
    return HttpResponse("You're looking at register")

def admin(request):
    return render(request, 'admin_dashboard.html')

def hod(request):
    course_list = Course.objects.all()
    return render(request, 'hod_department_courses.html', {'course_list':course_list})


@login_required
def faculty(request):
    course_list = Course.objects.filter(is_current_sem=True)
    return render(request, 'faculty_current_sem_courses.html', {'course_list':course_list})

@login_required
def faculty_current_courses(request):
    course_list = Course.objects.filter(is_current_sem=True)
    return render(request, 'faculty_current_sem_courses.html', {'course_list':course_list})

@login_required
def faculty_department_courses(request):
    course_list = Course.objects.all()
    return render(request, 'faculty_department_courses.html', {'course_list':course_list})

@login_required
def hod_current_courses(request):
    course_list = Course.objects.filter(is_current_sem=True)
    return render(request, 'hod_current_sem_courses.html', {'course_list':course_list})

@login_required
def hod_current_sem_course_details(request, course_num):
    course = Course.objects.get(course_code=course_num)
    sections = Section.objects.filter(course__course_code=course_num)
    return render(request, 'hod_current_sem_course_detail.html', {'course':course, 'sections':sections})

@login_required
def hod_department_courses(request):
    course_list = Course.objects.all()
    return render(request, 'hod_department_courses.html', {'course_list':course_list})

@login_required
def department_course_details(request, course_num):
    course = Course.objects.get(course_code=course_num)
    return render(request, 'hod_dept_course_detail.html', {'course':course})

@login_required
def admin_department_courses(request):
    course_list = Course.objects.all()
    return render(request, 'admin_department_courses.html', {'course_list':course_list})

def faculty_current_sem_course_details(request, course_num):
    course = Course.objects.get(course_code=course_num)
    sections = Section.objects.filter(course__course_code=course_num)
    return render(request, 'faculty_current_sem_course_detail.html', {'course':course, 'sections':sections})

def course_add(request, course_num):
    return HttpResponse(course_num + "Added to my courses.")

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login/')

def is_faculty(user):
    return user.groups.filter(name='faculty').exists()

def is_hod(user):
    return user.groups.filter(name='hod').exists()

def is_admin(user):
    return user.groups.filter(name='admin').exists()

@login_required
def faculty_course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'dashboard/faculty_course_detail.html', {'course': course})

@login_required
def hod_course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'dashboard/hod_course_detail.html', {'course': course})

@login_required
def hod_course_cart(request):
    course_cart = Application.objects.filter(user=request.user)
    return render(request, 'hod_course_cart.html', {'course_cart':course_cart})

@login_required
def admin_course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'dashboard/admin_course_detail.html', {'course': course})

@login_required
def faculty_applied_sections(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'dashboard/faculty_course_detail.html', {'course': course})

@login_required
def faculty_course_cart(request):
    course_cart = Application.objects.filter(user=request.user)
    return render(request, 'faculty_course_cart.html', {'course_cart':course_cart})

@login_required
def hod_faculty_detail(request):
    expertise = get_object_or_404(Expertise, user=request.application.user)
    return render(request, 'hod_faculty_detail.html', {'expertise':expertise})

class ApplicationList(ListView):
    context_object_name = 'application_list'
    template_name = 'faculty_course_cart.html'

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ApplicationList, self).get_context_data(**kwargs)
        context['teacher'] = self.request.user
        return context

# def manage_sections(request):
#     SectionFormSet = modelformset_factory(Section, fields=('name', 'title'))
#     if request.method == 'POST':
#         formset = AuthorFormSet(request.POST, request.FILES)
#         if formset.is_valid():
#             formset.save()
#             # do something.
#     else:
#         formset = AuthorFormSet()
#     return render(request, 'manage_sections.html', {'formset': formset})

# def apply_to_section(request, section):
#     re