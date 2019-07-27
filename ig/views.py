from django.shortcuts import render
from .models import Comment,Profile,Image
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request, 'index.html')


def profile(request,username):
    profile = User.objects.get(username=username)
    user_details = Profile.get_by_id(profile.id)
    print(user_details.user)
    return render(request, 'profile.html' ,{'user_details':user_details,})