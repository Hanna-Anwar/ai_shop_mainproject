from django.shortcuts import render,redirect

from user_app.forms import UserRegisterForm,LoginForm

from user_app.models import CustomUserModel

from django.views.generic import View

from django.contrib.auth import authenticate,login,logout


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
 

class HomeView(View):

    def get(self,request):

        return render(request, "home.html")
