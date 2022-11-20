from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import  HttpResponse,HttpResponseRedirect
from main.forms import SignUpForm,CategoryForm,PostForm,LoginForm,ForbiddenWordForm,CommentForm,ReplyForm,TagForm
from main.models import Categories,Posts,ForbiddenWords,Comment,Reply,Tag
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib import messages
from django.core.mail import send_mail


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, "main/register.html", context={"form":form})

def custom_login(request):
    if request.POST:
            form = LoginForm(request.POST)
            print("here")
            if form.is_valid():
              
              username = request.POST['username']
              password = request.POST['password']
              user = authenticate(username = username, password = password)
              print(user)
              if user is not None:
                 if user.is_active:
                   login(request, user)
                   return redirect('allposts')
                 else:
                   messages.error(request, 'Your Account Is Blocked, Please Contact An Admin')
                   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
              else:  
                   messages.error(request, 'Wrong Username Or Password')
                   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = LoginForm()
    return render(request, "main/login.html",context={"form":form})

@login_required
def admin_dashboard(request):
    if request.user.is_staff:
      return render(request, "main/admindashboard.html")
    else:
      return redirect('allposts')


def list_category(request):
    categories = Categories.get_all_objects()
    return render(request, "main/Category/categories.html", context={"categories":categories})

def create_category(request):
    if request.POST:
        myform =CategoryForm(request.POST, request.FILES)
        if myform.is_valid():
            myform.save()
            return redirect('allcategories')
        else:
             return render(request, "main/Category/createcategory.html", context={"form":myform})


    myform = CategoryForm()
    return render(request, "main/Category/createcategory.html", context={"form":myform})

