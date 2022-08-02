from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from blogapp.models import Profile, UserToken, Post, Category, Comment, SubComment
from blogapp.forms import UpdateUserForm, UpdateProfile, UserPasswordChange, SignUpForm, LoginForm, UserPasswordReset, AddBlogForm

import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

def category(request):
    category = Category.objects.all()
    return category

# --------------------home-----------------------------------

def home(request):
    blogs = Post.objects.order_by('?')
    context = {
        'category':category(request),
        'blogs':blogs,
        }
    return render(request, 'home.html', context)

def about(request):
    context = {
        'category':category(request),
        }
    return render(request, 'about.html', context)

# -------------------profile-----------------------

def profile(request):
    if request.user.is_authenticated:

        user = User.objects.get(id=request.user.id)
        context = {
                'user':user,
                'category':category(request)
            }
        return render(request, 'profile/profile.html', context)

    else:
        return redirect('l')

def user_update(request):
    if request.user.is_authenticated:

        if request.method=='POST':
            fm = UpdateUserForm(request.POST, instance=request.user)
            if fm.is_valid():
                fm.save()
                messages.success(request,'User Update Successfully !')
                return redirect('p')
            else:
                return redirect('u')
        else:
            fm = UpdateUserForm(instance=request.user)
            return render(request, 'profile/update.html', {'form':fm, 'category':category(request)})

    else:
        return redirect('l')

def user_image_bio(request):
    if request.user.is_authenticated:

        if request.method=='POST':
            fm = UpdateProfile(request.POST, request.FILES, instance=request.user.profile)
            if fm.is_valid():
                fm.save()
                messages.success(request,'User Profile Picture Update Successfully !')
                return redirect('p')
            else:
                return redirect('u')
        else:
            fm = UpdateProfile(instance=request.user.profile)
            return render(request, 'profile/profileupdate.html', {'form':fm, 'category':category(request)})

    else:
        return redirect('l')

# ----------------------Blog---------------------------

def blog(request):
    blogs = Post.objects.order_by('?')
    context = {
        'blogs':blogs,
        'category':category(request)
    }
    return render(request, 'blog/blog.html', context)

def latest_blog(request):
    blogs = Post.objects.order_by('-add_date')
    context = {
        'blogs':blogs,
        'category':category(request)
    }
    return render(request, 'blog/latestblog.html', context)

def blog_category(request, slug):
    blog_category = Category.objects.get(slug=slug)
    blogs = Post.objects.filter(category=blog_category)
    context = {
        'blogs':blogs,
        'blogcategory':blog_category,
        'category':category(request)
    }
    return render(request, 'blog/category.html', context)

def search_blog(request):
    query = request.GET['query']
    blogs = Post.objects.filter(title__icontains=query)
    return render(request,'blog/searchblog.html',{'blogs':blogs, 'category':category(request)})

def author_profile(request, author):
    blog_user = User.objects.get(username=author)
    return render(request,'blog/authorprofile.html',{'bloguser':blog_user, 'category':category(request)})

# --------------------read post------------------------------------------

def read_post(request, slug):
    blog = Post.objects.get(slug=slug)
    comment = Comment.objects.all().order_by('-add_date')
    subcomment = SubComment.objects.all().order_by('-add_date')
    
    context = {
        'blog':blog,
        'category':category(request),
        'comment':comment,
        'subcomment':subcomment
        }
        
    return render(request, 'blog/readblog.html', context)

# --------------------------dashboard read post----------------------------

def dashboard_blog_read(request, slug):
    if request.user.is_authenticated:
        blog = Post.objects.get(slug=slug)
        comment = Comment.objects.all().order_by('-add_date')
        subcomment = SubComment.objects.all().order_by('-add_date')
        
        context = {
            'blog':blog,
            'category':category(request),
            'comment':comment,
            'subcomment':subcomment
            }
            
        return render(request, 'blog/dashboardblogread.html', context)
    else:
        return redirect('l')

# ------------------------comment read post-----------------------------

