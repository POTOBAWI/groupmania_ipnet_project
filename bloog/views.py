from django.shortcuts import render,redirect
from django.views.generic import ListView
from .models import *
from .forms import BlogForm
# from BLOG import settings
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, get_object_or_404
from .models import Blog
from django.contrib.auth.decorators import login_required
# from django.core.mail import send_mail,EmailMessage
# from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
# from django.utils.encoding import force_bytes,force_text
# from django.template.loader import render_to_string
# from django.contrib.sites.shortcuts import get_current_site
# Create your views here.


class List(ListView):
    template_name='blog/index.html'
    queryset=Blog.objects.all()
    paginate_by=3
def detailView(request,slug):
    post=Blog.objects.get(slug=slug)
    #recuperation des commentaires liés a un post
    comments=post.comment.all() #comments fait reference au related_name ds la class comment
    if request.method=='POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save(commit=False) #enregistrement sans le champ post
            form.instance.post=post#enregistrement de post
            form.save()#enregistrement du formulaire
            return redirect ('detailView',slug=post.slug)

    else :
        form=BlogForm
    content={
        'article':post,
        'comments':comments,
        'form':BlogForm
    }
    return render(request,'blog/update.html',content)
@login_required
def index(request):
    return render(request,'blog/index.html')

def register(request):
    if request.method=='POST':
        username=request.POST["username"]
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        if User.objects.filter(username=username):
            messages.error(request,"ce nom d'utilisateur est deja pris")
            return redirect('register')
        if User.objects.filter(email=email):
            messages.error(request,"cet email possede deja un compte")
            return('register')
        if not username.isalnum():
            messages.error(request,'le nom doit etre alphanumerique')
            return redirect('register')
        if password!=password1:
            messages.error(request,'vos mots de passe ne correpondent pas')
            return redirect('register')

        mon_utilisateur=User.objects.create_user(username,email,password)
        mon_utilisateur.firstname=firstname 
        mon_utilisateur.lastname=lastname 
        mon_utilisateur.save()
        messages.success(request,'votre compte est créé avec succes')
        
        # # LE MESSAGE EMAIL

        # subject='biebvenue sur le systeme d"authentification de Bruno poto'
        # message=f"bienvenue {mon_utilisateur.firstname } {mon_utilisateur.lastname} nous sommes heureux de vous compter parmi nous"
        
        # #QUI ENVOIE LE MAIL?
        # from_email=settings.EMAIL.HOST.USER
        
        # # A QUI ?
        # to_list=[mon_utilisateur.email]
        
        # #ENVOI DU MAIL(fail silently a false permet d'avertir en cas d'erreur)
        # send_mail(subject,message,from_email,to_list,fail_silently=False)
        
        # #EMAIL DE CONFIRMATION
        return redirect ('login')
    return render(request,'blog/register.html')

def logIn(request):
    if request.method== 'POST':
        username=request.POST["username"]
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            firstname=user.first_name
            login(request,user)
        
            
            return render(request,'blog/index.html',{'firstname':firstname})
        else:
            messages.error(request,"mauvaise authentification")
            return redirect ('login')
    return render(request,'blog/login.html')

def logOut(request):
    logout(request)
    messages.success(request,'vous etes deconnecté')
    return redirect ('index')
def add_like(request, post_id):
    like, created = Like.objects.get_or_create(utilisateur=request.user, post_id=post_id)
    if not created:
        like.delete()
    return redirect('view_posts')
# views.py



def post_detail(request, post_id):
    post = get_object_or_404(Blog, pk=post_id)
    return render(request, 'post_detail.html', {'post': post})



