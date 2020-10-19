from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Post, Profile
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginator_func(request, posts):
    page = request.GET.get("page")
    paginator = Paginator(posts, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts


def index(request):
    posts = Post.objects.all()
    paginator_posts = paginator_func(request, posts)
    context = {
        'posts': paginator_posts,
    }
    return render(request, "network/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile_view(request, profile_user_id):
    posts = Post.objects.filter(user=profile_user_id)
    paginator_posts = paginator_func(request, posts)
    context = {
        'posts': paginator_posts,
        'profile_user': User.objects.get(id=profile_user_id),
        'profile': Profile.objects.get(user=profile_user_id)
    }
    return render(request, "network/profile.html", context)

def following_posts_view(request):
    following = Profile.objects.get(user=request.user).following.all()
    posts = Post.objects.filter(user__in=following)
    paginator_posts = paginator_func(request, posts)
    context = {
        'posts': paginator_posts,
    }
    return render(request, "network/following_posts.html", context)


@login_required
def post_create(request):
    form = PostForm(request.POST)
    next_url = request.POST.get("next")
    if form.is_valid():
        content = form.cleaned_data["content"]
        post = Post(user=request.user, content=content)
        post.save()
        return redirect(next_url)
    return HttpResponseRedirect(reverse("index"))


# API view to follow a user
@csrf_exempt
@login_required
def profile_follow(request, profile_user_id):
    if request.method == "PUT":
        # Attempt to find the profile
        try:
            profile_user = User.objects.get(id=profile_user_id)
            profile = Profile.objects.get(user=profile_user_id)
            print(profile)
        except Profile.DoesNotExist:
            return JsonResponse({"error": "User Profile does not exist!"}, status=404)
        
        # Find logged in user's profile
        current_user = request.user
        current_user_profile = Profile.objects.get(user=current_user)

        # Add or remove the user from the profiles followers field
        if current_user in profile.followers.all():
            profile.followers.remove(current_user)
            current_user_profile.following.remove(profile_user)
        else:
            profile.followers.add(current_user)
            current_user_profile.following.add(profile_user)
        profile.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({"error": "Must be PUT request"}, status=400)


# API view to like a post
@csrf_exempt
@login_required
def post_like(request, post_id):
    if request.method == "PUT":
        # Attempt to find the post
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post does not exist!"}, status=404)
        
        # Add or remove the user from the post's like field
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        post.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({"error": "Must be PUT request"}, status=400)


# API view to edit an existing post
@csrf_exempt
@login_required
def post_edit(request, post_id):

    if request.method == "PUT":
        # Attempt to find the post
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post does not exist!"}, status=404)
        
        # Update the post content
        data = json.loads(request.body)
        post.content = data["content"]
        post.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({"error": "Must be PUT request"}, status=400)