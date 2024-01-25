from datetime import datetime

from django import forms
from django.core.validators import validate_email

from adviser.models import Announcement, Task, UserTask
from users.models import Group, User


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
        queryset=Group.objects.none(),
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

        # labels = {
        #     "task_no": "Task No:",
        # }

        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Enter a title for the task..."}
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

    # def clean_task_no(self):
    #     task_no = self.cleaned_data["task_no"]

    #     if not task_no:
    #         raise forms.ValidationError("Please enter the task no.")

    #     return task_no

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

    # def __init__(self, *args, **kwargs):
    #     super(TaskForm, self).__init__(*args, **kwargs)

    #     instance = kwargs.get("instance")
    #     if instance and instance.task_no:
    #         pass
    #     else:
    #         next_task_no = Task.objects.count() + 1
    #         self.initial["task_no"] = next_task_no

    def __init__(self, adviser, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields["task_type"].choices = [("", "Select a Task Type...")] + list(
            self.fields["task_type"].choices
        )[1:]

        if kwargs.get("instance"):
            self.fields.pop("groups")
        else:
            groups_queryset = Group.objects.filter(advisory__adviser=adviser)
            if groups_queryset.exists():
                self.fields["groups"].queryset = groups_queryset
            else:
                self.fields["groups"].widget = forms.TextInput(
                    attrs={
                        "readonly": "readonly",
                        "disabled": "disabled",
                        "placeholder": "No groups available",
                    },
                )


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["header", "body"]

    def clean_header(self):
        header = self.cleaned_data["header"]

        if not header:
            raise forms.ValidationError("Please enter a header for the announcement")

        return header

    def clean_body(self):
        body = self.cleaned_data["body"]

        if not body:
            raise forms.ValidationError("Please enter a content for the announcement")

        return body

    def is_valid(self):
        ret = forms.Form.is_valid(self)

        for f in self.errors:
            self.fields[f].widget.attrs.update(
                {"class": self.fields[f].widget.attrs.get("class", "") + " error"}
            )
        return ret


class AdviserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "name",
            "username",
            "email",
            "course",
            "specialized_in",
            "profile_picture",
        ]

        widgets = {"profile_picture": forms.FileInput()}

    def clean_name(self):
        name = self.cleaned_data["name"]

        if not name:
            raise forms.ValidationError("Please enter a name")

        return name

    def clean_username(self):
        username = self.cleaned_data["username"]

        if not username:
            raise forms.ValidationError("Please enter a username")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]

        if not email:
            raise forms.ValidationError("Please enter an email address")
        if validate_email(email) == False:
            raise forms.ValidationError("Please enter a valid email address")

        return email

    def clean_course(self):
        course = self.cleaned_data["course"]

        if not course:
            raise forms.ValidationError("Please enter a course")

        return course

    def clean_specialized_in(self):
        specialized_in = self.cleaned_data["specialized_in"]

        if not specialized_in:
            raise forms.ValidationError("Please enter a you're specialized in")

        return specialized_in

    def is_valid(self):
        ret = forms.Form.is_valid(self)
        for f in self.errors:
            self.fields[f].widget.attrs.update(
                {"class": self.fields[f].widget.attrs.get("class", "") + " error"}
            )
        return ret


class RevisionForm(forms.ModelForm):
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

    class Meta:
        model = Task
        fields = [
            "deadline",
        ]

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

    def is_valid(self):
        ret = forms.Form.is_valid(self)

        for f in self.errors:
            self.fields[f].widget.attrs.update(
                {"class": self.fields[f].widget.attrs.get("class", "") + " error"}
            )
        return ret
