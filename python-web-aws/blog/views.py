from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
import collections
from django.contrib import messages
from users.forms import PostFormUpdate
from django.http import HttpResponse
from .models import Post, Like, Comment
from django.contrib.auth.models import User
from blog.data_helper.helper import Tree
from django.urls import reverse


# Create your views here.
def home(request):
    top_user = get_object_or_404(User, username="Borsoi")
    return render(request, 'blog/base.html', {'top_user' : top_user})

def about(request):
    return HttpResponse('<h1>Blog About</>')

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    #post like
    likes = collections.defaultdict(list)
    like_user = post.likes.values_list('user__id', flat=True)
    like_count = post.likes.count()
    likes[post.id] = list(like_user) + [like_count]
    #user of the post
    top_user = post.author

    #init comment
    comments = Comment.objects.filter(post=post, reply = None).prefetch_related(
        'cmt_like',
        'cmt_like__user',
        'replies',
        'replies__cmt_like',
        'replies__cmt_like__user'
    ).annotate(
        cmt_like_count=models.Count('cmt_like'),
    ).select_related('user')

    def process_replies(cmt):
        print("reply:")
        print(cmt.content)
        cmt.likes_count = cmt.cmt_like.count()
        cmt.like_users = [like.user.id for like in cmt.cmt_like.all()]
        replies.append(cmt)
        for rep in cmt.replies.all():
            print("in recurse")
            process_replies(rep) 
        
    
    for comment in comments:
        print("comment:")
        print(comment.content)
        comment.like_users = [like.user.id for like in comment.cmt_like.all()]
        replies = []
        for reply in comment.replies.all():
            print(reply.content)
            process_replies(reply)
        comment.all_replies = replies

    context = {
        'post' : post,
        'top_user': top_user,
        'comments': comments,
        'likes': likes,
        'local_user': request.user,
        'cmt_count': len(comments)
    }
    return render(request, 'blog/post-detail.html', context)
 #create post in blog.views
@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = PostFormUpdate(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Update post successfully!")

    return redirect('users-profile', username=request.user.username)

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully!")

    print("work till here")
    return redirect('users-profile', username=request.user.username)
    

def like_post(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponse('Forbidden', status=401)
        if 'post_id' in request.POST and request.POST['post_id'] != '' :
            ##check likes
            post_id = request.POST['post_id']
            commented = request.POST['commented']
            user_id = request.user.id
            #check if is comment or post
            if commented=='false':
                like_exist = Like.objects.filter(post_id=post_id, user_id=user_id).exists()
                print("post activate delete")
                if like_exist:
                    like = Like.objects.filter(post_id=post_id, user_id=request.user.id).first()
                    like.delete()
                    print("function activate delete")
                else: 
                    like = Like(post_id=post_id, user_id=request.user.id)
                    like.save()
                    print(f'{request.user} like')
                return HttpResponse('Update Success', status=200)
            print("still running")
            like_exist = Like.objects.filter(comment_id=post_id, user_id=user_id).exists()
            if like_exist:
                    like = Like.objects.filter(comment_id=post_id, user_id=request.user.id).first()
                    like.delete()
                    print("function activate delete")
            else: 
                    like = Like(comment_id=post_id, user_id=request.user.id)
                    like.save()
                    print(f'{request.user} like')
            return HttpResponse('Update Success', status=200)

        else:
            return HttpResponse('Bad Request', status=400)
    
def add_comment(request,pk):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponse('Forbidden', status=401)

        post_id = pk
        content = request.POST.get('content')
        user_id = request.user.id
        print("work under post")
        if post_id and content:
            post = get_object_or_404(Post, pk=post_id)
            print(f"work under {post_id}")
            reply_id = request.POST.get('reply_id')
            if reply_id:
                reply = get_object_or_404(Comment, pk=reply_id)
            else:
                reply = None

            comment = Comment(post=post, user_id=user_id, content=content, reply=reply)
            comment.save()
            return HttpResponse('Update Success', status=200)
    return HttpResponse('Bad Request', status=400)

def search_view(request):
    query = request.GET.get('query')  # Get the search query from the request's GET parameters
    user_q = request.GET.get('user') if not query else query
    post_q = request.GET.get('post') if not query else query

    print(user_q)
    print(post_q)
    
    if user_q!= None or post_q!= None:
        # # Search users
        users_query = User.objects.filter(username__icontains=user_q)
        
        # # Search posts
        posts = Post.objects.filter(title__icontains=post_q)

        for usr in users_query:
            user_url = reverse('users-profile', args=[usr.username])
            usr.user_url = user_url
    else:
        users_query = []
        posts = []
    
    context = {
        'users': users_query,
        'posts': posts,
    }
    
    return render(request, 'blog/search_results.html', context)
