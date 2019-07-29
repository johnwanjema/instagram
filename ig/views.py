from django.shortcuts import render, redirect
from .models import Comment, Profile, Image
from django.contrib.auth.models import User
from .forms import SignupForm, ImageForm, CommentForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .email import send_welcome_email
from .models import User, Profile, Comment, Image
# Create your views here.


def index(request):
    images = Image.get_allImages()
    print(images)
    return render(request, 'index.html', {'images': images})


def profile(request, username):
    profile = User.objects.get(username=username)
    user_details = Profile.get_by_id(profile.id)
    print(user_details.user)
    images = Image.get_profile_images(profile.id)
    print(images)
    return render(request, 'profile.html', {'user_details': user_details,'images': images })


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
            return render(request, 'registration/registration_form.html', {'form': form})


@login_required(login_url='/accounts/login')
def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.profile = request.user
            image.save()
            return redirect('profile', username=request.user)
    else:
        form = ImageForm()

    return render(request, 'new_image.html', {'form': form})


@login_required(login_url='/accounts/login')
def image(request, image_id):
    image = Image.get_image_id(image_id)
    comments = Comment.get_comments_by_images(image_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.user = request.user
            comment.save()
            return redirect('image', image_id=image_id)
    else:
        form = CommentForm()

    return render(request, 'image.html', {'image': image, 'form': form, 'comments': comments})


def search(request):
    if 'search' in request.GET and request.GET["search"]:
        search_term = request.GET.get("search")
        print(search_term)
        searched_profile = Profile.search_profile(search_term)
        print(searched_profile)
        message = f"{search_term}"
        return render(request, 'search.html',{"message":message,"profiles": searched_profile})
    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})


