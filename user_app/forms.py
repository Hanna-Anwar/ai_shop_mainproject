from django.contrib.auth.forms import UserCreationForm

from user_app.models import CustomUserModel

class UserRegisterForm(UserCreationForm):

    class Meta:

        model = CustomUserModel

        fields = ['username','full_name','email','mobile_no','password1','password2']
        
      

#These fields exist only in the form, NOT in the database.

# Django uses them for:

# User enters password → password1
# User re-enters password → password2
# Django checks if both match