def edit_category(request, id):
    category = Categories.get_object(id)
    if request.POST:
        form = CategoryForm(request.POST,request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('allcategories')
        else:
            return HttpResponse("Form not valid ")
    myform = CategoryForm(instance=category)
    return render(request, "main/Category/updateCategory.html", context={"form":myform})

def delete_category(request, id):
    Categories.delete_category(id)
    return redirect('allcategories')

def list_post(request):
    posts = Posts.get_all_objects()
    return render(request, "main/Post/posts.html", context={"posts":posts,"notall":False})

def list_post_basedCategory(request,id):
    posts = Posts.filterCategory(id)
    return render(request, "main/Post/posts.html", context={"posts":posts,"notall":True})

def list_postdetails(request,id):
    post = Posts.get_object(id)
    comments=Comment.filterPost(id)
    replies=Reply.filterPost(id)
    return render(request, "main/Post/post.html", context={"post":post,"comments":comments,"replies":replies})

def create_post(request):
    if request.POST:
        myform =PostForm(request.POST, request.FILES)
        if myform.is_valid():
            myform.save()
            return redirect('allposts')
        else:
             return render(request, "main/Post/createpost.html", context={"form":myform})


    myform = PostForm()
    return render(request, "main/Post/createpost.html", context={"form":myform})

def edit_post(request, id):
    post = Posts.get_object(id)
    if request.POST:
        form = PostForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('postdetails', id=id)
        else:
            return HttpResponse("Form not valid")
    myform = PostForm(instance=post)
    return render(request, "main/Post/updatepost.html", context={"form":myform})

def delete_post(request, id):
    Posts.delete_post(id)
    return redirect('allposts')

@login_required
def list_user(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, "main/User/users.html", context={"users":users})

def list_forbiddenword(request):
    forbiddenwords = ForbiddenWords.get_all_objects()
    return render(request, "main/ForbiddenWord/forbiddenwords.html", context={"forbiddenwords":forbiddenwords})


def create_forbiddenword(request):
    if request.POST:
        myform =ForbiddenWordForm(request.POST, request.FILES)
        if myform.is_valid():
            myform.save()
            return redirect('allforbiddenwords')
        else:
             return render(request, "main/ForbiddenWord/createforbiddenword.html", context={"form":myform})
    myform = ForbiddenWordForm()
    return render(request, "main/ForbiddenWord/createforbiddenword.html", context={"form":myform})


def edit_forbiddenword(request, id):
    forbiddenword = ForbiddenWords.get_object(id)
    if request.POST:
        form = ForbiddenWordForm(request.POST,request.FILES, instance=forbiddenword)
        if form.is_valid():
            form.save()
            return redirect('allforbiddenwords')
        else:
            return HttpResponse("Form not valid ")
    myform = ForbiddenWordForm(instance=forbiddenword)
    return render(request, "main/ForbiddenWord/updateforbiddenword.html", context={"form":myform})

def delete_forbiddenword(request, id):
    ForbiddenWords.delete_forbiddenword(id)
    return redirect('allforbiddenwords')

def edit_blockuser(request,id):
      User = get_user_model()
      user = User.objects.get(id=id)
      user.is_active= not user.is_active
      user.save()
      return redirect('allusers')

def edit_adminuser(request,id):
      User = get_user_model()
      user = User.objects.get(id=id)
      user.is_staff = True
      user.save()
      return redirect('allusers')

def subscribe_user(request,id):
      category = Categories.get_object(id)
      category.users.add(request.user)
      message="You have subscribed to "+category.name
      send_mail(
     'Subscription',
      message,
     'katty_guirguis@hotmail.com',
     [request.user.email],
    fail_silently=False,
)
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def unsubscribe_user(request,id):
      category = Categories.get_object(id)
      category.users.remove(request.user)
      message="You have unsubscribed from "+category.name
      send_mail(
     'Unsubscription',
      message,
     'katty_guirguis@hotmail.com',
     [request.user.email],
    fail_silently=False,
)
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def create_comment(request,id):
    if request.POST:
        myform =CommentForm(request.POST, request.FILES)
        comment = myform.save( commit=False)  
        word_list = comment.content.split()
        result = ''
        forbiddenwords=ForbiddenWords.get_all_objects()
        for forbiddenword in forbiddenwords:
            word=forbiddenword.word
            stars = '*' * len(word)
            count = 0
            index = 0
            for i in word_list:
                 if i == word:
                  word_list[index] = stars
                 index += 1
        result =' '.join(word_list)
        comment.content=result
        comment.user = request.user
        comment.date=datetime.datetime.now()
        post=Posts.get_object(id)
        comment.post=post
        comment.save()     
        return redirect('postdetails', id=id)

    myform = CommentForm()
    return render(request, "main/Comment/createcomment.html", context={"form":myform})


def like_post(request,id):
      post = Posts.get_object(id)
      if post.likes is not None:
         post.likes=post.likes+1
         post.save()
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def dislike_post(request,id):
      post = Posts.get_object(id)
      if post.dislikes is not None:
         if post.dislikes < 10:
          post.dislikes=post.dislikes+1
          post.save()
         elif post.dislikes == 10:
          Posts.delete_post(id)
          return redirect('allposts')

      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def create_reply(request,pid,cid):
    if request.POST:
        myform =ReplyForm(request.POST, request.FILES)
        reply = myform.save( commit=False)  
        word_list = reply.content.split()
        result = ''
        forbiddenwords=ForbiddenWords.get_all_objects()
        for forbiddenword in forbiddenwords:
            word=forbiddenword.word
            stars = '*' * len(word)
            count = 0
            index = 0
            for i in word_list:
                 if i == word:
                  word_list[index] = stars
                 index += 1
        result =' '.join(word_list)
        reply.content=result
        reply.user = request.user
        reply.date=datetime.datetime.now()
        reply.post=Posts.get_object(pid)
        reply.comment=Comment.get_object(cid)
        reply.save()     
        return redirect('postdetails', id=pid)
    myform = CommentForm()
    return render(request, "main/Reply/createreply.html", context={"form":myform})


def create_tag(request):
    if request.POST:
        myform =TagForm(request.POST, request.FILES)
        if myform.is_valid():
            myform.save()
            return redirect('alltags')
        else:
             return render(request, "main/Tag/createtag.html", context={"form":myform})
    myform = TagForm()
    return render(request, "main/Tag/createtag.html", context={"form":myform})

def search(request):
     searchtag=request.GET['search_tag']
     searchtitle=request.GET['search_title']
     if searchtitle == "":
        posts=(Posts.filterTag(searchtag))
     elif searchtag == "":
        posts=(Posts.filterTitle(searchtitle))
     else:
        posts = (Posts.filterTag(searchtag) | Posts.filterTitle(searchtitle)).distinct()
     return render(request, "main/Post/posts.html", context={"posts":posts,"notall":True})

def list_tag(request):
    tags = Tag.get_all_objects()
    return render(request, "main/Tag/tags.html", context={"tags":tags})
      