def comment(request, slug):
    if request.user.is_authenticated:
        if request.method == 'POST':
            message = request.POST['comment']
            blog = Post.objects.get(slug=slug)

            Comment.objects.create(post=blog, author=request.user, content=message)
            
            return redirect('read', slug=slug)
        else:
            return redirect('read', slug=slug)
    else:
        return redirect('l')

def subcomment(request, slug):
    if request.user.is_authenticated:
        if request.method == 'POST':
            message = request.POST['subcomment']
            id = int(request.POST['id'])

            blog = Post.objects.get(slug=slug)
            comments = Comment.objects.get(pk=id)
            
            SubComment.objects.create(post=blog, author=request.user, reply=comments, content=message)
            
            return redirect('read', slug=slug)
        else:
            return redirect('read', slug=slug)
    else:
        return redirect('l')

def delete_comment(request, slug):
    if request.method == 'POST':
        id = request.POST['id']
        comment = Comment.objects.get(pk=id)
        comment.delete()
        return redirect('read', slug=slug)

def delete_sub_comment(request, slug):
    if request.method == 'POST':
        id = request.POST['id']
        comment = SubComment.objects.get(pk=id)
        comment.delete()
        return redirect('read', slug=slug)


# -----------------------------------dashboard read comment------------------------------------

def d_comment(request, slug):
    if request.user.is_authenticated:
        if request.method == 'POST':
            message = request.POST['comment']
            blog = Post.objects.get(slug=slug)

            Comment.objects.create(post=blog, author=request.user, content=message)
            
            return redirect('dashboardblogread', slug=slug)
        else:
            return redirect('dashboardblogread', slug=slug)
    else:
        return redirect('l')

def d_subcomment(request, slug):
    if request.user.is_authenticated:
        if request.method == 'POST':
            message = request.POST['subcomment']
            id = int(request.POST['id'])

            blog = Post.objects.get(slug=slug)
            comments = Comment.objects.get(pk=id)
            
            SubComment.objects.create(post=blog, author=request.user, reply=comments, content=message)
            
            return redirect('dashboardblogread', slug=slug)
        else:
            return redirect('dashboardblogread', slug=slug)
    else:
        return redirect('l')

def d_delete_comment(request, slug):
    if request.method == 'POST':
        id = request.POST['id']
        comment = Comment.objects.get(pk=id)
        comment.delete()
        return redirect('dashboardblogread', slug=slug)

def d_delete_sub_comment(request, slug):
    if request.method == 'POST':
        id = request.POST['id']
        comment = SubComment.objects.get(pk=id)
        comment.delete()
        return redirect('dashboardblogread', slug=slug)

# -----------------------------------dashboard------------------------------------

def user_dashboard(request):
    if request.user.is_authenticated:
        blogs = Post.objects.filter(author=request.user).order_by('-add_date')
        return render(request, 'blog/dashboard.html',  {'blogs':blogs, 'category':category(request)})
    else:
        return redirect('l')

