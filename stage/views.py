from django.shortcuts import render,redirect
from  django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.urls import reverse
from django.urls.base import reverse
from .forms import UserSignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.contrib.auth.decorators import login_required


def welcome(request):
    return render(request, "index.html")


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
    context = {
        'user':request.user
    }    
    return render (request, "accounts/profile.html", context)    
        
        
        

       


    
class    PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('welcome')



        