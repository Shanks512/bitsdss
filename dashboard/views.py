from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.http import require_http_methods

# Create your views here.
from .models import User, Course

def index(request):
    user_list = User.objects.all()
    context = {'user_list': user_list}
    return render(request, 'dashboard/index.html', context)

@require_http_methods(["GET", "POST"])
def login(request):
    # if request.method == "POST":
    #     form = MyForm(request.POST)
    #     if form.is_valid():
    #         # <process form cleaned data>
    #         return HttpResponseRedirect('/success/')
    # else:
    #     form = MyForm(initial={'key': 'value'})

    # return render(request, 'form_template.html', {'form': form})
	return HttpResponse("You're looking at register")

@require_http_methods(["GET", "POST"])
def register(request):
    return HttpResponse("You're looking at register")

def admin(request):
    return HttpResponse("You're looking at admin")

def hod(request):
    return HttpResponse("You're looking at hod")

def faculty(request):
    return HttpResponse("You're looking at faculty")    