from django.contrib.auth.forms import UserCreationForm

from django import forms

from user_app.models import CustomUserModel,UserProfileModel

class UserRegisterForm(UserCreationForm):

    class Meta:

        model = CustomUserModel

        fields = ['username','full_name','email','mobile_no','password1','password2']

class LoginForm(forms.Form):

    username = forms.CharField(max_length=100)

    password = forms.CharField(max_length=100)
        
      
class ForgetMailForm(forms.Form):

    email = forms.CharField(max_length=50)


class OtpVerifyForm(forms.Form):

    otp = forms.CharField(max_length=10)


class PasswordResetForm(forms.Form):

    new_password = forms.CharField(max_length=30)

    confirm_password = forms.CharField(max_length=30)

class UserProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfileModel

        fields = ['address','city','state','pincode','height','weight','body_shape','preferred_size','style_preference','favorite_color']



#These fields exist only in the form, NOT in the database.
# Django uses them for:

# User enters password → password1
# User re-enters password → password2
# Django checks if both match