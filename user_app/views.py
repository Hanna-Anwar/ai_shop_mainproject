from django.shortcuts import render

from user_app.forms import UserRegisterForm

from user_app.models import CustomUserModel

from django.views.generic import View


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


class HomeView(View):

    def get(self,request):

        return render(request, "home.html")
