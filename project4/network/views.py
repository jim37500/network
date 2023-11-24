from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Post, Comment, Follower, Like
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
import json



def index(request):
    filter_posts = Post.objects.all().order_by('-create_time')
    posts = paginate_post(request, filter_posts)
    like_messages = generate_likes_list(request, posts)
    comments_list = generate_comments_list(posts)
    return render(request, "network/index.html", {
        "posts": posts,
        "likes": like_messages,
        "comments_list": comments_list
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


@login_required
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
    

@login_required
def post(request):
    if request.method == "POST":
        content = request.POST["content"]
        new_post = Post(user=request.user, content=content)
        new_post.save()
        print("save")
        return HttpResponseRedirect(reverse("index"))
    

def profile(request, name):
    user = get_object_or_404(User, username=name)
    if request.user.is_authenticated:
        try:
            is_follow = Follower.objects.get(follower=request.user, followed_user=user)
        except ObjectDoesNotExist:
            message = "Follow"
        else:
            message = "Followed"  
        if user != request.user:
            can_follow = True
        else:
            can_follow = False
    else:
        can_follow = False
        message = ""

    filter_posts = Post.objects.filter(user=user).order_by("-create_time")
    posts = paginate_post(request, filter_posts)
    like_messages = generate_likes_list(request, posts)
    comments_list = generate_comments_list(posts)

    return render(request, "network/profile.html", {
        "user_name": user.username,
        "posts": posts,
        "can_follow": can_follow,
        "message": message,
        "likes": like_messages,
        "comments_list": comments_list
    })


def manage_follow(request, name):
    if request.method == "POST":
        user = get_object_or_404(User, username=name)
        try:
            is_follow = Follower.objects.get(follower=request.user, followed_user=user)
        except ObjectDoesNotExist:
            new_follow = Follower(follower=request.user, followed_user=user)
            new_follow.save()
        else:
            is_follow.delete()
        
        return HttpResponseRedirect(reverse("profile", args=[name]))


@login_required
def following(request):
    following_users = request.user.following.values_list("followed_user", flat=True)
    filter_posts = Post.objects.filter(user_id__in=following_users).order_by("-create_time")
    posts = paginate_post(request, filter_posts)
    like_messages = generate_likes_list(request, posts)
    comments_list = generate_comments_list(posts)

    return render(request, "network/following.html", {
        "posts": posts,
        "likes": like_messages,
        "comments_list": comments_list
    })


@csrf_exempt
@login_required
def edit_post(request, post_id):
    try:
        post = Post.objects.get(user=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == "GET":
        return JsonResponse({
            "content": post.content,
            "create_time": post.create_time.strftime('%b. %d, %Y, %I:%M %p')
        })
    
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return JsonResponse({
            "content": post.content
        })
    
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@csrf_exempt
@login_required
def manage_like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    liked = Like.objects.filter(user=request.user, post=post).exists()

    if request.method == "POST":
        if liked:
            Like.objects.filter(user=request.user, post=post).delete()
            liked = False
            post.likes -= 1
        else:
            new_like = Like(post=post, user=request.user)
            new_like.save()
            liked = True
            post.likes += 1
        post.save()
    return JsonResponse({'is_like': liked, "likes": post.likes})



@csrf_exempt
@login_required
def manage_comment_post(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content")
        if content:
            try:
                # Attempt to create a new comment
                new_comment = Comment.objects.create(post_id=post_id, user=request.user, content=content)
                post = Post.objects.get(pk=post_id)
                post.comments += 1
                post.save()
                return JsonResponse({
                    'user': request.user.username,
                    'content': new_comment.content,
                    'create_time': new_comment.create_time.strftime('%b. %d, %Y, %I:%M %p')
                    })
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'No content provided'}, status=400)


def paginate_post(request, filter_posts):
    posts_per_page = 10
    paginator = Paginator(filter_posts, posts_per_page)
    page_number = request.GET.get('page')
    
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return posts


@login_required
def generate_likes_list(request, posts):
    like_messages = []
    for post in posts:
        liked = Like.objects.filter(user=request.user, post=post).exists()
        if liked:
            message = "Unlike"
        else:
            message = "Like"
        like_messages.append(message)
    
    return like_messages


def generate_comments_list(posts):
    comments_list = []
    for post in posts:
        comments = Comment.objects.filter(post=post)
        post.comments = comments.count()
        post.save()
        comments_list.append(comments)

    
    return comments_list

















