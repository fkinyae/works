from decimal import Context
from django.contrib.auth import forms
from django.shortcuts import render,redirect,get_object_or_404
from  django.http import HttpResponse,Http404
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.urls import reverse
from django.urls.base import reverse
from django.views.generic.base import TemplateView
from .forms import UserSignUpForm,UserUpdateForm,ProfileUpdateForm,ProjectForm,RatingForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic.edit import UpdateView
from .models import Profile,Project,Rate
from django.contrib.auth.mixins import LoginRequiredMixin

class edit_profile(generic.UpdateView):
    model=Profile
    template='accounts/edit_profile.html'
    fields=['bio','profile_pic','twitter_url']
    success_url=reverse_lazy('')



def usersignup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link=reverse('activate',kwargs={'uidb64':uidb64,'token':account_activation_token.make_token(user)})
            activate_url='http://'+domain+link
            
            email_body='Hi ' +user.username+ ' Please use this link to verify your account\n' +activate_url
            
            email_subject = 'Activate Your Account'
            
            to_email = form.cleaned_data.get('email')
            
            email = EmailMessage(email_subject, email_body, 'francis.kinyae@student.moringaschool.com',[to_email])
            
            email.send()
            
            return HttpResponse('We have sent you an email, please confirm & activate your email address to complete registration')
    else:
        
        form = UserSignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activate successfully')
        
    else:
        return HttpResponse('Activation link is invalid!')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)
        
        user = authenticate(request, password=password, username=username)
        if user is None:
            context = {"error": "Invalid username or password"}
            return render(request, "stages/accounts/login.html",context)
        login(request,user)


def logout_view(request):
    if request.method == "POST":
        logout(request)
        
def view_profile(request):
 
    return render (request, "accounts/profile.html")   

def edit_profile(request):
    if request.method=='POST':
        user_form=UserUpdateForm(request.POST, instance=request.user)
        profile_form=ProfileUpdateForm(request.POST, request.FILES,instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form=UserUpdateForm(instance=request.user)   
        profile_form=ProfileUpdateForm(instance=request.user.profile)

    context = {
        "user_form":user_form,
        "profile_form":profile_form,
        
    }
    return render (request, "accounts/edit_profile.html",context)  
   
class    PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('welcome')
    
@login_required(login_url='/accounts/login/')
def new_project(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project .user = current_user
            project .save()
            return redirect('welcome')

    else:
        form = ProjectForm()
    return render(request, 'project.html', {"form": form})    

def view_projects(request):
    projects=Project.all_projects()
    form=ProjectForm()
    return render(request, 'index.html',{"projects":projects,"form":form})


@login_required(login_url='/accounts/login/')
def rate_project(request,id):
    try:
        project = Project.objects.get(pk = id)
        ratings=Rate.get_ratings()
        
    except Project.DoesNotExist:
        raise Http404()
    current_user = request.user
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            design = form.cleaned_data['design']
            usability = form.cleaned_data['usability']
            content = form.cleaned_data['content']
            rate = form.save(commit=False)
            rate.project = project
            rate.user = current_user
            rate.design = design
            rate.usability = usability
            rate.content = content
            rate.save()
            
    all_ratings=Rate.objects.filter( project = id)
            
    designs = [d.design for d in all_ratings]
    design_average = sum(designs) / len(designs)
    
    usabilities = [u.usability for u in all_ratings]
    usability_average = sum(usabilities) / len(usabilities)
    
    contents = [c.content for c in all_ratings]
    content_average = sum(contents) / len(contents)
    
    score=(content_average + usability_average + design_average) / 3
    percent=score / 10 * 100


            
            
    form = RatingForm()
    return render(request,'rate.html',locals())
    
    
    
def search_results(request):
       if 'project' in request.GET and request.GET["project"]:
              search_term=request.GET.get("project")
              searched_projects =Project.search_project(search_term)
              message=f"{search_term}"
              
              return render(request, 'search.html',{"message":message,"projects": searched_projects })
       else:
              message="You haven't searched for any term"
              return render(request,'search.html',{"message":message})   



        