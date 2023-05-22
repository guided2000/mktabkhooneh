from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import *
from .mixins import * 
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from blog.models import post
from .models import User
from .forms import ProfileForm
from django.http import HttpResponse
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage 

# Create your views here.
 


class postlist (LoginRequiredMixin, ListView):
    template_name = "registration/home.html"
    def get_queryset(self):
        if self.request.user.is_superuser:
            return post.objects.all()
        else:
            return post.objects.filter(author=self.request.user)


class postcreate (LoginRequiredMixin,FormValidsMixin,FieldsMixin,CreateView):
    model= post
    fields =["image", "author","title","content","tags","category","status","published_date"]
    template_name="registration/article-create-update.html"
 
class postupdate (AuthorAccessMixin,FormValidsMixin,FieldsMixin,UpdateView):
    model= post
    fields =["image", "author","title","content","tags","category","status","published_date"]
    template_name="registration/article-create-update.html"
 
class postDelete( SuperUserAccessMixin ,DeleteView):
    model= post
    success_url=reverse_lazy('account:home')
    template_name= 'registration/article_confirm_delete.html'

class Profile (LoginRequiredMixin ,UpdateView):
    model= User
    template_name="registration/profile.html"
    form_class = ProfileForm
    success_url=reverse_lazy("account:profile")

    def get_object(self):
        return User.objects.get(pk = self.request.user.pk)

    def get_form_kwargs(self):
        kwargs= super(Profile,self).get_form_kwargs()
        kwargs.update({
            'user':self.request.user
        })
        return kwargs 

class login (LoginView):
     def get_success_url(self):
         user = self.request.user
         if user.is_superuser or user.is_author:
             return reverse_lazy("account:home")
         else:
             return reverse_lazy("account:profile")

       


class PasswordResetDone(PasswordResetDoneView):
    template_name="registration/password_reset_done.html"

# class Register (CreateView):
#     form_class =SignupForm
#     template_name="registration/register.html"
#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.is_active = False
#         user.save()
#         current_site = get_current_site(self.request)
#         mail_subject = 'Activate your blog account.'
#         message = render_to_string('registration/activate_account.html', {
#             'user': user,
#             'domain': current_site.domain,
#             'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#             'token':account_activation_token.make_token(user),
#         })
#         to_email = form.cleaned_data.get('email')
#         email = EmailMessage(
#                     mail_subject, message, to=[to_email]
#         )
#         email.send()
#         #return HttpResponse('Please confirm your email address to complete the registration')
#         return render(self.request, 'registration/signup.html')
class Register(CreateView):
    form_class = SignupForm
    template_name = 'registration/register.html'
    def form_valid(self,form):
        # save form in the memory not in database  
        user = form.save(commit=False)  
        user.is_active = False  
        user.save()  
        # to get the domain of the current site  
        current_site = get_current_site(self.request)  
        mail_subject = 'Activation link has been sent to your email id'  
        message = render_to_string('registration/activate_account.html', {  
            'user': user,  
            'domain': current_site.domain,  
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
            'token':account_activation_token.make_token(user),
            'protocol': 'https' if self.request.is_secure() else 'http' 
        })  
        to_email = form.cleaned_data.get('email')  
        email = EmailMessage(  
                    mail_subject, message, to=[to_email]  
        )  
        email.send()  
        return render(self.request,'registration/activation.html')   
 
def activate(request, uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()  
        # return redirect('home')
        return render(request,'registration/login.html')
        
    else:
        return HttpResponse('Activation link is invalid!')

 