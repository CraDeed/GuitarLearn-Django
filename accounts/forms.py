from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SingupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 필수필드 선정
        self.fields["email"].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("이미 등록 된 이메일 주소입니다.")

        return email

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'last_name']