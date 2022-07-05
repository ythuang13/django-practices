from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Like, Follow


def index(request):
    posts = Post.objects.all().order_by("-timestamp")

    return render(request, "network/index.html", {
        "posts": posts
    })


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


def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    followers = user.get_followers()
    following = user.get_following()
    posts = Post.objects.all().filter(user=user).order_by("-timestamp")

    return render(request, "network/profile.html", {
        "profile_user": user,
        "followers": followers,
        "following": following,
        "posts": posts
    })


@login_required(login_url="login")
def following(request, user_id):

    # Follow a new profile must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
        

    request_user = request.user
    # Can't follow or unfollow yourself
    if request_user.id == user_id:
        return JsonResponse({"error": "Can't follow or unfollow yourself."}, status=400)

    for follow in Follow.objects.all():
        if follow.follower == request_user and follow.following.id == user_id:
            # already followed, unfollow
            follow.delete()
            break
    else:
        # not yet followed, follow
        new_follow = Follow.objects.create(follower=request_user,
                                           following=User.objects.get(pk=user_id))
    

    return JsonResponse({"message": "follow status changed successfully"}, status=201)


@login_required(login_url="login")
def follow(request):
    followed = request.user.get_following() 
    posts = Post.objects.all().filter(user__in=followed).order_by("-timestamp")

    return render(request, "network/follow.html", {
        "posts": posts,
    })


@login_required(login_url="login")
def new(request):
    if request.method == "POST":
        post_body = request.POST["body"]
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        
        try:
            new_post = Post.objects.create(user=user, body=post_body)
            new_post.save()

        except IntegrityError:
            return render(request, "network/index.html", {
                "message": "Something went wrong with your new post."
            })

    return HttpResponseRedirect(reverse("index"))