def add_blog(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = AddBlogForm(request.POST,request.FILES)
            if fm.is_valid():
                form = fm.save(commit=False)
                form.author = request.user
                form.save()
                messages.success(request,'Post Added Successfully !')
                return redirect('dashboard')
            return render(request, 'blog/addblog.html', {'form':fm, 'category':category(request)})
        else:
            fm = AddBlogForm()
            return render(request, 'blog/addblog.html', {'form':fm, 'category':category(request)})
    else:
        return redirect('l')

def update_blog(request, slug):
    if request.user.is_authenticated:
        if request.method=='POST':
            blog = Post.objects.get(slug=slug)
            fm = AddBlogForm(request.POST,request.FILES,instance=blog)
            if fm.is_valid():
                fm.save()
                messages.success(request,'Post Updated Successfully !')
                return redirect('dashboard')
            else:
                return render(request, 'blog/updateblog.html',{'form':fm, 'category':category(request)})
        else:       
            blog = Post.objects.get(slug=slug)
            fm = AddBlogForm(instance=blog)
            return render(request, 'blog/updateblog.html',{'form':fm, 'category':category(request)})
    else:
        return redirect('l')

def delete_blog(request, slug):
    post = Post.objects.get(slug=slug)
    post.delete()
    messages.success(request,'Post Deleted Successfully !')
    return redirect('dashboard')

# ------------------------User---------------------------------

def user_delete(request):
    user = User.objects.get(username=request.user)
    user.delete()
    messages.success(request,'User Account Removed Successfully !')
    return redirect('home')

def user_logout(request):
    logout(request)
    messages.success(request,'User Logout Successfully !')
    return redirect('home')

def user_login(request):
    if not request.user.is_authenticated:

        if request.method=='POST':
            fm = LoginForm(request=request, data=request.POST)
            if fm.is_valid():
                username = fm.cleaned_data['username']
                password = fm.cleaned_data['password']
                user = authenticate(username=username,password=password)
                login(request, user)
                messages.success(request,'User Login Successfully !')
                return redirect('home')
            else:
                return render(request, 'login-signup/login.html', {'form':fm})
        else:
            fm = LoginForm()
            return render(request, 'login-signup/login.html', {'form':fm})
    
    else:
        return redirect('home')

# ---------------------------email----------------------------------

def email_verification(host ,email, token):
    subject = "Verify Email"
    message = f"Hi check your link http://{host}/account-verify/{token}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)

# -------------------------signup------------------------------------

def user_account_verify(request, token):
    token = UserToken.objects.get(token=token)
    user = User.objects.get(username=token.user)

    if user.is_active == False:
        user.is_active = True
        user.save()
        return render(request, 'email-verification/send_email_verified.html')
    else:
        return render(request, 'email-verification/send_email_already_verified.html')

def user_signup(request):  
    if not request.user.is_authenticated:
        if request.method == 'POST':  
            fm = SignUpForm(request.POST)  
            if fm.is_valid():  
                form = fm.save(commit=False)  
                form.is_active = False  
                form.save()

                token = uuid.uuid4()
                profile_token = UserToken(user=form, token=token)
                profile_token.save()
                
                profile = Profile(user=form)
                profile.save()

                host = request.get_host()
                email_verification(host, form.email, token)
                
                return render(request, 'email-verification/send_email_done.html')
            else:
                return render(request, 'login-signup/signup.html', {'form': fm}) 
        else:  
            fm = SignUpForm()  
            return render(request, 'login-signup/signup.html', {'form': fm}) 
    else:
        return redirect('home')

# --------------------old password change--------------------------

def password_change(request):
    if request.user.is_authenticated:
        
        if request.method=='POST':
            fm = UserPasswordChange(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request,'User Password Change Successfully !')
                return redirect('p')
            else:
                return render(request, 'password-change/password_change.html', {'form':fm})
        else:
            fm = UserPasswordChange(user=request.user)
            return render(request, 'password-change/password_change.html', {'form':fm, 'category':category(request)})

    else:
        return redirect('home')

# -----------------------password change-------------------------

def email_password_reset(host, email, token):
    subject = "Password Reset Link"
    message = f"Hi check your link http://{host}/password-reset/{token}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)

def user_email_send(request):
    if request.method == 'POST':  
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
            pro_obj = UserToken.objects.get(user=user)
            host = request.get_host()
            email_password_reset(host, email, pro_obj.token)
        except (User.DoesNotExist, Profile.DoesNotExist) as e:
            messages.warning(request,'Invalid Email !')
            return render(request, 'password-change/password_reset_email.html')

        return render(request, 'password-change/password_reset_email_done.html')
    else:
        return render(request, 'password-change/password_reset_email.html')

def user_password_reset(request, token):
    pro_obj = UserToken.objects.get(token=token)
    user = User.objects.get(username=pro_obj.user)
    if request.method == 'POST':  
        form = UserPasswordReset(user=user, data=request.POST) 
        if form.is_valid():  
            form.save()
            return render(request, 'password-change/password_reset_done.html')
        else:
            return render(request, 'password-change/password_reset.html', {'form': form})
    else:
        form = UserPasswordReset(user=user) 
        return render(request, 'password-change/password_reset.html', {'form': form})
