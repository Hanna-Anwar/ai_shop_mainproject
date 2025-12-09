from django.shortcuts import render,redirect

from user_app.forms import UserRegisterForm,LoginForm,ForgetMailForm,OtpVerifyForm,PasswordResetForm,UserProfileForm

from user_app.models import CustomUserModel,UserProfileModel

from django.views.generic import View,CreateView,DetailView,UpdateView

from django.contrib.auth import authenticate,login,logout

from django.core.mail import send_mail

from django.contrib.auth.hashers import make_password

from django.urls import reverse_lazy

import random

class UserRegisterView(View):

    def get(self, request):

        form = UserRegisterForm()

        return render(request, "registration.html", {"form": form})
    
    def post(self, request):

        form = UserRegisterForm(request.POST)

        if form.is_valid():  

            CustomUserModel.objects.create_user(
                                                username=form.cleaned_data['username'],
                                                full_name=form.cleaned_data['full_name'],
                                                email=form.cleaned_data['email'],
                                                mobile_no=form.cleaned_data['mobile_no'],
                                                password=form.cleaned_data['password1']  
            )


            return render(request, "registration.html", {
                                                         "form": UserRegisterForm(),
                                                         "msg": "User Registered Successfully!"
            })

        # If invalid

        print("Form errors:", form.errors)

        return render(request, "registration.html", {"form": form})
    


class LoginView(View):

    def get(self,request):

        form = LoginForm()

        return render(request,"login.html",{"form":form})
    
    def post(self,request):

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user:

            login(request,user)

            return redirect("home")
        
        # If login fails
        
        form = LoginForm()

        error_msg = "Invalid username or password"
        
        return render(request,"login.html",{"form":form,"error":error_msg})
    

class LogoutView(View):

    def get(self,request):

        logout(request)

        return redirect("login")
    
class ForgetEmailView(View):

    def get(self,request):

        form = ForgetMailForm()

        return render(request,"forget_mail.html",{"form":form})

    def post(self,request):

         email = request.POST.get('email')

         user = CustomUserModel.objects.get(email=email)

         if user:
             
             otp_generate = random.randint(10000,99999)

             request.session['otp'] = otp_generate

             request.session['email'] = email

             send_mail(subject="Your Fashion Store Password Reset Code",
                       message = f"""  
                                 Hello,
                                Your OTP for resetting your password is: {otp_generate}
                                If you did not request a password reset, please ignore this email.
                                Thank you,
                                Fashion Store Team""",
                                from_email= "hannaanwar469@gmail.com",
                                recipient_list=[email],
                                fail_silently=True)
             
             
             
             return redirect("otp")
         

class OtpVerifyView(View):

    def get(self,request):

        form =OtpVerifyForm()

        return render(request,"otp_verify.html",{"form":form})
    
    def post(self,request):

        form = OtpVerifyForm(request.POST)

        otp = request.POST.get('otp')

        if request.session.get('otp') == int(otp):

            return redirect("reset")

        return render(request, "otp_verify.html", {
            "form": OtpVerifyForm(),
            "error": "Invalid OTP!"
        })
    

class PasswordResetView(View):

    def get(self,request):

        form = PasswordResetForm()

        return render(request,"reset_password.html",{"form":form})

    def post(self,request):

        new_password = request.POST.get('new_password')

        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:

            return render(request,"reset.html")
        
        email = request.session.get('email')
        
        user = CustomUserModel.objects.get(email=email)

        user.password = make_password(new_password)

        user.save()

        return redirect("login")

#Profile view


class UserProfileView(CreateView):

    model = UserProfileModel

    form_class = UserProfileForm

    template_name = "profile_create.html"

    success_url = reverse_lazy("home")

    def form_valid(self, form):

        profile = form.save(commit=False)

        profile.user = self.request.user

        return super().form_valid(form)
    
    def dispatch(self, request,**kwargs):
        
        # Prevent creating multiple profiles

        if UserProfileModel.objects.filter(user=request.user).exists():

            return redirect("profile_edit") 
         
        return super().dispatch(request, **kwargs)

#detail view 
class ProfileShowView(DetailView):

    model = UserProfileModel

    template_name = "profile_show.html"

    context_object_name = "profile"

    def get_object(self):

        return UserProfileModel.objects.get(user =self.request.user)
    

#updateview
class ProfileEditView(UpdateView):

    model = UserProfileModel

    template_name = "profile_edit.html"

    form_class = UserProfileForm  # update fields

    success_url = reverse_lazy("profile_show")

    def get_object(self):

        return UserProfileModel.objects.get(user=self.request.user)

    
class HomeView(View):

    def get(self,request):

        return render(request, "home.html")
