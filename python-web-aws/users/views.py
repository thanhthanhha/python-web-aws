from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash, authenticate, login
import collections
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserSignUpForm, UserUpdateForm, ProfileUpdateForm, PasswordUpdateForm, PostFormUpdate, PostFormCreate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog.models import Post
from django.contrib.auth.models import User

# Create your views here.


def signup(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account is created for {username}')
            print(username)
            return redirect('blog-home')
        else: 
            print("test me")
    else:
        form = UserSignUpForm()

    if request.user.is_authenticated:
        username = request.user.username
        return redirect('user/' + username)
    
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user/' + username)  # Redirect to profile page
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/signin.html', {'form': form})

@login_required
def profile(request, username):

    if username != request.user.username:
        print(f'{username} is here')
        permission = False
        user = get_object_or_404(User, username=username)
    else :
        user = request.user
        permission = True


    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        password_form = PasswordUpdateForm(request.user, request.POST)
        post_updateform = PostFormUpdate(request.POST)
        post_createform = PostFormCreate(request.POST, request.FILES, author=request.user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('users-profile', username=user.username)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, f'Password changed successfully!')
            return redirect('users-profile', username=user.username)
        #edit post in blog.views
        if post_createform.is_valid():
            print(request.POST)
            print("in function")
            post_createform.save(author=request.user)
            return redirect('users-profile', username=user.username)

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        password_form = PasswordUpdateForm(request.user)
        post_updateform = PostFormUpdate()
        post_createform = PostFormCreate()
    
    posts = Post.objects.filter(author=user)
    likes = collections.defaultdict(list)
    for post in posts:
        post_like = post.likes.values_list('user__id', flat=True)
        like_count = post.likes.count()
        likes[post.id].extend(post_like)
        likes[post.id].append(like_count)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
        'posts': posts,
        'post_updateform': post_updateform,
        'post_createform': post_createform,
        'user' : user,
        'local_user': request.user,
        'likes' : likes
    }

    if permission == False:
        return render(request, 'users/guest_profile.html', context)
    return render(request, 'users/profile.html', context)

