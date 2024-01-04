from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.template import loader
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, PostForm
from .models import UserPost, Comment
from django.contrib.auth.models import User
from django.db.models import F
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

def homepage(request):
    template = loader.get_template("index.html")
    latest_post = UserPost.objects.latest('created_at')
    action = request.GET.get('action', None)
    latest_post_id = latest_post.id
    match action:
        case None:
            posts = UserPost.objects.all().order_by('-id')[:10]
        case "Newest":
            posts = UserPost.objects.all().order_by('-id')[:10]
        case "Oldest":
            posts = UserPost.objects.all()[:10]
        case "My_posts":
            username = request.user.username
            posts = [post for post in UserPost.objects.filter(username=username)][:25]
    
    return HttpResponse(template.render({"posts":posts, "latest_post_id":latest_post_id, "action":action}, request))

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You Have Been Registered")
                return redirect(reverse('uno:homepage')) 
    else:
        form = RegistrationForm()


    return render(request, 'register.html', {'form': form})

def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out")
	return redirect(reverse('uno:homepage'))

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You Have Been Logged In")
                return redirect(reverse('uno:homepage')) 
            else:
                messages.success(request, "This user does not exist")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                user= request.user
                username = user.username
                form_text = form.cleaned_data['post_text']
                p = UserPost(post_text=form_text, username = username)
                p.save()
                messages.success(request, "Succesfuly added post")
                return redirect(reverse('uno:homepage')) 
        else:
            form = PostForm()

        return render(request, 'add_post.html', {'form': form})
    else:
        messages.success(request, "You need to be logged in to do that")
        return redirect(reverse('uno:homepage'))
    
        
    
            


def like(request):
    id = request.GET.get('id')
    action = request.GET.get('action')
    post = UserPost.objects.get(pk=id)  
    user = request.user.id
    post.add_like(user_id=user)  
    post.save()
    return redirect(reverse("uno:homepage") + f'#{post.pk}&action={action}')

def dislike(request):
    id = request.GET.get('id')
    action = request.GET.get('action')
    post = UserPost.objects.get(pk=id)  
    user = request.user.id
    post.add_dislike(user_id=user)  
    post.save()
    return redirect(reverse("uno:homepage") + f'#{post.pk}&action={action}')


def edit_post(request): 
    if request.user.is_authenticated:
        id = request.GET.get("id")
        post = UserPost.objects.get(pk=id) 
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                user= request.user
                form_text = form.cleaned_data['post_text']
                post.post_text = form_text
                post.save()
                messages.success(request, "Succesfuly edited post")
                return redirect(reverse('uno:homepage') + f'#{id}') 
        else:
            form = PostForm(initial={'post_text':post.post_text})

        return render(request, 'edit_post.html', {'form': form, 'post_id': id})
    else:
        messages.success(request, "You need to be logged in to do that")
        return redirect(reverse('uno:homepage'))
    
def delete_post(request):
    id = request.GET.get("id")
    post = get_object_or_404(UserPost, pk=id)
    post.delete()
    messages.success(request, "Post succesfuly deleted")
    return redirect(reverse('uno:homepage'))

def add_comment(request):
    id = request.GET.get("id")
    post = get_object_or_404(UserPost, pk=id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                user= request.user
                username = user.username
                form_text = form.cleaned_data['post_text']
                c = Comment.objects.create(comment_text= form_text,
                                           user_post = post,
                                           created_at = timezone.now(),
                                           commenter = username
                                           )
                c.save()
                messages.success(request, "Succesfuly added comment")
                return redirect(reverse('uno:comments') + f'?id={id}')
        else:
            form = PostForm()

        return render(request, 'add_comment.html', {'form': form, 'post_id': id})
    else:
        messages.success(request, "You need to be logged in to do that")
        return redirect(reverse('uno:homepage'))
    
def comments(request):
    id = request.GET.get("id")
    post = get_object_or_404(UserPost, pk=id)
    comments_set = post.comments.all().order_by('-id')[:25]
    return render(request, 'comments.html', {'post':post,'post_id':id, 'comments':comments_set})