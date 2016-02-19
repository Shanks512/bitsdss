from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import User, Course
from django.contrib.auth.decorators import login_required

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
    #         # <process form cleaned data>
    #         return HttpResponseRedirect('/success/')
    # else:
    #     form = MyForm(initial={'key': 'value'})

    # return render(request, 'form_template.html', {'form': form})
    state = "Please log in below..."
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
                raise forms.ValidationError(u"Your account is not active, please contact the site admin.")
        else:
            raise forms.ValidationError(u"Incorrect username/password")
    return render(request, 'login.html')


@require_http_methods(["GET", "POST"])
def register(request):
    return HttpResponse("You're looking at register")

def admin(request):
    return render(request, 'admin_dashboard.html')

def hod(request):
    return render(request, 'hod_dashboard.html')

def faculty(request):
    course_list = Course.objects.filter(is_current_sem=True)
    return render(request, 'faculty_current_sem_courses.html', {'course_list':course_list})

def logout(request):
    """
    Log users out and re-direct them to the main page.
    """
    auth_logout(request)
    return HttpResponseRedirect('/login/')

def is_faculty(user):
    return user.groups.filter(name='faculty').exists()

def is_hod(user):
    return user.groups.filter(name='hod').exists()

def is_admin(user):
    return user.groups.filter(name='admin').exists()