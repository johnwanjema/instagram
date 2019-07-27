from django.shortcuts import render,redirect
from .models import Comment,Profile,Image
from django.contrib.auth.models import User
from .forms import SignupForm
from django.http import HttpResponse
from .email import send_welcome_email
from .models import User,Profile,Comment
# Create your views here.
def index(request):
    return render(request, 'index.html')


def profile(request,username):
    profile = User.objects.get(username=username)
    user_details = Profile.get_by_id(profile.id)
    print(user_details.user)
    return render(request, 'profile.html' ,{'user_details':user_details,})

def signup(request):
    if request.user.is_authenticated():
        return redirect('index')
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                Profile.sendemail()  
                email = form.cleaned_data['email']
                send_welcome_email(email)             
                return HttpResponse('signup')
        else:
            form = SignupForm()
            return render(request, 'registration/registration_form.html',{'form':form})


