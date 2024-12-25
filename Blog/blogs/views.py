from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from .models import BlogPost
from .forms import BlogPostForm


def index(request):
    posts = BlogPost.objects.order_by('-date_added')
    return render(request, 'blogs/index.html', {'posts': posts})


def profile(request):
    user_posts = BlogPost.objects.filter(author=request.user).order_by('-date_added')
    return render(request, 'blogs/profile.html', {'user_posts': user_posts})



@login_required
def new_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = BlogPostForm()
    return render(request, 'blogs/new_post.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать эту запись.")  # Ограничение доступа

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blogs/edit_post.html', {'form': form, 'post': post})



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})




def post_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'blogs/post_detail.html', {'post': post})
