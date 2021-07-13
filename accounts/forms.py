from django.contrib.auth.forms import UserCreationForm
from accounts.models import User

class RegisterUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "password", "email"]