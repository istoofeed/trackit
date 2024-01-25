from django import forms
from django.core.validators import validate_email

from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Please enter your username"}),
    )
    password = forms.CharField(
        max_length=250,
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Please enter your password"}),
    )

    def clean_username(self):
        username = self.cleaned_data["username"]

        if username == "":
            raise forms.ValidationError("Please fill this field")

        if bool(User.objects.filter(username=username).exists()) == False:
            raise forms.ValidationError("User does not exists")

        return username

    def clean_password(self):
        password = self.cleaned_data["password"]

        if password == "":
            raise forms.ValidationError("Please fill this field")

        return password

    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f in self.errors:
            self.fields[f].widget.attrs.update(
                {"class": self.fields[f].widget.attrs.get("class", "") + " error"}
            )
        return ret


class SignupForm(forms.Form):
    error_css_class = "error"

    USER_TYPE = (
        ("", "Select User Type"),
        ("student", "Student"),
        ("adviser", "Adviser"),
    )

    ROLE_CHOICES = (
        ("", "Select role"),
        ("project manager", "Project Manager"),
        ("lead developer", "Lead Developer"),
        ("ui/ux designer", "UI/UX Designer"),
        ("qa tester", "QA Tester"),
    )

    name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Enter your name"}),
    )
    course = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Enter your course"}),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE, required=False)
    user_role = forms.ChoiceField(
        choices=ROLE_CHOICES, required=False, label="For Students only:"
    )
    specialized_in = forms.CharField(
        max_length=255,
        required=False,
        label="For Advisers Only:",
        widget=forms.TextInput(attrs={"placeholder": "Specialized In"}),
    )
    username = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Enter your username"}),
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={"autocomplete": "off", "placeholder": "Enter your email."}
        ),
    )
    password = forms.CharField(
        max_length=250,
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password"}),
    )
    password2 = forms.CharField(
        max_length=250,
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
        label="Confirm Password",
    )

    def clean_name(self):
        name = self.cleaned_data["name"]

        if not name:
            raise forms.ValidationError("Please fill this field")
        if User.objects.filter(name=name).exists():
            raise forms.ValidationError("Name already exists")

        return name

    def clean_course(self):
        course = self.cleaned_data["course"]

        if not course:
            raise forms.ValidationError("Please fill this field")

        return course

    def clean_username(self):
        username = self.cleaned_data["username"]

        if not username:
            raise forms.ValidationError("Please fill this field")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]

        if not email:
            raise forms.ValidationError("Please fill this field")
        if validate_email(email) == False:
            raise forms.ValidationError("Please enter a valid email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")

        return email

    def clean_password(self):
        password = self.cleaned_data["password"]

        if not password:
            raise forms.ValidationError("Please fill this field")
        if len(password) < 6:
            raise forms.ValidationError("Please longer")

        return password

    def clean_password2(self):
        password2 = self.cleaned_data["password2"]

        if not password2:
            raise forms.ValidationError("Please fill this field")

        return password2

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get("user_type")
        user_role = cleaned_data.get("user_role")
        specialized_in = cleaned_data.get("specialized_in")
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if user_type not in ["student", "adviser"]:
            raise forms.ValidationError(
                {"user_type": forms.ValidationError("Please select a  user type")}
            )

        if user_type == "student" and not user_role:
            self.add_error("user_role", forms.ValidationError("Please fill this field"))

        if user_type == "adviser" and not specialized_in:
            self.add_error(
                "specialized_in", forms.ValidationError("Please fill this field")
            )

        if password2:
            if password != password2:
                self.add_error("password2", forms.ValidationError("Password mismatch"))

    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f in self.errors:
            self.fields[f].widget.attrs.update(
                {"class": self.fields[f].widget.attrs.get("class", "") + " error"}
            )
        return ret
