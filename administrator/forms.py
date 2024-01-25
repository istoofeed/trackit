from datetime import datetime

from django import forms
from django.contrib.auth.models import Group as BaseGroup
from django.core.validators import validate_email

from adviser.models import Task
from users.models import Group

from .models import CapstoneApprovedTitle, GroupAdvisory, Guide, User


class AirDatePickerWidget(forms.TextInput):
    def format_value(self, value):
        if value:
            if isinstance(value, str):
                try:
                    value = datetime.strptime(value, "%B %d, %Y %I:%M %p")
                except ValueError:
                    pass
            return value.strftime("%B %d, %Y %I:%M %p")
        return ""


class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        required=False,
        input_formats=["%B %d, %Y %I:%M %p"],
        widget=AirDatePickerWidget(
            attrs={
                "class": "airdatepicker",
                "placeholder": "Select a date and time...",
                "autocomplete": "off",
            }
        ),
    )

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(attrs={"placeholder": "Select groups:"}),
        required=False,
        label="Select Groups:",
    )

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "deadline",
            "task_type",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Enter a title for the task..."},
            ),
            "description": forms.Textarea(
                attrs={"placeholder": "Enter the description for the task..."}
            ),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]

        if not title:
            raise forms.ValidationError("Please enter a title")

        return title

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]

        if not deadline:
            raise forms.ValidationError("Please enter a deadline")

        try:
            deadline_str = deadline.strftime("%B %d, %Y %I:%M %p")
            datetime.strptime(deadline_str, "%B %d, %Y %I:%M %p")
        except ValueError:
            raise forms.ValidationError(
                "Invalid date and time format. Please use 'MM-dd-yyyy HH:MM' format."
            )

        return deadline

    def clean_task_type(self):
        task_type = self.cleaned_data["task_type"]

        if not task_type:
            raise forms.ValidationError("Please select a task type")

        return task_type

    def clean_groups(self):
        groups = self.cleaned_data["groups"]

        if not groups:
            raise forms.ValidationError("Please select a group")

        return groups

    def is_valid(self):
        ret = forms.Form.is_valid(self)

        for f in self.errors:
            self.fields[f].widget.attrs.update(
                {"class": self.fields[f].widget.attrs.get("class", "") + " error"}
            )
        return ret

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)

        self.fields["task_type"].choices = [("", "Select a Task Type...")] + list(
            self.fields["task_type"].choices
        )[1:]

        if kwargs.get("instance"):
            self.fields.pop("groups")


class GroupAdvisoryForm(forms.ModelForm):
    class Meta:
        model = GroupAdvisory
        fields = [
            "group",
            "adviser",
        ]

    def clean_group(self):
        group = self.cleaned_data["group"]

        if not group:
            raise forms.ValidationError("Please Select a Group.")

        return group

    def clean_adviser(self):
        adviser = self.cleaned_data["adviser"]

        if not adviser:
            raise forms.ValidationError("Please Select the Adviser")

        return adviser

    def is_valid(self):
        ret = forms.Form.is_valid(self)

        for f in self.errors:
            self.fields[f].widget.attrs.update(
                {"class": self.fields[f].widget.attrs.get("class", "") + " error"}
            )
        return ret

    def __init__(self, *args, **kwargs):
        super(GroupAdvisoryForm, self).__init__(*args, **kwargs)
        advisers_group = BaseGroup.objects.get(name="adviser")
        self.fields["adviser"].queryset = advisers_group.user_set.all()


class ApprovedTitleForm(forms.ModelForm):
    class Meta:
        model = CapstoneApprovedTitle
        fields = [
            "file",
            "capstone_title",
            "description",
            "capstone_adviser",
            "group_members",
        ]

        widgets = {"file": forms.FileInput()}

    def clean_capstone_title(self):
        capstone_title = self.cleaned_data["capstone_title"]

        if not capstone_title:
            raise forms.ValidationError("Please enter a title")

        return capstone_title

    def clean_file(self):
        file = self.cleaned_data["file"]

        if not file:
            raise forms.ValidationError("Please upload a file")

        return file

    def clean_description(self):
        description = self.cleaned_data["description"]

        if not description:
            raise forms.ValidationError("Please enter a description")

        return description

    def clean_capstone_adviser(self):
        capstone_adviser = self.cleaned_data["capstone_adviser"]

        if not capstone_adviser:
            raise forms.ValidationError("Please enter the capstone adviser")

        return capstone_adviser

    def clean_group_members(self):
        group_members = self.cleaned_data["group_members"]

        if not group_members:
            raise forms.ValidationError("Please enter the group members")

        return group_members

    def is_valid(self):
        ret = forms.Form.is_valid(self)

        for f in self.errors:
            self.fields[f].widget.attrs.update(
                {"class": self.fields[f].widget.attrs.get("class", "") + " error"}
            )
        return ret


class GuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = [
            "content",
        ]

    def clean_content(self):
        content = self.cleaned_data["content"]

        if not content:
            raise forms.ValidationError("Please enter a title")

        return content

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
        widget=forms.TextInput(attrs={"placeholder": "Enter user's name"}),
    )
    course = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Enter user's course"}),
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
        widget=forms.TextInput(attrs={"placeholder": "Enter user's username"}),
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={"autocomplete": "off", "placeholder": "Enter user's email."}
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
